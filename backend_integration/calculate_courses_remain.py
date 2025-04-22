import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import ssl
import json
import re

ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

with open("major_curriculum.json", "r") as file:
    major_curriculum = json.load(file)
with open("specialization_curriculum.json", "r") as file:
    special_curriculum = json.load(file)


# Test: 
# {"special": "AIT", "courses": []}
# {"special": "AIT", "courses": ["Math 2568", "CSE 2331", "Stat 3201"]}

def get_remaining_groups(transcript: dict):
    groups_remaining = []
    groups_remaining = checkEngineering(transcript, groups_remaining)
    groups_remaining = checkMajorCore(transcript, groups_remaining)
    groups_remaining = checkNonMajor(transcript, groups_remaining)
    groups_remaining = checkTechnicalElectives(transcript, groups_remaining)
    groups_remaining = checkGenEds(transcript, groups_remaining)
    groups_remaining = checkSpecial(transcript, groups_remaining)
    return groups_remaining

def checkEngineering(transcript: dict, groupsList: list):
    # Flag to check if all requirements are met
    isGroupDone = True
    # Loop through each category
    for group in major_curriculum["Engineering"]:
        # Flag to check if a category is complete or not
        isSubGroupDone = False
        # Loop through courses in category
        for course in group:
            if course in transcript["courses"]:
                isSubGroupDone = True
                break   # Remove break for debugging
        # If a category is not complete, break and return
        if isSubGroupDone == False:
            isGroupDone = False           
            break   # Remove break for debugging
    if isGroupDone == False:
        groupsList.append("Engineering Requirements")
    return groupsList

def checkMajorCore(transcript: dict, groupsList: list):
    # Flag to check if all requirements are met
    isGroupDone = True
    # Loop through each category
    for group in major_curriculum["MajorCore"]:
        # Flag to check if a category is complete or not
        isSubGroupDone = False
        # Loop through courses in category
        for course in group:
            if course in transcript["courses"]:
                isSubGroupDone = True
                break   # Remove break for debugging
        # If a category is not complete, break and return
        if isSubGroupDone == False:
            isGroupDone = False           
            break   # Remove break for debugging
    if isGroupDone == False:
        groupsList.append("Major Core Requirements")
    return groupsList

def checkNonMajor(transcript: dict, groupsList: list):
    # Flag to check if all requirements are met
    isGroupDone = True
    for group in major_curriculum["NonMajor"]["Courses"]:
        # Flag to check if a category is complete or not
        isSubGroupDone = False
        # Loop through courses in category
        for course in group:
            if course in transcript["courses"]:
                isSubGroupDone = True
                break   # Remove break for debugging
        # If a category is not complete, break and return
        if isSubGroupDone == False:
            isGroupDone = False           
            break   # Remove break for debugging
    # Make sure the user has at least 8 credits of Math/Science electives
    electiveCredits = 8
    for course in major_curriculum["NonMajor"]["Electives"]:
        name = list(course.keys())[0]
        if name in transcript["courses"]:
            electiveCredits -= list(course.values())[0]
    if isGroupDone == False or electiveCredits > 0:
        groupsList.append("Non-Major Requirements")
    return groupsList

def checkTechnicalElectives(transcript: dict, groupsList: list):
    # Sum of credits for 3000+s.
    sum3000Plus = 0
    # Loop through each category
    for category in major_curriculum["TechnicalElectives"]:
        for course in major_curriculum["TechnicalElectives"][category]:
            courseName = list(course.keys())[0]
            # Amount of credits for a course
            courseCredits = list(course.values())[0]
            # Get just the 4 digit course number
            courseNum = int(re.search("[0-9]+", courseName)[0])
            if courseNum >= 3000 and courseName in transcript["courses"]:
                sum3000Plus += courseCredits
    # Find total credits
    totalCredits = sum3000Plus
    # Update list
    if totalCredits < 17:
        groupsList.append("Technical Electives Requirements")
        
    return groupsList

def checkGenEds(transcript: dict, groupsList: list):
    # Flag to check if all requirements are met
    isGroupDone = True
    # Categories that are not done
    categoryNotDone = []
    # Credit count for each category
    creditRequirements = {"LaunchSeminar": 1, "WritingAndInfo": 3, "MathAndQuant": 3, "LitVisualAndPerform": 3, 
                          "HistoricalAndCultural": 3, "NaturalScience": 3, "SocialAndBehavioral": 3, 
                          "RaceEthnicAndGender": 3, "Citizenship": 4, "Choice": 4}
    for category in major_curriculum["GenEd"]:
        creditsSum = 0
        for course in major_curriculum["GenEd"][category]:
            courseName = list(course.keys())[0]
            # Amount of credits for a course
            courseCredits = int(list(course.values())[0])
            # Get just the 4 digit course number
            courseNum = int(re.search("[0-9]+", courseName)[0])
            # Add to credits sum iof course has been taken
            if courseName in transcript["courses"]:
                creditsSum += courseCredits
            # Break if credits is greater than or equal to the requirement 
            if creditsSum >= creditRequirements[category]:
                break
        if creditsSum < creditRequirements[category]:
            isGroupDone = False
            categoryNotDone.append(category)

    if isGroupDone == False:
        groupsList.extend(categoryNotDone)
            
    return groupsList

def checkSpecial(transcript: dict, groupsList: list):
    # Flag to check if group is done
    isGroupDone = True
    coursesTaken = set()
    specialGroup = transcript["special"]
    for category in special_curriculum[specialGroup]:
        for course in category:
            if course in transcript["courses"] and course not in coursesTaken:
                coursesTaken.add(course)
                break
        
    if isGroupDone == False:
        groupsList.append(specialGroup + " Specialization Requirements")

    return groupsList


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
    if not docs: # Nothing found in elasticsearch
        return []
    source = docs[0]['_source']
    course_reqs = source["prereqs"]
    # print(source["description"])
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