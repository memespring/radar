from django.core.management.base import BaseCommand, CommandError
import twitter

class Command(BaseCommand):

    def handle(self, *args, **options):
        print "Singing in to Twitter"
        api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
consumer_secret=TWITTER_CONSUMER_SECRET, access_token_key=TWITTER_ACCESS_TOKEN_KEY, access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

        print "Posting tweet"
        status = api.PostUpdate('another test')

        print "Tweet was: %s" % status
