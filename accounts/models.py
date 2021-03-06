from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followers'
    )

    type = models.CharField(max_length=265)
