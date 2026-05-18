"""FastAPI application."""
from __future__ import annotations
from fastapi import FastAPI
from db.database import Base, engine
from models.book import Book
from models.author import Author
from api.v1.router import router as v1_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Library API",
    description="A simple book library API built with FastAPI and SQLAlchemy",
    version="1.0.0",
)

app.include_router(v1_router)