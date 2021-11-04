from newsfeeds.models import NewsFeed
from newsfeeds.tasks import fanout_newsfeeds_task
from twitter.cache import USER_NEWSFEEDS_PATTERN
from utils.redis_helper import RedisHelper

class NewsFeedService(object):
    @classmethod
    def fanout_to_followers(cls,tweet):

        # （因为这里只是创建了一个任务，把任务信息放在了 message queue 里，并没有真正执行这个函数）
        # 要注意的是，delay 里的参数必须是可以被 celery serialize 的值，因为 worker 进程是一个独立
        # 的进程，甚至在不同的机器上，没有办法知道当前 web 进程的某片内存空间里的值是什么。所以
        # 我们只能把 tweet.id 作为参数传进去，而不能把 tweet 传进去。因为 celery 并不知道
        # 如何 serialize Tweet。
        fanout_newsfeeds_task.delay(tweet.id)

    @classmethod
    def get_cached_newsfeeds(cls, user_id):
        queryset = NewsFeed.objects.filter(user_id=user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=user_id)
        return RedisHelper.load_objects(key, queryset)

    @classmethod
    def push_newsfeed_to_cache(cls, newsfeed):
        queryset = NewsFeed.objects.filter(user_id=newsfeed.user_id).order_by('-created_at')
        key = USER_NEWSFEEDS_PATTERN.format(user_id=newsfeed.user_id)
        RedisHelper.push_object(key, newsfeed, queryset)






