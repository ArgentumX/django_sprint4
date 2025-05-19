from django.db.models import Count
from django.utils import timezone
from .models import Post


def _filter_posts_and_count_comments(
    queryset: list[Post],
    **kwargs
) -> list[Post]:
    queryset = queryset.filter(
        **kwargs
    ).order_by('-pub_date').annotate(comment_count=Count('comments'))
    return queryset


def filter_posts_for_author(
    queryset: list[Post],
    **kwargs
) -> list[Post]:
    return _filter_posts_and_count_comments(
        queryset,
        **kwargs
    )


def filter_posts_for_reader(
    queryset: list[Post],
    **kwargs
) -> list[Post]:
    return _filter_posts_and_count_comments(
        queryset,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True,
        **kwargs
    )


def filter_posts(
    queryset: list[Post],
    for_author=False,
    **kwargs
) -> list[Post]:
    if for_author:
        return filter_posts_for_author(queryset, **kwargs)
    else:
        return filter_posts_for_reader(queryset, **kwargs)
