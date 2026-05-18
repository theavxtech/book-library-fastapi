from pydantic import BaseModel
from typing import Optional
from schemas.author import AuthorResponse

class BookCreate(BaseModel):
    title: str
    author_name: str
    year: int

class BookResponse(BaseModel):
    id: int
    title: str
    year: int
    author: AuthorResponse

    class Config:
        from_attributes = True