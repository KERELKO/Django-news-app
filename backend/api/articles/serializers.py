from rest_framework import serializers

from api.content.serializers import ContentSerializer
from apps.articles.models import Article, Topic


class TopicSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Topic  
		fields = ['name', 'id']


class LinkedArticleSerializer(serializers.ModelSerializer):
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
			'id', 'title', 'slug', 'topic', 
			'source', 'is_active', 'published'
		]


class LinkedArticleWithContentSerializer(LinkedArticleSerializer):
	content = ContentSerializer(many=True)
	class Meta:
		model = Article  
		fields = LinkedArticleSerializer.Meta.fields + ['content']


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = [
			'id', 'title', 'slug', 'topic', 
			'source', 'is_active', 'published'
		]


class ArticleWithContentSerializer(ArticleSerializer):
	content = ContentSerializer(many=True)
	class Meta:
		model = Article  
		fields = ArticleSerializer.Meta.fields + ['content']
