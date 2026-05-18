"""Author routes."""
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from services.author_service import AuthorService
from schemas.author import AuthorCreate, AuthorResponse

router = APIRouter(prefix="/authors", tags=["authors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_author_service(db: Session = Depends(get_db)) -> AuthorService:
    return AuthorService(db)

@router.post("", response_model=AuthorResponse)
def create_author(
    payload: AuthorCreate,
    service: AuthorService = Depends(get_author_service)
):
    return service.create(payload)

@router.get("", response_model=list[AuthorResponse])
def get_authors(
    service: AuthorService = Depends(get_author_service)
):
    return service.get_all()