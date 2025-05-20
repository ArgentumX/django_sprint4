from django.urls import path
from .views import post_views
from .views import comment_views
from .views import profile_views

app_name = "blog"

urlpatterns_posts = [
    path(
        '',
        post_views.PostListView.as_view(),
        name='index',
    ),
    path(
        'posts/create/',
        post_views.CreatePostView.as_view(),
        name='create_post',
    ),
    path(
        'posts/<int:post_id>/',
        post_views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        'posts/<int:post_id>/edit/',
        post_views.EditPostView.as_view(),
        name='edit_post',
    ),
    path(
        'posts/<int:post_id>/delete/',
        post_views.DeletePostView.as_view(),
        name='delete_post',
    ),
    path(
        'category/<slug:category_slug>/',
        post_views.CategoryPostView.as_view(),
        name='category_posts',
    ),
]

urlpatterns_comments = [
    path(
        'posts/<int:post_id>/comment/',
        comment_views.CreateCommentView.as_view(),
        name='add_comment',
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        comment_views.EditCommentView.as_view(),
        name='edit_comment',
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        comment_views.DeleteCommentView.as_view(),
        name='delete_comment',
    ),
]

urlpatterns_profile = [
    path(
        'profile/edit/',
        profile_views.EditProfileView.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<slug:username>/',
        profile_views.ProfileDetailView.as_view(),
        name='profile',
    ),
]

urlpatterns = urlpatterns_posts + urlpatterns_comments + urlpatterns_profile
