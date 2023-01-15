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

    class Meta: 
        # Orders posts by most recent first, by default
        ordering = ['-created_at']

class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='targets')
    # target = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return self.user

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    # follower = models.ForeignKey(Followers, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class LikesPost(models.Model):
    post_id = models.CharField(max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username