from django.test import TestCase
from accounts.models import User
from posts.models import Post
from .models import Notification
import ipdb


class TestNotificationModel(TestCase):
    def setUp(self):
        self.notification_data = {
            'message_type': 'Like',
            'text': 'text',

        }

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

        self.current_user_data = {
            'id': 1,
            'username': 'Flora',
            'password': '1234',
            'type': 'Client'
        }

    def test_notification_create(self):
        current_user = User.objects.create_user(**self.current_user_data)
        user = User.objects.create_user(**self.user_data)
        post = Post.objects.create(**self.post_data,  author=user)

        self.assertEqual(len(post.like.all()), 0)

        notification = Notification.objects.create(user=post.author, author_id=current_user.id,
                                                   message_type="Like", text=f'Você recebeu um like de {current_user.username} no Post {post.title}')

        # o user logado curtiu o post do user
        self.assertEqual(notification.user_id, user.id)
        self.assertEqual(notification.text,
                         'Você recebeu um like de Flora no Post Olá Mundo')
