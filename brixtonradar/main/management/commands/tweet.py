from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse
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
            url = '%s/%s' % (settings.BASE_URL, reverse('event', args=[alert.event.pk]))
            status = api.PostUpdate(alert.event.message + ' ' + url + " #brixton", latitude=alert.event.lat, longitude=alert.event.lng)
            print "Tweet sent %s" % alert.event.message
            time.sleep(settings.SLEEP_BETWEEN_TWEETS)
            print "Waiting before sending next tweet"

        #delete them as have been sent
        alerts.delete()

