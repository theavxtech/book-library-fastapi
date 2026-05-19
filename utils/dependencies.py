"""Common FastAPI dependencies."""
from __future__ import annotations
from db.database import SessionLocal
from fastapi import Query

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        size: int = Query(default=10, ge=1, le=100, description="Items per page")
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size        