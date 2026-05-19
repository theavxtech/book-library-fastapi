"""Generic repository providing common CRUD operations."""
from __future__ import annotations
from typing import Any, Generic, TypeVar
from sqlalchemy.orm import Session
from db.database import Base

ModelT = TypeVar("ModelT", bound=Base)

class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: Session) -> None:
        self.model = model
        self.session = session

    def get(self, id: int) -> ModelT | None:
        return self.session.get(self.model, id)
    
    def count(self) -> int:
        return self.session.query(self.model).count()

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        return self.session.query(self.model).offset(skip).limit(limit).all()

    def create(self, **kwargs: Any) -> ModelT:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance