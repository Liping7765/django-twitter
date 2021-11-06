from rest_framework import viewsets
from likes.models import Like
from inbox.services import NotificationService
from likes.api.serializers import (
    LikeSerializer,
    LikeSerializerForCreate,
    LikeSerializerForCancel,
)
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from rest_framework.permissions import IsAuthenticated
from utils.decorators import required_params
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

class LikeViewSet(viewsets.GenericViewSet):
    query_set = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializerForCreate

    @required_params(method="POST",params=["object_id","content_type"])
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def create(self,request):
        serializer = LikeSerializerForCreate(
            data= request.data,
            context = {'request':request},
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save will trigger create() method in the serializer
        instance, created = serializer.get_or_create()
        if created:
            NotificationService.send_like_notification(instance)
        return Response(
            LikeSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['POST'],detail=False,)
    @required_params(method="POST",params=["object_id","content_type"])
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def cancel(self,request):
        serializer = LikeSerializerForCancel(
            data= request.data,
            context= {'request':request},
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        deleted = serializer.cancel()
        return Response(
            {
                'success':True,
                'deleted':deleted

             },status=status.HTTP_200_OK)




