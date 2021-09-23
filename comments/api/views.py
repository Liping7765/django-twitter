from rest_framework import viewsets,status
from comments.models import Comment
from rest_framework.permissions import IsAuthenticated,AllowAny
from comments.api.permissions import IsObjectOwner
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from rest_framework.response import Response

class CommentViewSet(viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializerForCreate

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]

        if self.action in ['destroy','update']:
            return[IsAuthenticated(),IsObjectOwner()]

        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        # Note: 'data=' has to be passed in to specify
        # that the params are for data
        # the default first parameter is instance
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        # save will trigger create() method in the serializer
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self,request,*args,**kwargs):

        serializer = CommentSerializerForUpdate(
            instance = self.get_object(),
            data = request.data,
        )

        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self,request,*args,**kwargs):
        comment = self.get_object()
        comment.delete()

        return Response({'success':True},status=status.HTTP_200_OK)
