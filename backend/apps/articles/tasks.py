from celery import shared_task
from django.shortcuts import get_object_or_404
from django.core.mail import send_mass_mail

from backend.apps.users.models import CustomUser as User
from .models import Article


@shared_task
def article_published(article_id: int) -> send_mass_mail:
	"""Send mail to the users who's 'get_notifications' field equals True"""
	article = get_object_or_404(Article, id=article_id)
	subject = 'New article was published!'
	message = (
		f'Check {article.title}\n'	
	)
	users = User.objects.filter(get_notifications=True)
	recipent_list = []
	for user in users:
		recipent_list.append(user.email)
	return send_mass_mail(subject, message, 'admin@news.com', recipent_list)
