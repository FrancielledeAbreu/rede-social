from django.db import models
from rest_framework import permissions
from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, default='')
    posted_on = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')

    class Meta:
        permissions = [
            ('author', 'author')
        ]

    def __str__(self):
        return f'{self.title}'
