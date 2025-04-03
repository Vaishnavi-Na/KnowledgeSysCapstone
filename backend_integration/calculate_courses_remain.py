import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl
import json

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

with open("major_curriculum.json") as f:
    major_curriculum: dict = json.load(f)


# Test: 
# {"special": "AIT", "courses": []}
# {"special": "AIT", "courses": ["Math 2568", "CSE 2331", "Stat 3201"]}

def get_remaining_groups(transcript: dict) -> list[list[str]]:
    '''Get a list of all unfinished groups'''
    taken_courses: set[str] = set(transcript['courses'])
    specialization: str = transcript.get('special', '')

    # Combine general and specialization-specific courses
    curriculum: list[list[str]] = major_curriculum["general"]
    curriculum.extend(major_curriculum.get(specialization, [[]]))

    remaining_groups: list[list[str]] = []

    for group in curriculum:
        # If none of the courses in the group are taken, it's unfinished
        if not any(course in taken_courses for course in group):
            remaining_groups.append(group)

    return remaining_groups

def calculate_remaining_courses(transcript: dict, course: str) -> list[list[str]]:
    '''Given a course, return a list of all unmet prereq groups'''
    taken_courses: set[str] = set(transcript['courses'])
    if course in taken_courses:
        return []  # already completed, no unmet prereqs
    
    # Find prerequisite info
    searching_rule = {
        "match": {
            "course": course
        }
    }
    query = {
        "query": searching_rule
    }
    res = es.search(index = "osu_courses", body = query)
    docs = res["hits"]["hits"]
    source = docs[0]['_source']
    course_reqs = source["prereqs"]
    print(source["description"])
    # course_reqs = next((item["prereqs"] for item in prereq_info if item["course"] == course), None)
    if not course_reqs:
        return []  # no prerequisites, course can be taken

    unmet_groups = []
    all_requirements = course_reqs.get('Prerequisites', []) + course_reqs.get('Concurrent Courses', [])

    for prereq_group in all_requirements:
        # At least one course in the group must be taken
        if not any(c in taken_courses for c in prereq_group):
            unmet_groups.append(prereq_group)

    return unmet_groups