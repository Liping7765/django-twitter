def incr_likes_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        return


    # NOT TO USE: tweet.likes_count += 1; tweet.save();
    # use update to make sure changes are locked
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') + 1)


def decr_likes_count(sender, instance, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        return

    # handle tweet likes cancel
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') - 1)