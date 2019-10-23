import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# długości wyrzucone do zmiennych, na wypadek, gdyby miałyby być użyte w innych miejscach. Wygodniej będzie je zmienić.


TWITTER_MAXIMUM_TWEET_LENGTH = 280
TWITTER_MAXIMUM_COMMENT_LENGTH = 60
TWITTER_MAXIMUM_MSG_LENGTH = 64


class Tweet(models.Model):
    content = models.CharField(max_length=TWITTER_MAXIMUM_TWEET_LENGTH)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '[{}] TWEET by {}: {}'.format(self.creation_date, self.author, self.content[:20])


class Message(models.Model):
    to_user = models.ForeignKey(User, on_delete=True)
    from_user = models.ForeignKey(Tweet, on_delete=True)
    subject = models.CharField(max_length=40)
    content = models.TextField(max_length=200)
    date_sent = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=TWITTER_MAXIMUM_COMMENT_LENGTH)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_tweet = models.ForeignKey(Tweet, on_delete=True)

    def __str__(self):
        return '[{}] TWEET by {}: {}'.format(self.comment_date, self.comment_author, self.comment_text[:20])


