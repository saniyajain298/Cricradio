# Cricket Data Scraping and API Integration System

## Tech Stack:
- **Backend**: Django
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Containerization**: Docker

## Project Setup

### Run the Project using Docker

To get started, follow the steps below:

1. **Build and Start the Containers**  
   Build and start the containers with the following command:

   ```bash
   docker-compose up --build 
      
2. **Database Migration**  
  In case the tables are not migrated automatically, you can manually run the migration command using the following:

  ```bash
  docker-compose run web python manage.py migrate
  ```
        
## Available APIs

1. **Get List of Teams**
   - Endpoint: `GET http://127.0.0.1:8000/common/team`
   - Description: Retrieves a list of teams stored in the database.

2. **Get List of Matches**
   - Endpoint: `GET http://127.0.0.1:8000/match/matches`
   - Description: Retrieves a list of all available matches.

3. **Get Live Match Data**
   - Endpoint: `GET http://127.0.0.1:8000/match/matchdata/?char=<match_id>`
   - Description: Retrieves live data of a specific match using its `match_id`.

## Logic and Code Explanation

The project works by integrating data from APIs and web scraping to get information about teams, matches, and series. Here's a step-by-step breakdown of the logic:

### 1. **Team Data Collection**
   To avoid repeatedly scraping team data, an API call is used to fetch the list of teams, which is stored in the database for later use. Initially, this data is scraped from the web and stored in the database.

   - **API Used**: `https://crickapi.com/fixture/getFixture`
   - **Data Combined**: Web scraping results and the API response are combined to match team IDs with team names.

### 2. **Series Data Collection**
   Similar to the team data, series data is fetched through an API, and scraped data is combined to ensure that series names and their IDs are correctly mapped.

   - **API Used**: `https://crickapi.com/fixture/getFixture`
   - **Data Combined**: Series data from the API and web scraping is merged for better clarity.

### 3. **Match Data and IDs**
   To access match data dynamically, the match list is obtained through both scraping and an API. The `match_id` in the match API response is then used to match up with the team and series data for each match.

   - **APIs Used**:
     - `https://crex.live/fixtures/match-list` for the match list.
     - `https://oc.crickapi.com/commentary/getBallFeeds` for live match data.
   
   The match ID is used to gather live data, so scraping is only done once to collect initial data, and subsequent data retrievals are done through the API to avoid unnecessary scraping.

### 4. **Data Update with Celery**
   A Celery scheduler runs periodically to scrape and update the team and series data. The dynamic data is fetched in intervals and updated in the database to ensure that the information is always up-to-date.

### 5. **Scraping and API Call Integration**
   Scraping data is performed once during startup, after which APIs are used to fetch real-time data like match scores, commentary, etc. This reduces the need for repeated scraping, improving system efficiency.

## API Calls Used in the System

Below are the `curl` commands used for retrieving the relevant data:

- **Match List AP**:
  ```bash
  curl "https://crex.live/fixtures/match-list" \
    -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8" \
    -H "accept-language: en-US,en;q=0.6" \
    -H "cache-control: no-cache" \
    -H "cookie: isSelectNumProgress=0; isSelectPerProgress=1; isMidOvProShow=0; isFullOvProShow=0; systemThemeEnabled=no; selectedTheme=light; system-theme=light" \
    -H "pragma: no-cache" \
    -H "priority: u=0, i" \
    -H "sec-ch-ua: \"Chromium\";v=\"130\", \"Brave\";v=\"130\", \"Not?A_Brand\";v=\"99\"" \
    -H "sec-ch-ua-mobile: ?0" \
    -H "sec-ch-ua-platform: \"Windows\"" \
    -H "sec-fetch-dest: document" \
    -H "sec-fetch-mode: navigate" \
    -H "sec-fetch-site: same-origin" \
    -H "sec-fetch-user: ?1" \
    -H "sec-gpc: 1" \
    -H "upgrade-insecure-requests: 1" \
    -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


- **Teams List AP**:
  ```bash
  curl "https://crickapi.com/fixture/getFixture" 
  -H "accept: application/json, text/plain, */*" 
  -H "accept-language: en-US,en;q=0.6" 
  -H "authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA" 
  -H "content-type: application/json" 
  -H "origin: https://crex.live" 
  -H "priority: u=1, i" 
  -H "referer: https://crex.live/" 
  -H "sec-ch-ua: "Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"" 
  -H "sec-ch-ua-mobile: ?0" 
  -H "sec-ch-ua-platform: "Windows"" 
  -H "sec-fetch-dest: empty" 
  -H "sec-fetch-mode: cors" 
  -H "sec-fetch-site: cross-site" 
  -H "sec-gpc: 1" 
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" 
  --data-raw "{\"type\":\"\",\"page\":0,\"wise\":\"3\",\"lang\":\"en\"}"

- **Series List AP**:
  ```bash
  curl "https://crickapi.com/fixture/getFixture" 
  -H "accept: application/json, text/plain, */*" 
  -H "accept-language: en-US,en;q=0.6" 
  -H "authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImV4cGlyZXNJbiI6IjM2NWQifQ.eyJ0aW1lIjoxNjYwMDQ2NjIwMDAwfQ.bTEmMWlR7hLRUHxPPq6-1TP7cuuW7m6sZ9jcdbYzLRA" 
  -H "content-type: application/json" 
  -H "origin: https://crex.live" 
  -H "priority: u=1, i" 
  -H "referer: https://crex.live/" 
  -H "sec-ch-ua: "Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"" 
  -H "sec-ch-ua-mobile: ?0" 
  -H "sec-ch-ua-platform: "Windows"" 
  -H "sec-fetch-dest: empty" 
  -H "sec-fetch-mode: cors" 
  -H "sec-fetch-site: cross-site" 
  -H "sec-gpc: 1" 
  -H "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" 
  --data-raw "{\"type\":\"0\",\"page\":0,\"wise\":\"2\",\"lang\":\"en\"}"

## Future Improvements

- **Error Handling:**
  The current implementation does not handle all edge cases. More comprehensive error handling and logging would be beneficial, especially for API failures or data extraction errors.

- **Efficiency:**
  The system could benefit from optimizations in resource usage. Implementing a caching mechanism and optimizing data structures for storage could improve efficiency.

- **Time Optimization:**
  The process time for data fetching and processing could be further reduced by using asynchronous processing or parallel tasks.

## Evaluation Criteria

1. **Handling of Edge Cases:** The system should cover all edge cases and handle errors effectively.
2. **Organization and Relevance of Data:** Data should be semantically relevant and organized in a logical manner.
3. **Code Clarity and Organization:** The code should be structured, readable, and easy to understand.
4. **Resource Efficiency:** The system should optimize resource consumption.
5. **Time to Results:** The system should minimize response time and process data efficiently.

## Possible Follow-Up Questions

1. **Why did you choose this specific scraping approach?**
   The scraping approach was chosen to avoid repetitive data extraction and to rely on API responses for dynamic data, ensuring accuracy and minimizing server load.

2. **How can we optimize resource usage further?**
   By adding a caching layer to store frequently accessed data and reduce repeated API calls and database queries.

3. **Can the time consumption be reduced?**
   Yes, by using asynchronous processing, reducing redundant operations, and optimizing the task scheduling logic.

4. **What changes would you make if given more time?**
   With more time, I would implement robust error handling, integrate a caching mechanism, and optimize the database queries for improved performance.
