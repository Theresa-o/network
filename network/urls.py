
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("update_like", views.update_like, name="update_like"),
    path("following_feed", views.following_feed, name="following_feed"),
]
