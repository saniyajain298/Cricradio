import requests
from bs4 import BeautifulSoup




# Assuming this is the constants file with your constants
class Constants:
    MATCH_LIST_API_URL = 'https://crex.live/fixtures/match-list'  # Replace with the actual URL


def getMatchListScrappingJob():
    url = Constants.MATCH_LIST_API_URL

    # Set the headers exactly as in the curl request
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.6",
        "cookie": "selectedTheme=light; systemThemeEnabled=yes; isSelectNumProgress=0; isSelectPerProgress=1; isMidOvProShow=0; isFullOvProShow=0; system-theme=light",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
    }

    try:
        # Perform the GET request with the specified URL and headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for 4xx/5xx responses

        # Print the response content (for debugging)
        print("Response Content:")
        # print(response.text)
        matches = extractMatchInfoFromHTMLData(response.text)
        print("matches ",matches)
        match_fixtuer_data =getFixtureMatchListData()
        print("matchFixtuerData ", match_fixtuer_data)
        return matches, match_fixtuer_data

    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error: {e}")


def extractMatchInfoFromHTMLData(html_content):
    # print("extracted data :", html_content)
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all sections with match dates and associated matches
    match_date_sections = soup.find_all('div', class_='date')

    # Initialize a list to store match details
    matches = []

    for date_section in match_date_sections:
        # Extract the date (text inside the inner div)
        match_date = date_section.find('div').text.strip() if date_section.find('div') else 'No date found'

        # Find the match container associated with this date
        matches_container = date_section.find_next_sibling('div', class_='matches-card-space')

        if matches_container:
            # Find all individual match cards under this date
            match_cards = matches_container.find_all('li', class_='match-card-container')

            for card in match_cards:
                # Extract match link
                link_tag = card.find('a', class_='match-card-wrapper')
                match_link = link_tag['href'] if link_tag else None

                # Extract team names (Ensure fallback in case teams are not found)
                teams = card.find_all('span', class_='team-name')
                team1_name = teams[0].text.strip() if len(teams) > 0 else 'No team found'
                team2_name = teams[1].text.strip() if len(teams) > 1 else 'No team found'

                # Extract match time
                time_div = card.find('div', class_='start-text')
                match_time = time_div.text.strip() if time_div else 'No time found'

                # Extract match type
                match_type_div = card.find('p', class_='time')
                match_type = match_type_div.text.strip() if match_type_div else 'No match type found'


                # Extract match status (e.g., "Match Abandoned", "Live", etc.)
                status_div = card.find('div', class_='result')
                match_status = 'No status found'
                winning_team = None

                # Check for "Live" status
                live_tag = card.find('span', class_='liveTag')
                if live_tag:
                    match_status = 'Live'

                # If there is a result (e.g., "Match Abandoned" or "Won")
                elif status_div:
                    result_span = status_div.find_all('span')
                    if result_span:
                        match_status = result_span[1].text.strip()  # Extract match status
                        if "Won" in match_status:
                            winning_team = match_status.split("Won")[-1].strip()

                # Store the match details in the list
                match_details = {
                    'match_date': match_date,
                    'team1': team1_name,
                    'team2': team2_name,
                    'match_time': match_time,
                    'match_type': match_type,
                    'match_status': match_status,
                    'winning_team': winning_team,
                    'match_link': 'https://crex.live/'+ match_link
                }

                matches.append(match_details)
    # Print the extracted match details
    # print(matches)
    # for match in matches:
    #     print(match)
    return matches


def getFixtureMatchListData():

    url = "https://crickapi.com/fixture/getFixture"
    # Define the headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.6",
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA",
        "content-type": "application/json",
        "origin": "https://crex.live",
        "priority": "u=1, i",
        "referer": "https://crex.live/",
        "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    # Define the data
    data = {
        "type": "0",
        "page": 0,
        "wise": "1",
        "lang": "en",
        "formatType": "",
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print(response.json())  # Print the response JSON data
        return response.json()
    else:
        print(f"Error: {response.status_code}")

# def extractMatchInfoFromHTMLData():
#
#     url = "https://crickapi.com/fixture/getFixture"
#     # Define the headers
#     headers = {
#         "accept": "application/json, text/plain, */*",
#         "accept-language": "en-US,en;q=0.6",
#         "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA",
#         "content-type": "application/json",
#         "origin": "https://crex.live",
#         "priority": "u=1, i",
#         "referer": "https://crex.live/",
#         "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": '"Windows"',
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "cross-site",
#         "sec-gpc": "1",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
#     }
#
#     # Define the data
#     data = {
#         "type": "0",
#         "page": 0,
#         "wise": "1",
#         "lang": "en",
#         "formatType": "",
#     }
#
#     # Make the POST request
#     response = requests.post(url, headers=headers, json=data)
#
#     # Check if the request was successful
#     if response.status_code == 200:
#         print(response.json())  # Print the response JSON data
#         return response.json()
#     else:
#         print(f"Error: {response.status_code}")


def getLiveData(match_id):

    # API URL
    url = f"https://api-v1.com/v10/sV3.php?key={match_id}"
    print('foivjovgoifd', match_id)
    # Headers for the request
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.6",
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA",
        "origin": "https://crex.live",
        "priority": "u=1, i",
        "referer": "https://crex.live/",
        "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    # Making the GET request
    response = requests.get(url, headers=headers)

    # Checking the response
    if response.status_code == 200:
        print("Response received successfully")
        data = response.json()
        print(data)
        updateMatchLiveData(data, match_id)
    else:
        print(f"Request failed with status code {response.status_code}")


def updateMatchLiveData(data, match_id):
    from .models import MatchData
    from .models import Match
    match = Match.objects.get(match_unique_id=match_id)
    match_data, created = MatchData.objects.update_or_create(
        match_id=match,
        defaults={
            'match_name': data.get('F', None),
            'balls_in_each_over': data.get('A', None),
            'bowling_status': data.get('B', None),
            'match_duration': data.get('D', None),
            'team_info': data.get('L', None),
            'match_ip_addresses': data.get('M', None),
            'run_rate': data.get('R', None),
            'match_ips_or_stats': data.get('S', None),
            'match_status': data.get('Z', None),
            'player_performance_code': data.get('ats', None),
            'player_score': data.get('b', None),
            'bowling_type': data.get('g', None),
            'event_code': data.get('f', None),
            'event_data': data.get('q', None),
            'match_code': data.get('p', None),
            'team_or_player_status': data.get('s', None),
            'match_score': data.get('i', None),
            'runs_in_current_over': data.get('j', None),
            'runs_required': data.get('l', None),
            'match_event_time': data.get('o', None)
        }
    )

    return match_data
