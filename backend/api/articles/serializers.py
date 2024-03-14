from rest_framework import serializers

from backend.api.content.serializers import ContentSerializer
from backend.apps.articles.models import Article, Topic


class TopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topic  
		fields = ['name', 'id']


class HyperLinkedArticleSerializer(serializers.ModelSerializer):
	published = serializers.DateTimeField(read_only=False) 
	topic = serializers.HyperlinkedRelatedField(
		read_only=True,
		view_name='api:news:topic-detail',
	)
	id = serializers.HyperlinkedRelatedField(
		read_only=True,
		view_name='api:news:article-detail'
	)
	class Meta:
		model = Article
		fields = [
			'id', 'title', 'slug', 'topic', 'description', 
			'source', 'is_active', 'published'
		]


class HyperLinkedArticleWithContentSerializer(HyperLinkedArticleSerializer):
	content = ContentSerializer(many=True)
	class Meta:
		model = Article  
		fields = HyperLinkedArticleSerializer.Meta.fields + ['content']


class ArticleSerializer(serializers.ModelSerializer):
	published = serializers.DateTimeField(read_only=False) 
	class Meta:
		model = Article
		fields = [
			'id', 'title', 'slug', 'topic', 'description',
			'source', 'is_active', 'published'
		]


class ArticleWithContentSerializer(ArticleSerializer):
	content = ContentSerializer(many=True)
	class Meta:
		model = Article  
		fields = ArticleSerializer.Meta.fields + ['content']
