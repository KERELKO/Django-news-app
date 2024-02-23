from rest_framework import viewsets
from rest_framework.decorators import action

from apps.articles.models import Article, Topic
from . import serializers


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = serializers.LinkedArticleSerializer
	
	# HyperLinked Serializors
	@action(
		methods=['get'],
		detail=True,
		serializer_class=serializers.LinkedArticleWithContentSerializer,
	)
	def linked_detail_with_content(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@action(
		methods=['get'],
		detail=True,
		serializer_class=serializers.LinkedArticleSerializer
	)
	def linked_detail_simple(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	# Simple Serializers
	@action(
		methods=['get'],
		detail=True,
		serializer_class=serializers.ArticleWithContentSerializer,
	)
	def detail_with_content(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@action(
		methods=['get'],
		detail=True,
		serializer_class=serializers.ArticleSerializer,
	)
	def detail_simple(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class TopicViewSet(viewsets.ModelViewSet):
	queryset = Topic.objects.all()
	serializer_class = serializers.TopicSerializer
