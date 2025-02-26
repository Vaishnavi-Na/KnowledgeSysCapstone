from fastapi import FastAPI
from search_in_RMP import demo_search

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/demo")
async def demo_search_w_rating(rating: float = 2.5):
    return demo_search(rating)