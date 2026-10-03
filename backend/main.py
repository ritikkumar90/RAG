from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from routers import auth, user
from database import engine
import models



app = FastAPI(
    title="RAG API",
    description="API for uploading documents and asking questions.",
    version="1.0.0"
)
models.Base.metadata.create_all(bind=engine)

# Add CORS middleware so the frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def home():
    return {"message":"Home Page"}


