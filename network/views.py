from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from itertools import chain
from django.core.paginator import Paginator

from .models import User, NewTweet, Profile, Followers, LikesPost


def index(request):
    all_post = NewTweet.objects.all()
    pagination = Paginator(NewTweet.objects.all(), 3)
    page = request.GET.get('page')
    paginated_posts = pagination.get_page(page)

    context = {
        "all_post": all_post,
        "paginated_posts": paginated_posts,
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
    follower = request.user
    user = user_id
    # if Followers.objects.filter(follower=follower, user=user).first():

    # if request.user.is_authenticated:
    #     following = Followers.objects.filter(follower=follower, user=profile_user).exists()
    # else:
    #     following = False

    followers_user = len(Followers.objects.filter(user=user_id))
    following_user = len(Followers.objects.filter(follower=user_id))

    context = {
        "profile_user": profile_user,
        "post_count": post_count,
        "profile_post": profile_post,
        "followers_user": followers_user,
        "following_user": following_user,
        # "following": following,
    }

    return render(request, "network/profile.html", context)

# @login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.user

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            # delete_follower.save()
            following = False
            context = {
                "following": following,
                "profile_user": user,
            }

            return render(request, "network/profile.html", context)
            # return HttpResponseRedirect(reverse("follow"))
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            following = True
            context = {
                "following": following,
                "profile_user": user,
            }

            return render(request, "network/profile.html", context)
            # return HttpResponseRedirect(reverse("follow"))


    else:
        return HttpResponseRedirect(reverse("index"))

def update_like(request):
    username = request.user
    post_id = request.GET.get('post_id')
    post = NewTweet.objects.get(id = post_id)
    all_post = NewTweet.objects.all()

    like_filter = LikesPost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikesPost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.save()
        likes_post = True
        like_count = LikesPost.objects.filter(post_id=post_id, username=username).count()
        context = {
            "all_post": all_post, 
            'likes': like_count, 
            "likesPost": likes_post
        }
        return render(request, "network/index.html", context)
        # return render(request, 'network/index.html', {'likes': like_count, "likesPost": likes_post})
        # return JsonResponse({"likes": like_count, "likesPost": likes_post})

    else:
        like_filter.delete()
        post.save()
        likes_post = False
        like_count = LikesPost.objects.filter(post_id=post_id, username=username).count()
        context = {
            "all_post": all_post, 
            'likes': like_count, 
            "likesPost": likes_post
        }
        return render(request, "network/index.html", context)
        # return JsonResponse({"likes": like_count, "likesPost": likes_post})
        # return render(request, 'network/index.html', {'likes': like_count, "likesPost": likes_post})

def following_feed(request):
    user_following_list = []
    user_following_feed = []

    user_following = Followers.objects.filter(follower=request.user)

    for users in user_following:
        user_following_list.append(users.user)

    for users in user_following_list:
        feed_lists = NewTweet.objects.filter(user=users)
        user_following_feed.append(feed_lists)

    feed_list = list(chain(*user_following_feed))
    
    context = {
        "following_post": feed_list,
    }
    return render(request, "network/following.html", context)
    