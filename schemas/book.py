from pydantic import BaseModel
from typing import Optional
from schemas.author import AuthorResponse

class BookCreate(BaseModel):
    title: str
    author_id: str
    year: int

class BookSearch(BaseModel):
    book_id: Optional[int] = None
    title: Optional[str] = None
    author_id: Optional[str] = None
    year: Optional[int] = None

class BookResponse(BaseModel):
    id: int
    title: str
    year: int
    author: AuthorResponse 

    class Config:
        from_attributes = True