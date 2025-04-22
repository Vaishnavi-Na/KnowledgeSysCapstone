import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from calculate_courses_remain import calculate_remaining_courses, get_remaining_groups
from query import search_professors_sort
from scraper_json import scrap_from_adv_rep
from search_in_RMP import demo_search_lte_rating, demo_search_desc_department
import ssl
import json

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

def recursive_prereq_check(transcript: dict, prereq: str) -> list[str]:
    '''Given a course, return a list of all unmet prereqs'''

    check_prereq = calculate_remaining_courses(transcript, prereq)
    avail_classes = []
    if not check_prereq:
        avail_classes.append(prereq)
    else:
        # Basically DFS through the prereqs to find all unmet prereqs
        for prereq_group in check_prereq:
            for new_prereq in prereq_group:
                leaf_prereq = recursive_prereq_check(transcript, new_prereq)
                avail_classes.extend(leaf_prereq)
                if(leaf_prereq[0] == new_prereq):
                    break

    return avail_classes


def check_avail(transcript:dict, remaining_groups: list[list[str]]) -> list[str]:
    '''Given a dict of courses return a list of courses the student can take'''
    avail_courses = []
    prereqs = []
    # For each group in the unfinished groups
    for group in remaining_groups:
        # For each remaining course in the group
        for course in group:
            # Get the prereqs (if any) for the course
            prereqs = calculate_remaining_courses(transcript, course)
            # If list is empty then all prereqs met so we add the course
            if(not prereqs):
                avail_courses.append(course)
                break
            # If there are prereqs, add them into the list of courses to take
            else:
                # For each group of prereqs
                for prereq_group in prereqs:
                    # For each prereq in the group
                    for prereq in prereq_group:
                        # Make sure student meets requirements to take prereq
                        new_prereqs = recursive_prereq_check(transcript, prereq)
                        # Add the necessary courses to the available courses
                        avail_courses.extend(new_prereqs)
                            
    return avail_courses
           
def create_semester(transcript:dict, max_hours:int) -> list[str]:
    '''Given a transcript and max hours return a list of courses to take'''
    # Get the remaining groups of courses
    remaining_groups = get_remaining_groups(transcript)
    # Get the available courses to take
    avail_courses = check_avail(transcript, remaining_groups)
    
    semester_courses = []
    total_hours = 0
    curr_units = 0

    for course in avail_courses:
        # Find credit hour info
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
        if not docs: # Nothing found in elasticsearch
            return []
        source = docs[0]['_source']
        curr_units = source["units"]

        # If adding the course would exceed max hours, break
        if(total_hours + curr_units) > max_hours:
            break
        else:
            total_hours += curr_units
            semester_courses.append(course)
            curr_units = 0
    
    return semester_courses

# Need to ask user how many credit hours they want to take (diff each semester? same each semester?)
# Then can generate a full schedule properly
# Currently same credit hours each semester, no limit on semesters it would take to finish

def generate_schedule(transcript:dict, max_hours:int) -> list[list[str]]:
    '''Given a transcript and max hours return a list of semesters with courses to take'''
    schedule = []
    transcript_copy = transcript.copy()
    # While there are still courses to take
    while True:
        semester_courses = create_semester(transcript_copy, max_hours)
        if not semester_courses:
            break
        schedule.append(semester_courses)
        # Add the courses to the transcript copy so that the original is untouched
        for course in semester_courses:
            if course not in transcript['courses']:
                transcript_copy['courses'].add(course)
    return schedule

# Add frontend integration
# How are we picking tech electives? Some are from specialization but some need to be able to be chosen
