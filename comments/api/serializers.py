from rest_framework import serializers
from comments.models import Comment
from accounts.api.serializers import UserSerializerForComment
from likes.services import LikeService
from tweets.models import Tweet
from rest_framework.exceptions import ValidationError

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializerForComment(source='cached_user')
    likes_count = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'tweet_id',
            'user',
            'content',
            'created_at',
            'likes_count',
            'has_liked',
        )

    def get_likes_count(self,obj):
        return obj.like_set.count()

    def get_has_liked(self,obj):
        return LikeService.has_liked(self.context['request'].user,obj)



class CommentSerializerForCreate(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ('tweet_id','user_id','content')

    def create(self, validated_data):
        return Comment.objects.create(
            tweet_id= validated_data['tweet_id'],
            user_id=validated_data['user_id'],
            content =validated_data['content'],
        )

    def validate(self, attrs):
        if not Tweet.objects.filter(id= attrs['tweet_id']).exists():
            raise ValidationError({'message':'tweet does not exist'})
        return attrs


class CommentSerializerForUpdate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('tweet_id','user_id','content')

    def update(self,instance,validated_data):
        instance.content = validated_data['content']
        instance.save()
        return instance