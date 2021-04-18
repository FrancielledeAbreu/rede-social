from django.core.management.base import BaseCommand
from accounts.models import User
from posts.models import Post
import csv


class Command(BaseCommand):
    help = 'Populates the database from the information in the specified csv file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str,
                            help='Indicates the path .csv file')

    def handle(self, *args, **kwargs):
        csvfile = kwargs['csvfile']
        with open(csvfile) as file:
            timeline = csv.DictReader(file, delimiter=";")

            for item in timeline:
                user = User.objects.get_or_create(username=item["USERNAME"],
                                                  type=item["TYPE"],
                                                  password=str(item['PASSWORD']))[0]

                Post.objects.get_or_create(title=item["TITLE"],
                                           description=item["DESCRIPTION"],
                                           image=item["IMAGE"],
                                           private=item["PRIVATE"],
                                           author=user)[0]
