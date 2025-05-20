from .post_views import (
    PostListView,
    CreatePostView,
    PostDetailView,
    EditPostView,
    DeletePostView,
    CategoryPostView,
)

from .comment_views import (
    CreateCommentView,
    EditCommentView,
    DeleteCommentView,
)

from .profile_views import (
    EditProfileView,
    ProfileDetailView,
)

__all__ = [
    # post_views
    'PostListView',
    'CreatePostView',
    'PostDetailView',
    'EditPostView',
    'DeletePostView',
    'CategoryPostView',
    # comment_views
    'CreateCommentView',
    'EditCommentView',
    'DeleteCommentView',
    # profile_views
    'EditProfileView',
    'ProfileDetailView',
]
