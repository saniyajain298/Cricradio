import requests
from django.core.management.base import BaseCommand
from sqlparse.utils import consume

from ...models import Team, Series
from ...scrapy import getTeamListScrappingJob, getSeriesListScrappingJob


class Command(BaseCommand):
    help = 'Fetch team data from a scraping API and update the database'

    def handle(self, *args, **kwargs):


        try:
            # Call the API to get the team data
            series_data = getSeriesListScrappingJob()  # Your scraping job that returns the team data

            print(series_data)



        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error calling the scraping API: {e}'))
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f'Error parsing JSON response: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Unexpected error: {e}'))