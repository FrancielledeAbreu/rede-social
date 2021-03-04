from django.test import TestCase
from posts.models import Post
from accounts.models import User
from .models import Like


class LikeCommentModel(TestCase):
    def setUp(self):

        self.post_data = {
            "title": "Olá Mundo",
            "description": "projeto",
            "image": "image"
        }

        self.user_data = {
            'username': 'Teste',
            'password': '1234',
            'type': 'Client'
        }

    def test_comment_create(self):
        user = User.objects.create_user(**self.user_data)
        post = Post.objects.create(**self.post_data,  author=user)

        self.assertEqual(len(post.like.all()), 0)

        like = Like.objects.create(author=user, post=post)

        self.assertEqual(len(post.like.all()), 1)

        self.assertEqual(post.like.all().get(
            id=1), like)
