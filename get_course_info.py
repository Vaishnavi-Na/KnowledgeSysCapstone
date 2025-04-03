import random
from time import sleep
import requests
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl
import csv
import os
import json
import re

def get_prof_in(csv_name):
    all_parsed_data = []
    hash = set()
    # cse_interest_subjects = set(["cse", "math", "engr", "physics", "ece", "stat"]) # For the benefit of our machine
    cse_interest_subjects = set(["cse"])
    with open(csv_name, mode='r') as file:
        csv_reader=csv.reader(file)

        next(csv_reader)  
        previous_subject = "PLACE HOLDER"
        for row in csv_reader:
            base_url = "https://content.osu.edu/v2/classes/search"

            subject = row[2].lower()
            if subject != previous_subject:
                sec = random.randint(1,3) + random.random() * 3
                print(f"{previous_subject} done, rest {sec}s then starting {subject}")
                sleep(sec)
                previous_subject = subject
            key = f"{subject} {row[3]}"
            # print(f"key: {key}")
            # if key not in hash and subject in cse_interest_subjects:
            if key not in hash:
                hash.add(key)
                query_params = {
                    "q": row[3],  
                    "client": "class-search-ui",
                    "campus": "col",
                    "term": "1258",
                    "p": "1",
                    "class-session": "1",
                    "academic-career": "ugrd",
                    "subject": subject
                }
                courses = fetch_courses(base_url, query_params)
                parsed_data = parse_courses(courses)
                all_parsed_data.extend(parsed_data)
                if parsed_data: print(f"course {key} scraped")

                # index_to_elasticsearch(parsed_data)

        # with open("backend_integration\\osu_cse_courses.json", "w") as f:
        #     json.dump(all_parsed_data, f, indent=4)            

        # print("Scraping complete. Data saved to backend_integration\\osu_cse_courses.json")

        index_to_elasticsearch(all_parsed_data)
        print("Scraping complete. Data saved to index")

def fetch_courses(base_url, query_params):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://classes.osu.edu/",
        "Accept": "application/json"
    }
    courses = []
    
    response = requests.get(base_url, params=query_params, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return
    
    data = response.json()
    if len(data["data"]["courses"])>0:
        courses.append(data["data"]["courses"][0])
    return courses

def parse_prerequisites(text, course):
    text = re.sub(r'Prereq or concur:', 'Concur:', text, flags=re.IGNORECASE)
    text = re.sub(r'Concur\s*\(for students with credit for [^)]+\):', 'Concur:', text, flags=re.IGNORECASE)
    
    prereq_pattern = re.compile(r'Prereq: (.*?)(?:\.|Concur:|Not open|enrollment in|$)')
    concur_pattern = re.compile(r'Concur: (.*?)(?:\.|Not open|$)')
    major_pattern = re.compile(r'enrollment in (.*?)(?:\.|Not open|$)')
    exclusion_pattern = re.compile(r'Not open to students with credit for (.*?)(?:\.|$)')
    
    prerequisites = prereq_pattern.findall(text)
    concurrent = concur_pattern.findall(text)
    majors = major_pattern.findall(text)
    exclusions = exclusion_pattern.findall(text)
    
    course_code_pattern = re.compile(r'([A-Z][a-zA-Z&]*)(?:\s+)?(\d{3,4})')

    def normalize_items(text_chunk):
        parts = []
        last_prefix = course
        for raw in re.split(r',| or ', text_chunk):
            raw = raw.strip()
            if not raw:
                continue
            match = course_code_pattern.search(raw)
            if match:
                prefix, number = match.groups()
                last_prefix = prefix
                parts.append(f"{prefix} {number}")
            else:
                # try adding numbers to the last known prefix
                nums = re.findall(r'\d{3,4}', raw)
                if nums:
                    for num in nums:
                        parts.append(f"{last_prefix} {num}")
                else:
                    # fallback for freeform items (like "Grad standing")
                    parts.append(raw)
        return parts

    def extract_nested_list(data):
        if not data:
            return []
        result = []
        and_parts = re.split(r'\b; and\b', data[0], flags=re.IGNORECASE)
        for part in and_parts:
            group = normalize_items(part)
            if group:
                result.append(group)
        return result

    def extract_flat_list(data):
        if not data:
            return []
        return [item.strip() for item in re.split(r',| or | and ', data[0]) if item.strip()]
    
    return {
        "Prerequisites": extract_nested_list(prerequisites),
        "Concurrent Courses": extract_nested_list(concurrent),
        "Restricted Majors": extract_flat_list(majors),
        "Exclusions": extract_flat_list(exclusions)
    }
    
def parse_courses(courses):
    parsed_data = []
    for course in courses:
        course_info = course["course"]
        # print(json.dumps(course_info, indent=4))
        if 'title' not in course_info: return [] # no title might indicates enrollment not open
        sections = course.get("sections", [])
        course_info["catalogNumber"]
        parsed_data.append({
            "course": f"{course_info['subject']} {course_info['catalogNumber']}",
            "title": course_info['title'],
            "description": course_info["description"],
            "prereqs": parse_prerequisites(course_info["description"], course_info["subject"]),
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
    get_prof_in("osu_professors_data.csv")
    
if __name__ == "__main__":
    main()
