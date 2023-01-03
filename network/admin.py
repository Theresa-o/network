from django.contrib import admin
from .models import User, NewTweet, Profile, Followers

# Register your models here.
admin.site.register(User)
admin.site.register(NewTweet)
admin.site.register(Profile)
admin.site.register(Followers)