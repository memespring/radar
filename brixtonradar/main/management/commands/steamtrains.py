from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
from main import models
import BeautifulSoup
from datetime import datetime

#beholder_row_BRX
class Command(BaseCommand):

    def handle(self, *args, **options):
        print "Scraping"
        now = datetime.now()
        url = 'http://www.beholder.co.uk/steam/'
        html = urllib.urlopen(url)
        page = BeautifulSoup.BeautifulSoup(html)
        #brixton_row = page.find('tr', {'id': 'beholder_row_BRX'})
        #value = brixton_row.findAll('td')[1].string.strip()
        brixton_row = page.find('tr', {'id': 'beholder_row_LAN'})
        values = brixton_row.findAll('td')[1].findChildren()
        if values == []:
            print "NO TRAINS :("
        else:
            print "TRAINS!"

            # get the time
            times = ''
            for value in values:
                times =  value.text + ' '

            #try and get details of train
            html = urllib.urlopen(values[0]['href'])
            page = BeautifulSoup.BeautifulSoup(html)
            service_name = page.find('table').find('td').find('font').find('b').text.title()

            # work out guid and see if already saved
            guid = "%s/%s" % (url, now.strftime('%Y-%m-%d:%H'))
            existing_events = models.Event.objects.filter(guid=guid)

            if len(existing_events) == 0:
                event = models.Event()
                event.message = "%s will be steaming through Brixton Station at %s" % (service_name, times)
                event.event_type = models.EventType.objects.get(short_name='steamtrain')
                event.info_link = url
                event.guid = guid
                event.address = "32 Brixton Station Road, Brixton, London, SW9 8PE"
                event.lng = -0.11399
                event.lat = 51.46327
                event.data = {'service_name': service_name, 'time': times}
                event.save()
                print "saved %s " % event.message




