from django.db import models
from accounts.models import User
from posts.models import Post


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, default='')
    commented_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,  related_name='comment')

    def __str__(self):
        return f'{self.comment}'
