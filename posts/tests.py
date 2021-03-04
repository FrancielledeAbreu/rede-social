from django.test import TestCase
from accounts.models import User
from posts.models import Post

import ipdb


class TestPostModel(TestCase):
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

    def test_post_create(self):
        user = User.objects.create_user(**self.user_data)
        post = Post.objects.create(**self.post_data,  author=user)

        self.assertEqual(post.title, self.post_data['title'])
        self.assertEqual(post.description, self.post_data['description'])
        self.assertEqual(post.image, self.post_data['image'])
        self.assertEqual(post.author, user)
        self.assertEqual(len(user.post.all()), 1)
