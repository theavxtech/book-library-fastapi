"""Book service — book business logic."""
from __future__ import annotations
from fastapi import HTTPException
from sqlalchemy.orm import Session
from repositories.book_repository import BookRepository
from schemas.book import BookCreate , BookSearch
from models.book import Book
from services.author_service import AuthorService


class BookService:
    def __init__(self, session: Session) -> None:
        self.repo = BookRepository(session)
        self.author_service = AuthorService(session)

    def create(self, payload: BookCreate) -> Book:
        author = self.author_service.get_or_404(payload.author_id)
        return self.repo.create(
            title=payload.title,
            year=payload.year,
            author_id=author.author_id
        )

    def get_all(self) -> list[Book]:
        return self.repo.list()

    def get_or_404(self, book_id: int) -> Book:
        book = self.repo.get(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def search(self, payload: BookSearch) -> list[Book]:
        if not any([
            payload.book_id is not None,
            payload.title is not None,
            payload.author_id is not None,
            payload.year is not None
        ]):
            raise HTTPException(
                status_code=400,
                detail="Please provide at least one search parameter"
            )
        books = self.repo.search(
            book_id=payload.book_id,
            title=payload.title,
            author_id=payload.author_id,
            year=payload.year
        )
        if not books:
            raise HTTPException(
                status_code=404,
                detail="No books found matching your search"
            )
        return books