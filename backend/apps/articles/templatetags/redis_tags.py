from django.conf import settings  
from django.template import Library  
from ..models import Article

register = Library()
r = settings.DEFAULT_REDIS_CLIENT


@register.inclusion_tag('articles/most_viewed_articles.html')
def most_viewed_articles(count: int) -> dict:
	"""A function to get a list of the most-viewed articles using Redis"""
	
	# Get article IDs from the sorted set 'article_ranking'
	# in descending order (from highest to lowest score)
	article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:count]
	
	# Convert article IDs from bytes to integers and store them in a list
	article_ranking_ids = [int(id) for id in article_ranking]
	
	# Retrieve Article objects for the most viewed articles using the retrieved IDs
	most_viewed = list(Article.active.filter(id__in=article_ranking_ids))
	
	# Sort the most_viewed list based on the order of IDs in article_ranking_ids
	# This ensures that the most_viewed list is in the same order as the sorted set
	most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))
	return {'most_viewed_articles': most_viewed}
