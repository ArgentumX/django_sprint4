from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from ..forms import CommentForm

from ..models import Comment, Post
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

User = get_user_model()


class BaseCommentMixin(LoginRequiredMixin):
    model = Comment

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class CommentQueryMixin:
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return self.request.user.comments


class CreateCommentView(BaseCommentMixin, CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_id = self.kwargs.get('post_id')
        form.instance.post = get_object_or_404(Post, pk=post_id)
        return super().form_valid(form)


class EditCommentView(BaseCommentMixin, CommentQueryMixin, UpdateView):
    form_class = CommentForm


class DeleteCommentView(BaseCommentMixin, CommentQueryMixin, DeleteView):
    pass
