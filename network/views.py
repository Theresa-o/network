from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User, NewTweet, Profile, Followers, LikesPost


def index(request):
    all_post = NewTweet.objects.all()
    context = {
        "all_post": all_post,
    }
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        # author = request.user.username
        author = request.user
        caption = request.POST["caption"]
        new_post = NewTweet.objects.create(user=author, caption=caption)
        new_post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
        # return render(request, "network/layout.html", context)

def profile(request, user_id):
    profile_user = User.objects.get(pk = user_id)
    # user_profile = Profile.objects.get(user=user_object)
    profile_post = NewTweet.objects.filter(user = user_id)
    post_count = len(profile_post)
    follower = request.user.username
    # user = profile_user
    # if Followers.objects.filter(follower=follower, user=user).first():

    if Followers.objects.filter(follower=follower, user=profile_user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    context = {
        "profile_user": profile_user,
        "post_count": post_count,
        "profile_post": profile_post,
        "button_text": button_text,
    }

    return render(request, "network/profile.html", context)

# @login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return HttpResponseRedirect(reverse("follow"))
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return HttpResponseRedirect(reverse("follow"))


    else:
        return HttpResponseRedirect(reverse("index"))

def update_like(request):
    username = request.user
    post_id = request.GET.get('post_id')
    post = NewTweet.objects.get(id = post_id)

    like_filter = LikesPost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikesPost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        like_filter.delete()
        post.save()
        return HttpResponseRedirect(reverse("index"))
    