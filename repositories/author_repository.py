"""Author repository — author specific database queries."""
from __future__ import annotations
from sqlalchemy.orm import Session
from repositories.base import BaseRepository
from models.author import Author


class AuthorRepository(BaseRepository[Author]):
    def __init__(self, session: Session) -> None:
        super().__init__(Author, session)

    def get_by_name(self, name: str) -> Author | None:
        return (
            self.session.query(Author)
            .filter(Author.name == name)
            .first()
        )
    def get_by_author_id(self, author_id: str) -> Author | None:
        return (
            self.session.query(Author)
            .filter(Author.author_id == author_id)
            .first()
        )