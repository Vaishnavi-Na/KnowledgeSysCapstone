import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import json
import ssl

osu_url="https://www.ratemyprofessors.com/search/professors/724"
graphql_url = "https://www.ratemyprofessors.com/graphql"

#Headers (taken from devtools payload)
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic dGVzdDp0ZXN0",
    "content-type": "application/json",
    "cookie": "_pubcid=82771824-36cc-4e0d-86ad-ee65996248a1; _pubcid_cst=zix7LPQsHA==; pjs-unifiedid={...}",  # Paste full cookie
    "origin": "https://www.ratemyprofessors.com",
    "referer": osu_url,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

#GraphQL data query for professor information
data = {
    "query": """query TeacherSearchPaginationQuery($count: Int!, $cursor: String, $query: TeacherSearchQuery!) {
        search: newSearch {
            teachers(query: $query, first: $count, after: $cursor) {
                edges {
                    cursor
                    node {
                        legacyId
                        firstName
                        lastName
                        avgRating
                        numRatings
                        department
                        avgRating
                        avgDifficulty
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
        }
    }""",
    "variables": {
        "count": 8,
        "cursor": "YXJyYXljb25uZWN0aW9uOjc=",
        "query": {
            "text": "",
            "schoolID": "U2Nob29sLTcyNA==",
            "fallback": True
        }
    }
}

#Setup elasticsearch through REST API library
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

#This method gets the reviews for each professor in rate my professor
#using their ID, it gets a professor's review page and scrapes each review 
def get_reviews(professor_id, j):
    # URL of the professor's page on RateMyProfessors
    url = f'https://www.ratemyprofessors.com/professor/{professor_id}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find root of HTML webpage
    root = soup.find(id="root")
    ratings = root.find_all(class_="Rating__RatingBody-sc-1rhvpxz-0 dGrvXb")
    
    # Initialize the Ratings list if it doesn't exist
    if "Ratings" not in j:
        j["Ratings"] = []

    #Add a list of each rating (index, rating and comment) to the professor's dict
    for index, rating in enumerate(ratings):
        box=rating.find(class_="RatingValues__StyledRatingValues-sc-6dc747-0 gFOUvY")
        quality=box.find(class_="CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 gcFhmN")
        comment= rating.find(class_="Comments__StyledComments-dzzyvm-0 gRjWel")

        j["Ratings"].append({
                "index": index, 
                "rating": quality.get_text(strip=True) if quality else None,
                "comment": comment.get_text(strip=True) if comment else None
            })
        
#This function uses the graphql endpoint and the given headers to get information about each professor
#It returns when the professors being scraped either don't have any reviews or when there is no longer 
#any professors to scrape
def search_school_professor():
    while True:
        #get html from graphql_url using set headers
        response = requests.post(graphql_url, headers=headers, json=data).json()
        
        #for each professor, get their reviews and add elasticsearch index
        for professor in response["data"]["search"]["teachers"]["edges"]:            
            if professor["node"]["numRatings"]==0:
                return 

            get_reviews(professor["node"]["legacyId"],professor["node"])
            es.index(index='professors', id=professor["node"]["lastName"] + professor["node"]["firstName"], document=professor["node"])

        #pagination logic
        page_info = response["data"]["search"]["teachers"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break  # Stop if no more pages

        #update cursor for next request
        data["variables"]["cursor"] = page_info["endCursor"]
    return

search_school_professor()