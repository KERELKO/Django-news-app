from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # if True send notifications to the user; otherwise, do not
    get_notifications = models.BooleanField(default=False)
