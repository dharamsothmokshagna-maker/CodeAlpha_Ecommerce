from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="social_home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("create-post/", views.create_post, name="create_post"),
    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
]