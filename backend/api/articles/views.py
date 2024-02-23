from rest_framework import viewsets

from apps.articles.models import Article, Topic
from . import serializers


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = serializers.ArticleSerializer


class TopicViewSet(viewsets.ModelViewSet):
	queryset = Topic.objects.all()
	serializer_class = serializers.TopicSerializer
