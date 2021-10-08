from testing.testcases import TestCase
from datetime import timedelta
from utils.time_helpers import utc_now


class TweetTests(TestCase):
    def setUp(self):
        self.linghu = self.create_user('ling')
        self.tweet = self.create_tweet(self.linghu, content='This is a test')

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now, 10)

    def test_like_set(self):
        #test: owner create like
        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        #test: owner create like uniquely
        self.create_like(self.linghu, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        #test: different user create like
        dongxie = self.create_user('dongxie')
        self.create_like(dongxie, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)