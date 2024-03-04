from django.db import models
from django.contrib.auth.models import AbstractUser  


class CustomUser(AbstractUser):
	get_notifications = models.BooleanField(default=False)
	