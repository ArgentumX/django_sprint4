from django.urls import path
from . import views
app_name = "blog"

urlpatterns_posts = [
    path(
        '',
        views.PostListView.as_view(),
        name='index'
    ),
    path(
        'posts/create/',
        views.CreatePostView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.EditPostView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:post_id>/delete/',
        views.DeletePostView.as_view(),
        name='delete_post'
    ),
    path(
        'category/<slug:category_slug>/',
        views.CategoryPostView.as_view(),
        name='category_posts'
    ),
]

urlpatterns_comments = [
    path(
        'posts/<int:post_id>/comment/',
        views.CreateCommentView.as_view(),
        name='add_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.EditCommentView.as_view(),
        name='edit_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.DeleteCommentView.as_view(),
        name='delete_comment'
    ),
]

urlpatterns_profile = [
    path(
        'profile/edit/',
        views.EditProfileView.as_view(),
        name='edit_profile'
    ),
    path(
        'profile/<slug:username>/',
        views.ProfileDetailView.as_view(),
        name='profile'
    ),
]

urlpatterns = urlpatterns_posts + urlpatterns_comments + urlpatterns_profile
