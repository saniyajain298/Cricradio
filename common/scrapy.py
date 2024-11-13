import requests
from bs4 import BeautifulSoup

from .models import Series, Team


# Assuming this is the constants file with your constants
class Constants:
    TEAM_SCRAP_LIST_API_URL = 'https://crex.live/fixtures/team-list'  # Replace with the actual URL
    SERIES_SCRAP_LIST_API_URL = 'https://crex.live/fixtures/series-list'

def getTeamListScrappingJob():
    url = Constants.TEAM_SCRAP_LIST_API_URL

    try:
        # Perform the GET request with the specified URL and headers
        response = requests.get(url)

        teamsName = extractTeamFromHTMLData(response.text)
        teamId = getFixtureTeamData()
        teams = convertToObject(teamsName, teamId)

        return teams

    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error: {e}")


def extractTeamFromHTMLData(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all divs with the class 'team-name'
    team_names = [div.get_text(strip=True) for div in soup.find_all("div", class_="team-name")]

    return team_names


def getFixtureTeamData():
    url = "https://crickapi.com/fixture/getFixture"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.6",
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA",
        "content-type": "application/json",
        "origin": "https://crex.live",
        "priority": "u=1, i",
        "referer": "https://crex.live/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Brave\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1"
    }

    data = {
        "type": "",
        "page": 0,
        "wise": "3",
        "lang": "en"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


def convertToObject(teamsName, teamId):
    # Assuming teamsName is a list of team names and teamId is a dictionary of team IDs
    result = []

    # Make sure both lists have the same length
    if len(teamsName) == len(teamId):
        # Iterate through the teams and their IDs
        for i, name in enumerate(teamsName):
            # Use the index of the teamName list to get the corresponding ID from teamId
            team_id = list(teamId.values())[i]  # Extract the team ID by index
            result.append({
                "teamsName": name,
                "teamId": team_id
            })
    else:
        return {"error": "The lengths of teamsName and teamId don't match."}

    return result



# series
def getSeriesListScrappingJob():
    url = Constants.SERIES_SCRAP_LIST_API_URL

    try:
        # Perform the GET request with the specified URL and headers
        response = requests.get(url)

        seriesName = extractSeriesFromHTMLData(response.text)
        seriesObj = getFixtureSeriesData()

        series = convertToSeriesObject(seriesName, seriesObj)
        return series

    except requests.exceptions.RequestException as e:
        # Handle request errors
        print(f"Error: {e}")


def extractSeriesFromHTMLData(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all divs with the class 'team-name'
    series_names = [div.get_text(strip=True) for div in soup.find_all("div", class_="series-name")]

    return series_names


def getFixtureSeriesData():
    url = "https://crickapi.com/fixture/getFixture"
    headers = {
        "sec-ch-ua-platform": "\"Windows\"",
        "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA",
        "Referer": "https://crex.live/",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Brave\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
    }
    data = {
        "type": "0",
        "page": 0,
        "wise": "2",
        "lang": "en"
    }


    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        series_data = []

        for key in response.json():
            series_data.extend(response.json()[key])
        return series_data

    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}


def convertToSeriesObject(seriesName, seriesObj):

    # Assuming teamsName is a list of team names and teamId is a dictionary of team IDs
    result = []

    if len(seriesName) == len(seriesObj):
        # Iterate through the series names and their corresponding series IDs
        for i, name in enumerate(seriesName):
            series_data = seriesObj[i]

            # Assuming 'host_team' is a unique identifier of the Team model
            try:
                # Fetch the corresponding Team object using host_team's unique id
                host_team = Team.objects.get(team_unique_id =series_data['host_team'])
            except Series.DoesNotExist:
                print(f"Team with unique ID {series_data['host_team']} not found.")
                continue  # Skip to the next iteration if the team is not found

            # Create Series object and populate its fields
            series = Series(
                unique_series_id=str(series_data['sf']),  # Unique ID from the series data
                series_name=name,  # The series name from seriesName list
                host_team=host_team,  # Foreign Key to the Team model
                type=series_data['t'],  # Type from the series data
                status=series_data['st'],  # Status from the series data
                month_year=series_data['month_year'],  # Month and year from the series data
                tp=series_data['tp']  # Time period from the series data
            )

            # Save the Series object to the database
            series.save()
            result.append(series)  # Append the created series to the result list

    else:
        print("Error: seriesName and seriesId lists do not have the same length.")

    return result  # Return the list of created Series objects
