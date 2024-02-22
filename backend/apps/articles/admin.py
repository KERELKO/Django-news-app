from django.contrib import admin
from .models import (
	Article, 
	Comment, 
	Topic, 
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	display_fields = ['title', 'topic', 'status', 'published']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	display_fields = ['author', 'body', 'created', 'updated']


admin.site.register(Topic)
