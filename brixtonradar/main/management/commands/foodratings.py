from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
import json
from helpers import geo
from main import models
import time
from datetime import datetime

class Command(BaseCommand):


    def handle(self, *args, **options):
        print "Getting JSON"

        now = datetime.now()
        data = json.load(urllib.urlopen('http://ratings.food.gov.uk/enhanced-search/en-GB/%5E/sw9/desc_rating/0/522/%5E/1/1/500/json'))
        if data and data['FHRSEstablishment'].get('EstablishmentCollection'):
            for venue in data['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail']:
                if venue['RatingDate'].find(now.strftime('%Y')) > -1:
                    rating_date = datetime.strptime(venue['RatingDate'], '%Y-%m-%d')
                    days_since_rating = (now - rating_date).days

                    latlng = {'lat': float(venue['Geocode']['Latitude']), 'lng': float(venue['Geocode']['Longitude'])}
                    if geo.is_local(latlng):
                        #has it been added before?
                        venue_url = 'http://ratings.food.gov.uk/business/en-GB/%s' % venue['FHRSID']
                        guid = venue_url + venue['RatingDate']
                        existing_events = models.Event.objects.filter(guid=guid)
                        if len(existing_events) == 0:

                            event = models.Event()
                            event.message = "%s was inspected for food hygiene. It got %s out of 5." % (venue['BusinessName'], venue['RatingValue'])
                            event.event_type = models.EventType.objects.get(short_name='foodratings')
                            event.info_link = venue_url
                            event.guid = guid
                            event.occured = rating_date
                            event.address = "%s, %s %s" % (venue['AddressLine1'], venue['AddressLine2'], venue['PostCode'])
                            event.lng =  latlng['lng']
                            event.lat = latlng['lat']
                            event.data = {'business_name': venue['BusinessName'], 'business_type': venue['BusinessType'], 'rating_value': int(venue['RatingValue'])}
                            event.save()
                            print "saved %s " % event.message




        # for application in data['planning_applications']:
        #     existing_events = models.Event.objects.filter(guid=application['url'])
        #     if len(existing_events) == 0:
        #          if geo.is_local({'lat': application['lat'], 'lng': application['lng']}):
        #             address = application['address']
        #             building_name =  address.split(' London')[0]
        #             action =  self.guess_type(application['description'])
        #             agent = self.get_agent(application)

        #             message = "%s want %s %s" % (agent, action, building_name)

        #             event = models.Event()
        #             event.message = message
        #             event.event_type = models.EventType.objects.get(short_name='planning')
        #             event.info_link = application['url']
        #             event.guid = application['url']
        #             event.address = address
        #             event.lng =  application['lng']
        #             event.lat = application['lat']
        #             event.data = {'agent': agent, 'description': application['description'], 'application type': application['application_type']}
        #             event.save()
