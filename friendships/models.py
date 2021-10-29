from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_delete
from friendships.listeners import friendship_changed
from accounts.services import UserService
from utils.memcached_helper import MemcachedHelper

class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        #in order to avoid confusion when referencing foreign key
        related_name= 'following_friendship_set',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        # in order to avoid confusion when referencing foreign key
        related_name='follower_friendship_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            #to index two common usages of the table
            ('from_user', 'created_at'),
            ('to_user', 'created_at'),
        )
        unique_together = (('from_user','to_user'),)

    @property
    def cached_from_user(self):
        return MemcachedHelper.get_object_through_cache(User,self.from_user_id)

    @property
    def cached_to_user(self):
        return MemcachedHelper.get_object_through_cache(User,self.to_user_id)

# hook up with listeners to invalidate cache
pre_delete.connect(friendship_changed,sender= Friendship)
post_save.connect(friendship_changed,sender= Friendship)