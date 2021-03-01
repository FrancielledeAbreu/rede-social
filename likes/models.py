from django.db import models
from accounts.models import User
from posts.models import Post


class Like(models.Model):
    like_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='like')

    def __str__(self):
        return f'{self.id}'
