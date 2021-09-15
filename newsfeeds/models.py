from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet
# Create your models here.
class NewsFeed(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    tweet = models.ForeignKey(Tweet,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user','tweet'),)
        index_together = (('user','created_at'),)
        ordering = ('user','-created_at')

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'

