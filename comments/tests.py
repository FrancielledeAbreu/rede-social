from django.test import TestCase
from posts.models import Post
from accounts.models import User
from .models import Comment
import ipdb
# Create your tests here.


class TestCommentModel(TestCase):
    def setUp(self):

        self.comment_data = {
            "comment": "comment",
            "image": "image"

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

    def test_comment_create(self):
        user = User.objects.create_user(**self.user_data)
        post = Post.objects.create(**self.post_data,  author=user)
        comment = Comment.objects.create(
            **self.comment_data, author=user, post=post)

        self.assertEqual(comment.comment, self.comment_data['comment'])

        # ipdb.set_trace()
        self.assertEqual(post.comment.all().get(
            id=1), comment)
