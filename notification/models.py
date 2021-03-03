from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_id = models.IntegerField()
    message_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, blank=True, default='')
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}'
