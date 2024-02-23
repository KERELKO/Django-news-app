from rest_framework import serializers

from apps.articles.models import Article, Topic


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = [
			'id', 'title', 'slug', 'topic', 
			'source', 'is_active', 'published'
		]


class TopicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Topic  
		fields = ['name', 'id']
