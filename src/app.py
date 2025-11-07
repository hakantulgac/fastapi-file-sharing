from fastapi import FastAPI

from src.db import create_db_tables
from src.routers.channels import router as channel_router
from src.routers.files import router as files_router

create_db_tables()

app = FastAPI()

app.include_router(channel_router)
app.include_router(files_router)

@app.get("/")
def read_root():
    return {"message": "Application running. Visit /docs address"}