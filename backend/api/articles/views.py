from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.apps.articles.models import Article, Topic
from . import serializers


class TopicViewSet(viewsets.ModelViewSet):
	queryset = Topic.objects.all()
	serializer_class = serializers.TopicSerializer


class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.select_related('topic').all()
	serializer_class = serializers.ArticleSerializer
    
	def get_queryset(self):
		queryset = super().get_queryset()
		# You can modify queryset based on action name
		if self.action == 'hyperlinked_with_content':
			queryset = Article.objects.select_related(
				'topic'
			).prefetch_related('content', 'comments').all()
		return queryset
		
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
