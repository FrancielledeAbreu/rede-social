# from django.test import TestCase
# from accounts.models import User
# from django.db import IntegrityError
# import ipdb


# class TestUserModel(TestCase):
#     def setUp(self):
#         self.guilherme_data = {
#             'username': 'guilherme',
#             'password': '1234',
#             'type': 'client'
#         }

#         self.davis_data = {
#             'username': 'davis',
#             'password': '1234',
#             'type': 'client'
#         }

#     def test_user_create(self):
#         guilherme = User.objects.create_user(**self.guilherme_data)
#         # recarregar usuário

#         guilherme = User.objects.first()

#         self.assertEqual(guilherme.username, self.guilherme_data['username'])
#         self.assertEqual(len(guilherme.followers.all()), 0)
#         self.assertEqual(len(guilherme.following.all()), 0)

#     def test_following_user(self):
#         guilherme = User.objects.create_user(**self.guilherme_data)
#         davis = User.objects.create_user(**self.davis_data)

#         # guilherme segue davis
#         guilherme.following.add(davis)

#         # ipdb.set_trace()

#         # guilherme tem que estar na lista de seguidores
#         # do davis
#         self.assertEqual(davis.followers.first(), guilherme)

#         # o davis, por enquanto, não segue ninguém
#         self.assertEqual(len(davis.following.all()), 0)

#         # ninguém segue o guillherme, por enquanto
#         self.assertEqual(len(guilherme.followers.all()), 0)

#     def test_username_is_unique(self):
#         User.objects.create_user(**self.guilherme_data)

#         with self.assertRaises(IntegrityError):
#             User.objects.create_user(**self.guilherme_data)

#     # def test_friends_association_is_symmetrical(self):
#     #     guilherme = User.objects.create_user(**self.guilherme_data)
#     #     davis = User.objects.create_user(**self.davis_data)

#     #     guilherme.friends.add(davis)

#     #     # eles têm que ser amigos um do outro
#     #     self.assertEqual(guilherme.friends.first(), davis)
#     #     self.assertEqual(davis.friends.first(), guilherme)
