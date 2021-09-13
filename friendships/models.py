from django.db import models
from django.contrib.auth.models import User

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

