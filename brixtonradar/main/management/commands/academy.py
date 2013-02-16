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
        url = 'http://www.o2academybrixton.co.uk/?t=list'
        html = urllib.urlopen(url)
        page = BeautifulSoup.BeautifulSoup(html)
        rows = page.find('div', {'class': 'eventViewList'}).findAll('tr')
        for row in rows:

            #date and time
            datetime_td = row.find('td', {'class': 'eventViewListDate'})
            if datetime_td:
                datetime_scraped = ''
                for div in datetime_td.findAll('div'):
                    datetime_scraped = datetime_scraped + ' ' + div.text
                event_datetime = datetime.strptime(datetime_scraped, " %d %b '%y-%a %I.%M%p" )

                # is today?
                if (event_datetime -  datetime.now()).days == 0:

                    #artist
                    artist_td = row.find('td', {'class': 'eventViewListName'})
                    if artist_td:
                        artist_name = artist_td.find('a',{'class': 'main'}).text
                        url = artist_td.find('a',{'class': 'main'})['href']
                        #guid is artist, month year. i.e. dont save multiple night runs
                        guid = artist_name.replace(' ', '') + event_datetime.strftime('%m%y')

                        #Is sold out?
                        links_td = row.find('td', {'class': 'eventViewListLinks'})
                        status_div = links_td.find('div', {'class': 'icon'})
                        if status_div and status_div.text == 'Sold Out':

                            existing_events = models.Event.objects.filter(guid=guid)

                            if len(existing_events) == 0:
                                event = models.Event()
                                event.message = '"Buy/sell tickets for %s"' % artist_name
                                event.event_type = models.EventType.objects.get(short_name='academy')
                                event.info_link = url
                                event.guid = guid
                                event.occured = event_datetime
                                event.address = "Brixton Academy, 211 Stockwell Road, SW9 9SL"
                                event.lng = -0.11497
                                event.lat = 51.46526
                                event.data = {'artist_name': artist_name}
                                event.save()
                                print "saved %s " % event.message








