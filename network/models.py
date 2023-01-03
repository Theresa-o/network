from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class NewTweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} posted {self.caption}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    # follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')
    # target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return self.user