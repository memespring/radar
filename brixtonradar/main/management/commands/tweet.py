from django.core.management.base import BaseCommand, CommandError
import twitter
import settings
import time
from main import models

class Command(BaseCommand):

    def handle(self, *args, **options):

        print "Singing in to Twitter"
        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
consumer_secret=settings.TWITTER_CONSUMER_SECRET, access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY, access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

        print "Get any new alerts"
        alerts = models.Alert.objects.all()

        for alert in alerts:
            print "Posting tweet"
            status = api.PostUpdate(alert.event.message, latitude=alert.event.lat, longitude=alert.event.lng)
            print "Tweet sent %s" % alert.event.message
            time.sleep(settings.SLEEP_BETWEEN_TWEETS)
            print "Waiting before sending next tweet"

        #delete them as have been sent
        alerts.delete()

