from django.core.management.base import BaseCommand, CommandError
import settings
import urllib
import BeautifulSoup
from helpers import geo
from main import models

class Command(BaseCommand):

    def humanize(self, text):

        text = text.replace('review of premises licence', "is having it's licence reviewed")
        text = text.replace('new premises licence', 'applied for a licence')
        text = text.replace('time limited premises licence', 'applied for a time limited licence')

        return text

    def handle(self, *args, **options):
        print "Starting to scrape"
        html = urllib.urlopen('http://www.lambeth.gov.uk/Services/Business/LicencesStreetTrading/AlcoholEntertainmentLateNightRefreshment/CurrentApplications.htm')
        page = BeautifulSoup.BeautifulSoup(html)

        #find rows
        for infobox in page.findAll('div', {'class': 'infoBox'}):
            for list_item in infobox.findAll('li'):

                address = list_item.find('a').string
                details = list_item.contents[4].split('last date for representations')[0].rstrip(', ').rstrip(' - ')
                application_pdf_link = 'http://www.lambeth.gov.uk/' + list_item.find('a')['href']

                postcode = geo.extract_gb_postcode(address)
                latlng = geo.postcode_latlng(postcode)

                existing_events = models.Event.objects.filter(guid=application_pdf_link)
                if len(existing_events) == 0:
                    if geo.is_local(latlng):

                        applicant = address.split(',')[0]
                        application_type = details.replace('Application for ', '')
                        message = "%s %s " % (applicant, application_type)

                        event = models.Event()
                        event.message = self.humanize(message)
                        event.event_type = models.EventType.objects.get(short_name='licence')
                        event.info_link = application_pdf_link
                        event.guid = application_pdf_link
                        event.address = address
                        event.lng = latlng['lng']
                        event.lat = latlng['lat']
                        event.data = {'applicant': applicant, 'application_type': application_type}
                        event.save()
