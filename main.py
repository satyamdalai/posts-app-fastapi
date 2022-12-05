from fastapi import FastAPI
from pymongo import MongoClient
from decouple import config
from app.routes import api_router

MONGODB_URI = config("mongodb_uri")
MONGODB_DB = config("mongodb_db")

app = FastAPI()

app.include_router(api_router)


@app.on_event("startup")
def startup_db_client():
    app.client = MongoClient(MONGODB_URI)
    app.db = app.client[MONGODB_DB]
    app.posts = app.db.posts
    app.users = app.db.users


@app.on_event("shutdown")
def shutdown_db_client():
    app.client.close()
