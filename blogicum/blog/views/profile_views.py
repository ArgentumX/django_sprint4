from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from blogicum import settings

from ..utils import filter_posts
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

User = get_user_model()


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

        paginator = Paginator(posts, settings.POSTS_PER_PAGE)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'profile': profile,
            'page_obj': page_obj
        })
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
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
