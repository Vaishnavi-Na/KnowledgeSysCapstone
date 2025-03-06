import requests
from bs4 import BeautifulSoup

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
