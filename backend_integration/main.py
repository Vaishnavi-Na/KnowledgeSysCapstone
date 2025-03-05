from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from scraper_json import scrap_from_adv_rep
from search_in_RMP import demo_search_lte_rating, demo_search_desc_department

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
