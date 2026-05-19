"""Author service — author business logic."""
from __future__ import annotations
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.author_repository import AuthorRepository
from schemas.author import AuthorCreate
from models.author import Author


class AuthorService:
    def __init__(self, session: Session) -> None:
        self.repo = AuthorRepository(session)

    def create(self, payload: AuthorCreate) -> Author:
        existing_id = self.repo.get_by_author_id(payload.author_id)
        if existing_id:
            raise HTTPException(status_code=400, detail="Author ID already exists")

        return self.repo.create(
            author_id=payload.author_id,
            name=payload.name,
            nationality=payload.nationality,
            birth_year=payload.birth_year
        )
    
    def get_all(self, page: int, size: int) -> dict:
        skip = (page - 1) * size
        items = self.repo.list(skip=skip, limit=size)
        total = self.repo.count()
        pages = -(-total // size)
        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }
    
    def get_or_404(self, author_id: str) -> Author:
        author = self.repo.get_by_author_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    