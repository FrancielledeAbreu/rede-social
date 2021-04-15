from django.http import HttpResponse
from django.views import View
import csv

from django.shortcuts import get_object_or_404

from accounts.models import User
from notification.models import Notification


class ReportViewFollowers(View):

    def get(self, request, user_id):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        user = get_object_or_404(User, id=user_id)

        my_followers = user.followers.all()

        writer = csv.DictWriter(response, [])

        formatted_header = ['username'] + ['type']

        writer.fieldnames = formatted_header
        writer.writeheader()

        for user in my_followers:
            row = {'username': user.username, 'type': user.type}

            writer.writerow(row)

        return response


class ReportViewFollowing(View):

    def get(self, request, user_id):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        user = get_object_or_404(User, id=user_id)

        following = user.following.all()

        writer = csv.DictWriter(response, [])

        formatted_header = ['username'] + ['type']

        writer.fieldnames = formatted_header
        writer.writeheader()

        for user in following:
            row = {'username': user.username, 'type': user.type}

            writer.writerow(row)

        return response


class ReportViewNotification(View):

    def get(self, request, user_id):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        user = get_object_or_404(User, id=user_id)

        notifications = Notification.objects.filter(user_id=user_id)

        writer = csv.DictWriter(response, [])

        formatted_header = ['Notification']

        writer.fieldnames = formatted_header
        writer.writeheader()

        for message in notifications:
            row = {'Notification': message.text}

            writer.writerow(row)

        return response
