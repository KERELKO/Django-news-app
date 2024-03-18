from django.contrib import admin
from .models import (
    Article,
    Comment,
    Topic,
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'is_active', 'published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'body', 'created', 'edited']


admin.site.register(Topic)
