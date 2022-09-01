import random
from random import randint
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from myauth.models import UserModel
from mycontent.models import PostModel, CommentModel


class Command(BaseCommand):
    help = "Command to populate db with dummy data"

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        try:
            # req = requests.get('https://parade.com/1032891/marynliles/funny-usernames/')
            # soup = BeautifulSoup(req.content, "lxml")
            # var = soup.findAll("div", attrs={"class": "m-detail--body"})
            # for x in var:
            #     x.findAll('<p>')
            #     print(x)
            total = kwargs['total']
            for i in total:
                user = User.objects.create_user(username=f'testusername{i}', password=f'{i}')
                myuser = UserModel.objects.create(user=user
                                                  , age=randint(10, 30)
                                                  , gender=random.choice(['male', 'female']))
                post = PostModel.objects.create(title=f'testposttitle{i}'
                                                , body=f'testpostbody{i}'
                                                , user=user)
                comment = CommentModel.objects.create(cbody=f'testcommentbody{i}'
                                                      , user=user)
            print('Command is executed')
        except Exception as e:
            raise CommandError(e)
