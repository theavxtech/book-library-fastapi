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
        author_name: str | None = None,
        year: int | None = None,
    ) -> list[Book]:
        query = self.session.query(Book).join(Author)

        if book_id is not None:
            query = query.filter(Book.id == book_id)
        if title is not None:
            query = query.filter(Book.title == title)
        if author_name is not None:
            query = query.filter(Author.name == author_name)
        if year is not None:
            query = query.filter(Book.year == year)

        return query.all()