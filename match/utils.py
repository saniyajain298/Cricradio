from datetime import datetime, timezone

from . import call_match_api
from .models import Match
from .scrapy import getMatchListScrappingJob
from django.core.exceptions import ObjectDoesNotExist
from common.models import Team, Series
from django.db import transaction



def update_or_create_match():
    """
    Function to update or create a match record based on the provided data.
    """
    created_matches = []  # Initialize created_matches list to track created matches
    try:
        # Access the entire arrays d1_data and d2_data
        d1_data, d2_data = getMatchListScrappingJob()

        if not d1_data or not d2_data:
            raise ValueError("Match data is missing")

        # Iterate through both d1_data and d2_data
        for i in range(len(d1_data)):
            d1 = d1_data[i]
            d2 = d2_data[i] if i < len(d2_data) else None  # Ensure d2 has the corresponding element

            if not d2:
                print(f"Warning: Missing d2 data for match {i}")
                continue

            # Extract and convert match date
            match_date = datetime.strptime(d1['match_date'], '%a, %d %b %Y').date()

            # Match time: if 'No time found' is present, set as None, else convert from milliseconds
            match_time = None
            if 't' in d2 and d2['t']:
                match_time = datetime.fromtimestamp(d2['t'] / 1000, tz=timezone.utc)
            else:
                match_time = datetime.now(tz=timezone.utc)

            # Match status
            status = d2['st']
            team1_unique_id = d2['t1f']
            team2_unique_id = d2['t2f']

            # Ensure teams exist
            try:
                team1 = Team.objects.get(team_unique_id=team1_unique_id)
                team2 = Team.objects.get(team_unique_id=team2_unique_id)
            except Team.DoesNotExist as e:
                print(f"Error: {e}")
                continue

            # Get or create series
            series = None
            try:

                if d1['match_type'] == 'No match type found':
                    raise ValueError("No match type found in the data")

                series = Series.objects.get(unique_series_id=d1['match_type'])
                host_team = team1


            except Series.DoesNotExist:
                print("Series not found, attempting to create new series.")
                try:
                    host_team = Team.objects.get(team_unique_id=team1_unique_id)
                    series = Series.objects.create(
                        unique_series_id=d1['match_type'],
                        series_name=f"Series {d1['match_type']}",
                        host_team=host_team,
                        type=0,  # Modify based on your logic
                        status=d1['match_status'],
                        month_year=match_date.strftime('%b %Y'),
                        tp=None
                    )
                    print("Series created:", series)
                except Team.DoesNotExist:
                    print(f"Error: Team {team1_unique_id} not found for series creation")
                    continue
            except ValueError as ve:
                print(f"Error: {ve}")
                continue

                # Extract other match details
            match_link = d1['match_link']
            start_time = d2['ssd']
            end_time = d2['sed']
            print('checking before',d2)
            match_unique_id = d2['mf'] or d2['nf']


            # Use transaction to ensure atomic operations
            with transaction.atomic():
                print("noew Create match is", match_unique_id)
                match, created = Match.objects.update_or_create(
                    match_unique_id=match_unique_id,
                    defaults={
                        'match_date': match_date,
                        'team1_unique_id': team1,
                        'team2_unique_id': team2,
                        'match_time': match_time,
                        'series': series,
                        'status': status,
                        'host_team_id': host_team,
                        'match_link': match_link,
                        'start_time': start_time,
                        'end_time': end_time
                    }
                )

                # if created:
                created_matches.append(match)
                print(f"Created match {match} for match {i}")

                # Check if the match has already started
                if match.match_time <= datetime.now(timezone.utc):
                    # Match has started, call API now and schedule subsequent calls
                    print(f"Match {match_unique_id} has started, calling API now.")
                    call_match_api.apply_async(args=[match_unique_id], countdown=60)  # First call after 60 seconds
                    # If you want to schedule subsequent calls every minute
                    call_match_api.apply_async(args=[match_unique_id], countdown=60 * 2)  # Subsequent calls every minute
                else:
                    # Match hasn't started, schedule API call when it starts
                    time_until_start = (match.match_time - datetime.now(timezone.utc)).total_seconds()
                    if time_until_start > 0:
                        print(f"Match {match_unique_id} hasn't started yettt. Scheduling first API call.")
                        # Schedule the first call for the start time, then subsequent calls every minute
                        # call_match_api.apply_async(args=[match_unique_id], countdown=time_until_start)  # Call when match starts
                        # call_match_api.apply_async(args=[match_unique_id], countdown=time_until_start + 60)  # First call after match starts
                        call_match_api(match_unique_id)
                # else:
                #     print(f"Updated match {match} for match {i}")

        return created_matches if created_matches else None

    except ObjectDoesNotExist as e:
        print(f"Error: {str(e)}")
        return None
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None
