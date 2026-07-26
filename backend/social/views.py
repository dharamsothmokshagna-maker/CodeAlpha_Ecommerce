from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Post, Comment, Like, Follow
from django.contrib.auth import authenticate, login, logout


def home(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(request, "social/social_home.html", {
        "posts": posts
    })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "social/register.html", {
                "error": "Username already exists."
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("/social/login/")

    return render(request, "social/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/social/")

        return render(request, "social/login.html", {
            "error": "Invalid username or password."
        })

    return render(request, "social/login.html")


def logout_view(request):
    logout(request)
    return redirect("/social/")

def profile(request, username):
    profile_user = User.objects.get(username=username)

    posts = profile_user.post_set.all()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    return render(request, "social/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
    })

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("/social/login/")

    profile = request.user.profile

    if request.method == "POST":
        bio = request.POST.get("bio", "")
        profile.bio = bio

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        return redirect(
            "/social/profile/" + request.user.username + "/"
        )

    return render(request, "social/edit_profile.html", {
        "profile": profile
    })

def create_post(request):
    if not request.user.is_authenticated:
        return redirect("/social/login/")

    if request.method == "POST":
        content = request.POST["content"]

        if content.strip():
            Post.objects.create(
                user=request.user,
                content=content
            )

        return redirect("/social/")

    return render(request, "social/create_post.html")

def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect("/social/login/")

    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        content = request.POST["content"]

        if content.strip():
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect("/social/")
def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("/social/login/")

    post = Post.objects.get(id=post_id)

    like = Like.objects.filter(
        post=post,
        user=request.user
    ).first()

    if like:
        # Unlike the post
        like.delete()
    else:
        # Like the post
        Like.objects.create(
            post=post,
            user=request.user
        )

    return redirect("/social/")
def follow_user(request, username):
    if not request.user.is_authenticated:
        return redirect("/social/login/")

    user_to_follow = User.objects.get(username=username)

    # Prevent following yourself
    if request.user == user_to_follow:
        return redirect("/social/profile/" + username + "/")

    follow = Follow.objects.filter(
        follower=request.user,
        following=user_to_follow
    ).first()

    if follow:
        # Unfollow
        follow.delete()
    else:
        # Follow
        Follow.objects.create(
            follower=request.user,
            following=user_to_follow
        )

    return redirect("/social/profile/" + username + "/")