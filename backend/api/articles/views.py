from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.articles.models import Article, Topic
from . import serializers


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = serializers.ArticleSerializer
	
	# HyperLinked Serializors
	@action(
		methods=['get', 'post'],
		detail=False,
		serializer_class=serializers.HyperLinkedArticleWithContentSerializer,
	)
	def hyperlinked_with_content(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	@action(
		methods=['get', 'post'],
		detail=False,
		serializer_class=serializers.HyperLinkedArticleSerializer
	)
	def hyperlinked(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	# Simple Serializers
	@action(
		methods=['get'],
		detail=True,
		serializer_class=serializers.ArticleWithContentSerializer,
	)
	def detail_with_content(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@action(
		methods=['get', 'patch', 'delete'],
		detail=True,
		serializer_class=serializers.ArticleSerializer,
		permission_classes=[IsAuthenticated],
	)
	def detail_simple(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class TopicViewSet(viewsets.ModelViewSet):
	queryset = Topic.objects.all()
	serializer_class = serializers.TopicSerializer
