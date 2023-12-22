from fastapi import FastAPI
from routers import database

app = FastAPI()
app.include_router(database.router)


@app.get("/")
async def health_check():
    return {"message": "Analyzer is running"}
