from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import convert
import os

app = FastAPI()

origins = [
    os.getenv("FRONTEND_URL"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert.router)
