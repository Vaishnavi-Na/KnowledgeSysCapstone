from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from calculate_courses_remain import calculate_remaining_courses, get_remaining_groups
from query import search_professors_sort
from scraper_json import scrap_from_adv_rep
from search_in_RMP import demo_search_lte_rating, demo_search_desc_department
from generate_schedule import generate_schedule
# from query import demo_search_course

app = FastAPI()

# Allow CORS for requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/demo_course")
async def demo_search_course(subject: str = "cse", courseNum: str = "2221"):
    return demo_search_course(subject, courseNum)

@app.get("/demo_rating")
async def demo_search_w_rating(rating: float = 2.5):
    return demo_search_lte_rating(rating)

@app.get("/demo_sort")
async def demo_search_w_sorting(department: str = "English"):
    return demo_search_desc_department(department)

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

    return schedule

@app.post("/courses/professors")
async def search_prof(course: str, sort_by: str = "avg_rating", order: str = 'desc', comment_keywords: str = None):
    [subject, courseNum] = course.split(" ")
    if not subject or not courseNum:
        return []
    return search_professors_sort(subject, courseNum, sort_by, order, comment_keywords)
