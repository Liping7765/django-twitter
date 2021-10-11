from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedsSerializer
from rest_framework.response import Response

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    #define queryset to be limited to the user only.
    def get_queryset(self):
        return NewsFeed.objects.filter(user=self.request.user)

    def list(self,request):
        serializer = NewsFeedsSerializer(
            self.get_queryset(),
            context={"request":request},
            many=True,
        )
        return Response({
            'newsfeeds': serializer.data,
        },status=200)

