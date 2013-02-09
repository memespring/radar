from django.core.management.base import BaseCommand, CommandError
import twitter
import settings

class Command(BaseCommand):

    def handle(self, *args, **options):
        print "Singing in to Twitter"
        api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
consumer_secret=settings.TWITTER_CONSUMER_SECRET, access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY, access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)

        print "Posting tweet"
        status = api.PostUpdate('yet another test 1')

        print "Tweet was: %s" % status
