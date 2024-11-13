import requests
from django.core.management.base import BaseCommand
from sqlparse.utils import consume

from ...models import Team
from ...scrapy import getTeamListScrappingJob


class Command(BaseCommand):
    help = 'Fetch team data from a scraping API and update the database'

    def handle(self, *args, **kwargs):


        try:
            # Call the API to get the team data
            teams_data = getTeamListScrappingJob()  # Your scraping job that returns the team data

            # Inside the loop for processing teams:
            for team_data in teams_data:
                team_name = team_data.get('teamsName')
                team_unique_id = team_data.get('teamId')

                if not team_name or not team_unique_id:
                    self.stderr.write(self.style.ERROR(f'Missing team data: {team_data}'))
                    continue

                # Update or create logic:
                team, created = Team.objects.update_or_create(
                    team_unique_id=team_unique_id,
                    defaults={'team_name': team_name}
                )


        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Error calling the scraping API: {e}'))
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f'Error parsing JSON response: {e}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Unexpected error: {e}'))