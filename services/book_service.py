"""Book service — book business logic."""
from __future__ import annotations
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.book_repository import BookRepository
from repositories.author_repository import AuthorRepository
from schemas.book import BookCreate
from models.book import Book


class BookService:
    def __init__(self, session: Session) -> None:
        self.repo = BookRepository(session)
        self.author_repo = AuthorRepository(session)

    def create(self, payload: BookCreate) -> Book:
        author = self.author_repo.get_by_name(payload.author_name)
        if not author:
            raise HTTPException(
                status_code=404,
                detail="Author not found. Please create the author first."
            )
        return self.repo.create(
            title=payload.title,
            year=payload.year,
            author_id=author.id
        )

    def get_all(self) -> list[Book]:
        return self.repo.list()

    def get_or_404(self, book_id: int) -> Book:
        book = self.repo.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def search(
        self,
        book_id: int | None = None,
        title: str | None = None,
        author_name: str | None = None,
        year: int | None = None,
    ) -> list[Book]:
        if not any([book_id, title, author_name, year]):
            raise HTTPException(
                status_code=400,
                detail="Please provide at least one search parameter"
            )
        books = self.repo.search(
            book_id=book_id,
            title=title,
            author_name=author_name,
            year=year
        )
        if not books:
            raise HTTPException(
                status_code=404,
                detail="No books found matching your search"
            )
        return books