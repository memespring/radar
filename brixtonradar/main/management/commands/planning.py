from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
import json
from helpers import geo
from main import models

class Command(BaseCommand):

    def get_agent(self, application):
        data = json.load(urllib.urlopen(application['openlylocal_url'] + '.json'))
        return  data['planning_application']['other_attributes']['agent_company_name']

    def guess_type(self, text):
        haystack = text.lower()
        result = "applied for planning permission at"
        if haystack.find('change of use') > -1:
            result = "want to change the use of"
        elif haystack.find('demolition') > -1:
            result = "applied for a demolition at"
        elif haystack.find('erect') > -1:
            result = "want to build something at"

        return result

    def handle(self, *args, **options):
        print "Getting JSON"
        data = json.load(urllib.urlopen('http://openlylocal.com/councils/12/planning_applications.json'))
        for application in data['planning_applications']:
            existing_events = models.Event.objects.filter(guid=application['url'])
            if len(existing_events) == 0:
                 if geo.is_local({'lat': application['lat'], 'lng': application['lng']}):
                    address = application['address']
                    building_name =  address.split(' London')[0]
                    action =  self.guess_type(application['description'])
                    agent = self.get_agent(application)

                    message = "%s %s %s" % (agent, action, building_name)

                    event = models.Event()
                    event.message = message
                    event.event_type = models.EventType.objects.get(short_name='planning')
                    event.info_link = application['url']
                    event.guid = application['url']
                    event.address = address
                    event.lng =  application['lng']
                    event.lat = application['lat']
                    event.data = {'agent': agent, 'description': application['description'], 'application type': application['application_type']}
                    event.save()
