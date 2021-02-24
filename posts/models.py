from django.db import models
from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, default='')
    posted_on = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    image = models.CharField(max_length=255, blank=True, default='')
    commented_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,  related_name='comment')

    def __str__(self):
        return f'{self.comment}'


class Like(models.Model):
    like_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='like')

    def __str__(self):
        return f'{self.id}'
