"""Book routes."""
from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from services.book_service import BookService
from schemas.book import BookCreate, BookResponse

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)

@router.post("", response_model=BookResponse)
def create_book(
    payload: BookCreate,
    service: BookService = Depends(get_book_service)
):
    return service.create(payload)

@router.get("/search", response_model=list[BookResponse])
def search_books(
    book_id: Optional[int] = None,
    title: Optional[str] = None,
    author_name: Optional[str] = None,
    year: Optional[int] = None,
    service: BookService = Depends(get_book_service)
):
    return service.search(
        book_id=book_id,
        title=title,
        author_name=author_name,
        year=year
    )

@router.get("", response_model=list[BookResponse])
def get_books(
    service: BookService = Depends(get_book_service)
):
    return service.get_all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    return service.get_or_404(book_id)