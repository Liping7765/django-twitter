from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedsSerializer
from utils.paginations import EndlessPagination
from newsfeeds.services import NewsFeedService

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = EndlessPagination
    #define queryset to be limited to the user only.

    def list(self,request):
        newsfeeds = NewsFeedService.get_cached_newsfeeds(request.user.id)
        page = self.paginate_queryset(newsfeeds)
        serializer = NewsFeedsSerializer(
            page,
            context={"request":request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)

