from rest_framework import viewsets
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

class FriendshipViewSet(viewsets.GenericViewSet):
    serializer_class = FriendshipSerializerForCreate
    queryset = User.objects.all()

    # anyone can see any user's followers
    @action(methods=['GET'],detail=True, permission_classes=[AllowAny])
    def followers(self,request,pk):
        friendships = Friendship.objects.filter(
            to_user_id = pk
            ).order_by('-created_at')
        serializer = FollowerSerializer(friendships,many=True)
        return Response({'followers':serializer.data},status=200)

    # anyone can see any user's followings
    @action(methods=["GET"],detail=True,permission_classes = [AllowAny])
    def followings(self,request,pk):
        friendships = Friendship.objects.filter(
            from_user_id=pk,
        ).order_by('-created_at')
        serializer = FollowingSerializer(friendships, many=True)
        return Response({'followings': serializer.data}, status=200)

    #only authenticated user can initiate this follow request.
    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        #if already follow, return 201
        if Friendship.objects.filter(from_user=request.user,to_user=pk).exists():
            return Response({
                'success':True,
                'duplicate':True,
            },status=201)
        #if pk is not valid, return 400
        serializer = FriendshipSerializerForCreate(data={
            'from_user_id': request.user.id,
            'to_user_id': pk
        })
        if not serializer.is_valid():
            return  Response({
                'success': False,
                'error': serializer.errors,
            },status=400)
        #if pass above validations, return success
        serializer.save()
        return Response({'success': True},status=201)

    # only authenticated user can initiate this follow request.
    @action(methods=["POST"], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        #if unfollow user itself, return 400
        if request.user.id  == int(pk):
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself.'
            },status=400)

        deleted,_ = Friendship.objects.filter(
            from_user_id=request.user.id,
            to_user_id = pk,
        ).delete()

        return Response({'success':True, 'deleted':deleted})

