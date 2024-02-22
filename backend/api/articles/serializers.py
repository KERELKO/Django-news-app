from rest_framework import serializers

from apps.articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = [
			'title', 'slug', 'topic',
			'source', 'is_active', 'published'
		]
