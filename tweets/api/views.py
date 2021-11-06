from django.utils.decorators import method_decorator
from newsfeeds.services import NewsFeedService
from ratelimit.decorators import ratelimit
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import (
    TweetSerializer,
    TweetSerializerForCreate,
    TweetSerializerForDetail,
)
from tweets.models import Tweet
from tweets.services import TweetService
from utils.decorators import required_params
from utils.paginations import EndlessPagination


class TweetViewSet(viewsets.GenericViewSet):

    queryset = Tweet.objects.all()
    serializer_class = TweetSerializerForCreate
    pagination_class = EndlessPagination

    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(ratelimit(key='user_or_ip', rate='5/s', method='GET', block=True))
    def retrieve(self,request, *args, **kwargs):
        tweet= self.get_object()
        return Response(TweetSerializerForDetail(
            tweet,
            context={"request":request},
        ).data)

    @method_decorator(ratelimit(key='user', rate='1/s', method='POST', block=True))
    @method_decorator(ratelimit(key='user', rate='5/m', method='POST', block=True))
    def create(self, request, *args, **kwargs):
        """
        Overload create method,
        because the existed user should be used as userid.
        """
        serializer = TweetSerializerForCreate(
            data= request.data,
            context = {"request": request},
        )

        if not serializer.is_valid():
            return Response({
                'success':False,
                'message': 'Please check input',
                'errors' : serializer.errors,
            },status=400)
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(
            tweet,
            context={"request": request},
        ).data,status = 201)

    @required_params(params=['user_id'])
    def list(self,request,*args, **kwargs):
        """
        Reload list method,
        not showing all tweets but just filtered by user_id.
        Replaced if_statements with decorator to check required parameters.
        """
        user_id = request.query_params['user_id']
        cached_tweets = TweetService.get_cached_tweets(user_id)
        page = self.paginator.paginate_cached_list(cached_tweets, request)

        if page is None:
            queryset = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
            page = self.paginate_queryset(queryset)

        serializer = TweetSerializer(
            page,
            context={"request": request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)

