from celery import shared_task
from django.shortcuts import get_object_or_404
from django.core.mail import send_mass_mail

from backend.apps.users.models import CustomUser as User
from .models import Article


@shared_task
def article_published(article_id: int) -> send_mass_mail:
    """
    Send mail to the users whose 'get_notifications' field is equal to True
    """
    article = get_object_or_404(Article, id=article_id)
    subject = 'New article was published!'
    message = f'Check {article.title}\n'
    users = User.objects.filter(get_notifications=True)
    recipient_list = [(subject, message, 'admin@news.com', (user.email,)) for user in users]
    send_mass_mail(recipient_list)
