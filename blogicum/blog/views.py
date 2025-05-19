from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from blogicum import settings
from .forms import CommentForm, PostForm

from .utils import filter_posts_for_reader, filter_posts
from .models import Category, Comment, Post
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, \
    ListView, UpdateView

User = get_user_model()


class PostListView(ListView):
    model = Post
    paginate_by = settings.POSTS_PER_PAGE
    template_name = 'blog/index.html'

    def get_queryset(self):
        return filter_posts_for_reader(super().get_queryset())


class CategoryPostView(ListView):
    model = Post
    paginate_by = settings.POSTS_PER_PAGE
    template_name = 'blog/category.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category, slug=category_slug, is_published=True)
        self.category = category
        queryset = super().get_queryset()
        queryset = filter_posts_for_reader(
            queryset=queryset,
            category=category
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'category': self.category
        })
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        queryset = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        obj = get_object_or_404(queryset, pk=post_id)
        return filter_posts(
            queryset,
            for_author=(obj.author == self.request.user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        context.update({
            'form': CommentForm(),
            'comments': comments
        })
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.all()

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.is_authenticated or post.author != request.user:
            return redirect('blog:post_detail', post_id=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return self.request.user.posts

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_id = self.kwargs.get('post_id')
        form.instance.post = get_object_or_404(Post, pk=post_id)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return self.request.user.comments

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return self.request.user.comments

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.pk}
        )


class ProfileDetailView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        posts = filter_posts(
            profile.posts,
            for_author=(profile == self.request.user)
        )

        # 10 постов на страницу
        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'profile': profile,
            'page_obj': page_obj
        })
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
