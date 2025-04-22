from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from calculate_courses_remain import calculate_remaining_courses, get_remaining_groups
from query import search_professors_sort
from scraper_json import scrap_from_adv_rep
import ssl
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from typing import Optional
from pydantic import BaseModel
import os
from generate_schedule import generate_schedule
# from query import demo_search_course

app = FastAPI()

# Allow CORS for requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_adv_report(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="File is not a pdf")
    
    try:
        file_bytes = await file.read()
        result = scrap_from_adv_rep(file_bytes)

        if "error" in result: 
            # error occurred in scrap_from_adv_rep method
            return JSONResponse(content=result,status_code=500)
        
        return JSONResponse(content=result,status_code=200)
    except Exception as e:
        return JSONResponse(
            content={"error": f"Error uploading file: {str(e)}"},
            status_code=500  # Internal Server Error
        )

@app.post("/courses/get_remain")
async def get_remain(transcript: dict):
    specialization = transcript.get('special')
    if not specialization:
        raise HTTPException(status_code=400, detail="Specialization missing from transcript.")
    
    remaining_groups = get_remaining_groups(transcript)

    return {
        "specialization": specialization,
        "remaining_groups": remaining_groups
    }

@app.post("/courses/calc_remain")
async def calc_remain(transcript: dict, course: str):

    unmet_groups = calculate_remaining_courses(transcript, course)

    return unmet_groups

@app.post("/courses/gen_schedule")
async def gen_schedule(transcript: dict, hours: int):    
    schedule = generate_schedule(transcript, hours)
    print("Generated schedule:", schedule)

    return schedule

@app.post("/courses/professors")
async def search_prof(course: str, sort_by: str = "avg_rating", order: str = 'desc', comment_keywords: str = None):
    [subject, courseNum] = course.split(" ")
    if not subject or not courseNum:
        return []
    return search_professors_sort(subject, courseNum, sort_by, order, comment_keywords)

#Setup elasticsearch through REST API library
ctx = ssl.create_default_context()
ctx.load_verify_locations("http_ca.crt")
ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
load_dotenv()
es = Elasticsearch('https://localhost:9200', ssl_context=ctx, basic_auth=("elastic", os.getenv('ELASTIC_PASSWORD')))

@app.post("/courses/professors_with_courses")
async def search_prof_with_courses(
    course: str, 
    sort_by: str = "avg_rating", 
    order: str = 'desc', 
    comment_keywords: str = None
):
    print(f"Received request to search professors with course: {course}")
    print(f"Sort by: {sort_by}, Order: {order}, Comment Keywords: {comment_keywords}")

    try:
        subject, course_number = course.split()
        print(f"Parsed subject: {subject}, course_number: {course_number}")
    except ValueError:
        print("Error: Invalid course format")
        return {"error": "Invalid course format. Use e.g. 'CSE 2231'"}

    # Get list of professors for the course
    professors = search_professors_sort(subject, course_number, sort_by, order, comment_keywords)
    print(f"Found {len(professors.get('matched_professors', []))} matched professors")

    results = []

    # For each professor, get the courses they teach
    for prof in professors["matched_professors"]:
        instructor_name = prof["name"]

        query_body = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"subject.keyword": "CSE"}},
                        {"term": {"course_number.keyword": "2231"}},
                        {"term": {"instructor.keyword": instructor_name}}
                    ]
                }
            }
        }

        # Search in Elasticsearch
        print(f"Querying Elasticsearch for courses taught by {instructor_name}")
        res = es.search(index="osu_courses", body=query_body)
        hits = res["hits"]["hits"]
        print(f"Found {len(hits)} course(s) for {instructor_name}")

        courses = []

        # Transform Elasticsearch hits into the course details format
        for hit in hits:
            course_details = hit["_source"]
            print(f"  -> Found course: {course_details}")
            courses.append({
                "term": course_details.get("term"),
                "course_number": course_details.get("course_number"),
                "time": course_details.get("time"),
                "classroom": course_details.get("classroom"),
                "instructor": course_details.get("instructor")
            })

        # Add professor info along with the courses they teach
        prof_result = {
            "instructor": instructor_name,
            "rating": prof.get("avg_rating", None),
            "courses": courses,
            "id": prof.get('_id',None),
            "avg_rating": prof.get('avg_rating'),
            "difficulty": prof.get('difficulty'),
            "SEI_overall": prof.get('SEI_overall'),
            "SEI": prof.get('SEI'),
            "summary_comment": prof.get("summary_comment", ""),
            "score": prof.get('score')  
        }
        results.append(prof_result)
        print(f"Added result for {instructor_name}")

    print(f"\nFinal results: {results}")
    print({
        "matched_professors": results
    })
    return {
        "matched_professors": results
    }
