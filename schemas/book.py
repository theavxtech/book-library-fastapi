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

class BookSearch(BaseModel):
    title: Optional[str] = None
    author_name: Optional[str] = None
    year: Optional[int] = None
    book_id: Optional[int] = None    

    class Config:
        from_attributes = True