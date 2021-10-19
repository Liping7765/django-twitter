from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.api.serializers import UserSerializerForFriendship
from friendships.models import Friendship
from friendships.services import FriendshipService

class FollowingUserIdSetMixin:
    @property
    def following_user_id_set(self:serializers.ModelSerializer):
        if self.context['request'].user.is_anonymous:
            return {}

        if hasattr(self,'_cached_following_user_id_set'):
            return self._cached_following_user_id_set

        user_id_set = FriendshipService.get_following_user_id_set(
            self.context['request'].user.id
        )

        setattr(self,'_cached_following_user_id_set',user_id_set)
        return user_id_set



class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ('from_user_id','to_user_id',)

    def validate(self, attrs):
        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError({
                'message': 'You cannot follow yourself.',
            })
        if not User.objects.filter(id=attrs['to_user_id']).exists():
            raise ValidationError({
                'message': 'The user you are tying to follow does not exist.',
            })
        return attrs


    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']
        return Friendship.objects.create(
            from_user_id=from_user_id,
            to_user_id = to_user_id,
        )


class FollowerSerializer(serializers.ModelSerializer,FollowingUserIdSetMixin):
    user = UserSerializerForFriendship(source='from_user')
    created_at = serializers.DateTimeField()
    has_followed = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ('user','created_at','has_followed')

    def get_has_followed(self,obj):
        return obj.from_user_id in self.following_user_id_set



class FollowingSerializer(serializers.ModelSerializer,FollowingUserIdSetMixin):
    user = UserSerializerForFriendship(source='to_user')
    created_at = serializers.DateTimeField()
    has_followed = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ('user','created_at','has_followed')

    def get_has_followed(self,obj):

        if self.context['request'].user.is_anonymous:
            return False

        return obj.to_user_id in self.following_user_id_set