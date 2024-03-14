from django.db import models 
from django.contrib.contenttypes.models import ContentType  
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from backend.apps.articles.models import Article


class Content(models.Model):
	article = models.ForeignKey(
		Article,
		related_name='content',
		on_delete=models.CASCADE
	)
	content_type = models.ForeignKey(
		ContentType,
		related_name='%(class)s_related',
		on_delete=models.CASCADE,
		limit_choices_to={
			'model__in':(
				'text', 
				'video',
				'image', 
			)
		},
	)
	object_id = models.PositiveIntegerField()
	content = GenericForeignKey('content_type', 'object_id')


class Item(models.Model):

	class Meta:
		abstract = True

	def render(self):
		return render_to_string(
			f'content/{self._meta.model_name}.html',
			{'item': self}
		)
	

class Text(Item):
	text = models.TextField()


class Video(Item):
	video = models.URLField()


class Image(Item):
	image = models.ImageField(upload_to='')
