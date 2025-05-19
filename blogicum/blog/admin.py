from django.contrib import admin
from .models import Comment, Post, Category, Location


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category',
                    'location', 'pub_date', 'is_published')
    list_filter = ('is_published', 'pub_date', 'category', 'location')
    search_fields = ('title', 'text', 'author__username')
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    autocomplete_fields = ('author', 'category', 'location')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'slug')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Comment)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    search_fields = ('author',)
