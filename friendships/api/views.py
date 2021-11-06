from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from friendships.models import Friendship
from friendships.api.serializers import (
    FollowerSerializer,
    FollowingSerializer,
    FriendshipSerializerForCreate,
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from friendships.api.paginations import FriendshipPagination
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit


class FriendshipViewSet(viewsets.GenericViewSet):

    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all()

    #assign customized pagination class
    pagination_class = FriendshipPagination

    # anyone can see any user's followers
    @action(methods=['GET'],detail=True, permission_classes=[AllowAny])
    @method_decorator(ratelimit(key='user_or_ip', rate='3/s', method='GET', block=True))
    def followers(self,request,pk):

        friendships = Friendship.objects.filter(
            to_user_id = pk
            ).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowerSerializer(page,many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    # anyone can see any user's followings
    @action(methods=["GET"],detail=True,permission_classes = [AllowAny])
    @method_decorator(ratelimit(key='user_or_ip', rate='3/s', method='GET', block=True))
    def followings(self,request,pk):
        friendships = Friendship.objects.filter(
            from_user_id=pk,
        ).order_by('-created_at')
        page = self.paginate_queryset(friendships)
        serializer = FollowingSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    #only authenticated user can initiate this follow request.
    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def follow(self, request, pk):
        #if already follow, return 201
        if Friendship.objects.filter(from_user=request.user,to_user=pk).exists():
            return Response({
                'success':True,
                'duplicate':True,
            },status=status.HTTP_201_CREATED)
        #if pk is not valid, return 400
        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': pk
        })
        if not serializer.is_valid():
            return  Response({
                'success': False,
                'error': serializer.errors,
            },status=status.HTTP_400_BAD_REQUEST)
        #if pass above validations, return success
        serializer.save()
        return Response({'success': True},status=status.HTTP_201_CREATED)

    # only authenticated user can initiate this follow request.
    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    @method_decorator(ratelimit(key='user', rate='10/s', method='POST', block=True))
    def unfollow(self, request, pk):
        #if unfollow user itself, return 400
        if request.user.id  == int(pk):
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself.'
            },status=status.HTTP_400_BAD_REQUEST)

        deleted,_ = Friendship.objects.filter(
            from_user_id=request.user.id,
            to_user_id = pk,
        ).delete()
        return Response({'success':True, 'deleted':deleted})

