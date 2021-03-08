from django.test import TestCase
from accounts.models import User
from django.db import IntegrityError
import ipdb


class TestUserModel(TestCase):
    def setUp(self):
        self.teste_data = {
            'username': 'Teste',
            'password': '1234',
            'type': 'Client'
        }

        self.teste2_data = {
            'username': 'Teste2',
            'password': '1234',
            'type': 'Company'
        }

    def test_create(self):
        teste = User.objects.create_user(**self.teste_data)
        self.assertEqual(teste.username, self.teste_data['username'])
        self.assertEqual(teste.type, self.teste_data['type'])

    def test_following(self):
        teste = User.objects.create_user(**self.teste_data)
        teste2 = User.objects.create_user(**self.teste2_data)
        teste.following.add(teste2)
        self.assertEqual(teste2.followers.first(), teste)
        self.assertEqual(len(teste2.following.all()), 0)
        self.assertEqual(len(teste.followers.all()), 0)

    def test_username_unique(self):
        User.objects.create_user(**self.teste_data)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.teste_data)
