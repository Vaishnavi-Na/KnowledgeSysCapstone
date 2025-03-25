import requests
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl
import os

def fetch_courses(base_url, query_params):
    courses = []
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url, params=query_params)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
        
        data = response.json()
        courses.extend(data.get("data", {}).get("courses", []))
        
        next_page_link = data.get("data", {}).get("nextPageLink")
        if not next_page_link:
            break
        
        query_params["p"] = page + 1
        page += 1
    
    return courses

def parse_courses(courses):
    parsed_data = []
    for course in courses:
        course_info = course["course"]
        sections = course.get("sections", [])
        parsed_data.append({
            "title": course_info["title"],
            "description": course_info["description"],
            "catalog_number": course_info["catalogNumber"],
            "term": course_info["term"],
            "units": course_info["maxUnits"],
            "sections": [
                {
                    "class_number": section["classNumber"],
                    "section": section["section"],
                    "component": section["component"],
                    "instruction_mode": section["instructionMode"],
                    "meeting_details": [
                        {
                            "facility": meeting.get("facilityDescription", "N/A"),
                            "building": meeting.get("buildingDescription", "N/A"),
                            "room": meeting.get("room", "N/A"),
                            "start_time": meeting.get("startTime", "N/A"),
                            "end_time": meeting.get("endTime", "N/A"),
                            "days": {
                                "monday": meeting.get("monday", False),
                                "tuesday": meeting.get("tuesday", False),
                                "wednesday": meeting.get("wednesday", False),
                                "thursday": meeting.get("thursday", False),
                                "friday": meeting.get("friday", False),
                                "saturday": meeting.get("saturday", False),
                                "sunday": meeting.get("sunday", False),
                            },
                            "instructors": [
                                {
                                    "name": instructor.get("displayName", "N/A"),
                                    "role": instructor.get("role", "N/A"),
                                    "email": instructor.get("email", "N/A")
                                }
                                for instructor in meeting.get("instructors", [])
                            ]
                        }
                        for meeting in section.get("meetings", [])
                    ]
                }
                for section in sections
            ]
        })
    return parsed_data

def index_to_elasticsearch(data):
    ctx = ssl.create_default_context()
    ctx.load_verify_locations("http_ca.crt")
    ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    load_dotenv()
    es = Elasticsearch("https://localhost:9200", ssl_context=ctx, basic_auth=("elastic", os.getenv("ELASTIC_PASSWORD")))
    index_name = "osu_courses"
    
    for i, course in enumerate(data):
        es.index(index=index_name, id=i, document=course)
    
    print("Data successfully indexed to Elasticsearch.")


def main():
    base_url = "https://content.osu.edu/v2/classes/search"
    query_params = {
        "q": "CSE",
        "client": "class-search-ui",
        "campus": "col",
        "p": 1
    }
    
    courses = fetch_courses(base_url, query_params)
    parsed_data = parse_courses(courses)
    
    with open("osu_cse_courses.json", "w") as f:
        json.dump(parsed_data, f, indent=4)
    
    print("Scraping complete. Data saved to osu_cse_courses.json")
    
    index_to_elasticsearch(parsed_data)

if __name__ == "__main__":
    main()
