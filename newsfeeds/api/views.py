from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedsSerializer
from utils.paginations import EndlessPagination

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = EndlessPagination
    #define queryset to be limited to the user only.
    def get_queryset(self):
        return NewsFeed.objects.filter(user=self.request.user)

    def list(self,request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = NewsFeedsSerializer(
            page,
            context={"request":request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)

