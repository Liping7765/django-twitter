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
        cached_newsfeeds = NewsFeedService.get_cached_newsfeeds(request.user.id)
        page = self.paginator.paginate_cached_list(cached_newsfeeds,request)

        if page is None:
            queryset = NewsFeed.objects.filter(user=request.user)
            page = self.paginate_queryset(queryset)

        serializer = NewsFeedsSerializer(
            page,
            context={"request":request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)

