from rest_framework import viewsets

from apps.articles.models import Article
from . import serializers


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = serializers.ArticleSerializer
