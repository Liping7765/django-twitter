from rest_framework import viewsets
from likes.models import Like
from likes.api.serializers import LikeSerializer,LikeSerializerForCreate
from rest_framework.permissions import IsAuthenticated
from utils.decorators import required_params
from rest_framework import status
from rest_framework.response import Response

class LikeViewSet(viewsets.GenericViewSet):
    query_set = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializerForCreate

    @required_params(request_attr='data',params=["object_id","content_type"])
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
        like = serializer.save()
        return Response(
            LikeSerializer(like).data,
            status=status.HTTP_201_CREATED,
        )







