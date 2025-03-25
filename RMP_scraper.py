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
"""
query TeacherRatingsPageQuery(
  $id: ID!
) {
  node(id: $id) {
    __typename
    ... on Teacher {
      id
      legacyId
      firstName
      lastName
      department
      school {
        legacyId
        name
        city
        state
        country
        id
      }
      lockStatus
      ...StickyHeaderContent_teacher
      ...RatingDistributionWrapper_teacher
      ...TeacherInfo_teacher
      ...SimilarProfessors_teacher
      ...TeacherRatingTabs_teacher
    }
    id
  }
}

fragment CompareProfessorLink_teacher on Teacher {
  legacyId
}

fragment CourseMeta_rating on Rating {
  attendanceMandatory
  wouldTakeAgain
  grade
  textbookUse
  isForOnlineClass
  isForCredit
}

fragment HeaderDescription_teacher on Teacher {
  id
  legacyId
  firstName
  lastName
  department
  school {
    legacyId
    name
    city
    state
    id
  }
  ...TeacherTitles_teacher
  ...TeacherBookmark_teacher
  ...RateTeacherLink_teacher
  ...CompareProfessorLink_teacher
}

fragment HeaderRateButton_teacher on Teacher {
  ...RateTeacherLink_teacher
  ...CompareProfessorLink_teacher
}

fragment NameLink_teacher on Teacher {
  isProfCurrentUser
  id
  legacyId
  firstName
  lastName
  school {
    name
    id
  }
}

fragment NameTitle_teacher on Teacher {
  id
  firstName
  lastName
  department
  school {
    legacyId
    name
    id
  }
  ...TeacherDepartment_teacher
  ...TeacherBookmark_teacher
}

fragment NoRatingsArea_teacher on Teacher {
  lastName
  ...RateTeacherLink_teacher
}

fragment NumRatingsLink_teacher on Teacher {
  numRatings
  ...RateTeacherLink_teacher
}

fragment ProfessorNoteEditor_rating on Rating {
  id
  legacyId
  class
  teacherNote {
    id
    teacherId
    comment
  }
}

fragment ProfessorNoteEditor_teacher on Teacher {
  id
}

fragment ProfessorNoteFooter_note on TeacherNotes {
  legacyId
  flagStatus
}

fragment ProfessorNoteFooter_teacher on Teacher {
  legacyId
  isProfCurrentUser
}

fragment ProfessorNoteHeader_note on TeacherNotes {
  createdAt
  updatedAt
}

fragment ProfessorNoteHeader_teacher on Teacher {
  lastName
}

fragment ProfessorNoteSection_rating on Rating {
  teacherNote {
    ...ProfessorNote_note
    id
  }
  ...ProfessorNoteEditor_rating
}

fragment ProfessorNoteSection_teacher on Teacher {
  ...ProfessorNote_teacher
  ...ProfessorNoteEditor_teacher
}

fragment ProfessorNote_note on TeacherNotes {
  comment
  ...ProfessorNoteHeader_note
  ...ProfessorNoteFooter_note
}

fragment ProfessorNote_teacher on Teacher {
  ...ProfessorNoteHeader_teacher
  ...ProfessorNoteFooter_teacher
}

fragment RateTeacherLink_teacher on Teacher {
  legacyId
  numRatings
  lockStatus
}

fragment RatingDistributionChart_ratingsDistribution on ratingsDistribution {
  r1
  r2
  r3
  r4
  r5
}

fragment RatingDistributionWrapper_teacher on Teacher {
  ...NoRatingsArea_teacher
  ratingsDistribution {
    total
    ...RatingDistributionChart_ratingsDistribution
  }
}

fragment RatingFooter_rating on Rating {
  id
  comment
  adminReviewedAt
  flagStatus
  legacyId
  thumbsUpTotal
  thumbsDownTotal
  thumbs {
    thumbsUp
    thumbsDown
    computerId
    id
  }
  teacherNote {
    id
  }
  ...Thumbs_rating
}

fragment RatingFooter_teacher on Teacher {
  id
  legacyId
  lockStatus
  isProfCurrentUser
  ...Thumbs_teacher
}

fragment RatingHeader_rating on Rating {
  legacyId
  date
  class
  helpfulRating
  clarityRating
  isForOnlineClass
}

fragment RatingSuperHeader_rating on Rating {
  legacyId
}

fragment RatingSuperHeader_teacher on Teacher {
  firstName
  lastName
  legacyId
  school {
    name
    id
  }
}

fragment RatingTags_rating on Rating {
  ratingTags
}

fragment RatingValue_teacher on Teacher {
  avgRating
  numRatings
  ...NumRatingsLink_teacher
}

fragment RatingValues_rating on Rating {
  helpfulRating
  clarityRating
  difficultyRating
}

fragment Rating_rating on Rating {
  comment
  flagStatus
  createdByUser
  teacherNote {
    id
  }
  ...RatingHeader_rating
  ...RatingSuperHeader_rating
  ...RatingValues_rating
  ...CourseMeta_rating
  ...RatingTags_rating
  ...RatingFooter_rating
  ...ProfessorNoteSection_rating
}

fragment Rating_teacher on Teacher {
  ...RatingFooter_teacher
  ...RatingSuperHeader_teacher
  ...ProfessorNoteSection_teacher
}

fragment RatingsFilter_teacher on Teacher {
  courseCodes {
    courseCount
    courseName
  }
}

fragment RatingsList_teacher on Teacher {
  id
  legacyId
  lastName
  numRatings
  school {
    id
    legacyId
    name
    city
    state
    avgRating
    numRatings
  }
  ...Rating_teacher
  ...NoRatingsArea_teacher
  ratings(first: 20) {
    edges {
      cursor
      node {
        ...Rating_rating
        id
        __typename
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

fragment SimilarProfessorListItem_teacher on RelatedTeacher {
  legacyId
  firstName
  lastName
  avgRating
}

fragment SimilarProfessors_teacher on Teacher {
  department
  relatedTeachers {
    legacyId
    ...SimilarProfessorListItem_teacher
    id
  }
}

fragment StickyHeaderContent_teacher on Teacher {
  ...HeaderDescription_teacher
  ...HeaderRateButton_teacher
}

fragment TeacherBookmark_teacher on Teacher {
  id
  isSaved
}

fragment TeacherDepartment_teacher on Teacher {
  department
  departmentId
  school {
    legacyId
    name
    id
  }
}

fragment TeacherFeedback_teacher on Teacher {
  numRatings
  avgDifficulty
  wouldTakeAgainPercent
}

fragment TeacherInfo_teacher on Teacher {
  id
  lastName
  numRatings
  ...RatingValue_teacher
  ...NameTitle_teacher
  ...TeacherTags_teacher
  ...NameLink_teacher
  ...TeacherFeedback_teacher
  ...RateTeacherLink_teacher
  ...CompareProfessorLink_teacher
}

fragment TeacherRatingTabs_teacher on Teacher {
  numRatings
  courseCodes {
    courseName
    courseCount
  }
  ...RatingsList_teacher
  ...RatingsFilter_teacher
}

fragment TeacherTags_teacher on Teacher {
  lastName
  teacherRatingTags {
    legacyId
    tagCount
    tagName
    id
  }
}

fragment TeacherTitles_teacher on Teacher {
  department
  school {
    legacyId
    name
    id
  }
}

fragment Thumbs_rating on Rating {
  id
  comment
  adminReviewedAt
  flagStatus
  legacyId
  thumbsUpTotal
  thumbsDownTotal
  thumbs {
    computerId
    thumbsUp
    thumbsDown
    id
  }
  teacherNote {
    id
  }
}

fragment Thumbs_teacher on Teacher {
  id
  legacyId
  lockStatus
  isProfCurrentUser
}
"""

prof_data = {
    "query": """query RatingsListQuery($id: ID!, $cursor: String) {
        node(id: $id) {
            ... on Teacher {
            numRatings
            ratings(after:$cursor) {
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
    
    index = 0
    # Load all the comments
    while True:
        #print("\nNew Page")
        # Get the current page comments
        prof_data["variables"]["id"] = id
        response = requests.post(graphql_url, headers=headersProf, json=prof_data).json()
        print(response)
        ratings = response["data"]["node"]["ratings"]["edges"]
        if response["data"]["node"]["numRatings"]==0:
            return 
        
        for rating in ratings:
            j["Ratings"].append({
                "index":index, 
                "rating": rating["node"]["difficultyRating"],
                "comment": rating["node"]["comment"]
                })
            index += 1

        page_info = response["data"]["node"]["ratings"]["pageInfo"]

        #pagination logic
        if not page_info["hasNextPage"]:
            break  # Stop if no more pages

        #update cursor for next request
        prof_data["variables"]["cursor"] = page_info["endCursor"]
    # print(j)
        
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