"""Book repository — book specific database queries."""
from __future__ import annotations
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from models.book import Book
from models.author import Author


class BookRepository(BaseRepository[Book]):
    def __init__(self, session: Session) -> None:
        super().__init__(Book, session)

    def search(
        self,
        book_id: int | None = None,
        title: str | None = None,
        author_id: str | None = None,
        year: int | None = None,
        skip: int = 0,
        limit: int = 10
    ) -> list[Book]:
        query = self.session.query(Book).join(Author)

        if book_id is not None:
            query = query.filter(Book.id == book_id)
        if title is not None:
            query = query.filter(Book.title == title)
        if author_id is not None:
            query = query.filter(Author.author_id == author_id)
        if year is not None:
            query = query.filter(Book.year == year)

        return query.offset(skip).limit(limit).all()

    def search_count(
        self,
        book_id: int | None = None,
        title: str | None = None,
        author_id: str | None = None,
        year: int | None = None,
    ) -> int:
        query = self.session.query(Book).join(Author)

        if book_id is not None:
            query = query.filter(Book.id == book_id)
        if title is not None:
            query = query.filter(Book.title == title)
        if author_id is not None:
            query = query.filter(Author.author_id == author_id)
        if year is not None:
            query = query.filter(Book.year == year)

        return query.count()