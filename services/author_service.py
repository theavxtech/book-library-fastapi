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
        existing = self.repo.get_by_name(payload.name)
        if existing:
            raise HTTPException(status_code=400, detail="Author already exists")
        return self.repo.create(
            name=payload.name,
            nationality=payload.nationality,
            birth_year=payload.birth_year
        )

    def get_all(self) -> list[Author]:
        return self.repo.list()