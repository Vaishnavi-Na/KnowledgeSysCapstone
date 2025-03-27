import requests
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from bs4 import BeautifulSoup
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

headersProf = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic dGVzdDp0ZXN0",
    "content-type": "application/json",
    "origin": "https://www.ratemyprofessors.com",
    "referer": osu_url,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

#GraphQL data query for professor information
data = {
    "query": """query TeacherSearchPaginationQuery($count: Int!, $query: TeacherSearchQuery!, $cursor: String) {
    search: newSearch {
            teachers(query: $query, first: $count, after:$cursor) {
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
                        id
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
        "query": {
            "text": "",
            "schoolID": "U2Nob29sLTcyNA==",
            "fallback": True
        },
        "cursor":None
    }
}

prof_data = {
    "query": """query RatingsListQuery($count: Int!, $id: ID!, $courseFilter: String, $cursor: String) {
        node(id: $id) {
            ... on Teacher {
            numRatings
            ratings(first: $count, after: $cursor,courseFilter: $courseFilter) {
                edges {
                    node {
                        comment
                        clarityRating
                        difficultyRating
                    }
                }
                pageInfo {
                    hasNextPage
                    endCursor
                }
            }
            }
        }
    }""",
    "variables": {
        "count": 30,
        "cursor": None,
        "id": 0000
    }
}



#Setup elasticsearch through REST API library
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

# def get_first_page()""

#This method gets the reviews for each professor in rate my professor
#using their ID, it gets a professor's review page and scrapes each review 
def get_reviews(professor_id, j, id):
    # URL of the professor's page on RateMyProfessors
    url = f"https://www.ratemyprofessors.com/professor/{professor_id}"
    headersProf["referer"] = url

    # Initialize the Ratings list if it doesn't exist
    if "Ratings" not in j:
        j["Ratings"] = []
    
    index = 1
    # Load all the comments
    while True:
        #print("\nNew Page")
        # Get the current page comments
        prof_data["variables"]["id"] = id
        response = requests.post(graphql_url, headers=headersProf, json=prof_data).json()
        # print(response)
        ratings = response["data"]["node"]["ratings"]["edges"]
        if response["data"]["node"]["numRatings"]==0:
            return 
        
        for rating in ratings:
            j["Ratings"].append({
                "index":index, 
                "rating": rating["node"]["clarityRating"],
                "difficulty": rating["node"]["difficultyRating"],
                "comment": rating["node"]["comment"]
                })
            index += 1

        page_info = response["data"]["node"]["ratings"]["pageInfo"]

        #pagination logic
        if not page_info["hasNextPage"]:
            break  # Stop if no more pages

        #update cursor for next request
        prof_data["variables"]["cursor"] = page_info["endCursor"]
    prof_data["variables"]["cursor"] = None
        
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
            print("\n" + professor["node"]["lastName"] + professor["node"]["firstName"])
            get_reviews(professor["node"]["legacyId"],professor["node"],professor["node"]["id"])
            es.index(index='professors', id=professor["node"]["lastName"] + professor["node"]["firstName"], document=professor["node"])

        #pagination logic
        page_info = response["data"]["search"]["teachers"]["pageInfo"]
        if not page_info["hasNextPage"]:
            break  # Stop if no more pages

        #update cursor for next request
        data["variables"]["cursor"] = page_info["endCursor"]
    return

search_school_professor()