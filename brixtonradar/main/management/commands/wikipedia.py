from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
from main import models
from datetime import date, timedelta, datetime
import json
import feedparser
import dateutil.parser
from helpers import geo

class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'http://api.wikilocation.org/articles?lat=%s&lng=%s&limit=25&format=json' % ('51.46238', '-0.1145')
        data = json.load(urllib.urlopen(url))
        for article in data['articles']:
            id = article['id']
            title = article['title']

            #check if local
            if geo.is_local({'lat': float(article['lat']), 'lng': float(article['lng'])}):

                #rss history
                feed_url = 'http://en.wikipedia.org/w/index.php?curid=%s&action=history&feed=atom' % id
                rss = feedparser.parse(feed_url)
                for entry in rss.entries:
                    datetime_updated = dateutil.parser.parse(entry['updated'])
                    split = entry['title'].split(':')
                    change_title = split[len(split) -1]
                    message =  "The Wikipedia article about %s was edited - %s" % (title, change_title)

                    save = False

                    #check if recent (last few days)
                    yesterday = date.today() - timedelta(3)
                    save = (datetime_updated.date() > yesterday)

                    if save:
                        print "save"
                        event = models.Event()
                        event.message = message
                        event.event_type = models.EventType.objects.get(short_name='wikipedia')
                        event.info_link = entry['links'][0]['href']
                        event.guid = entry['links'][0]['href']
                        event.address = ''
                        event.lng =  article['lng']
                        event.lat = article['lat']
                        event.data = article
                        event.save()


