from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
from main import models
from datetime import datetime
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'http://api.wikilocation.org/articles?lat=51.500688&lng=-0.124411&limit=1&format=json' %s ()

        data = json.load(urllib.urlopen(url))
