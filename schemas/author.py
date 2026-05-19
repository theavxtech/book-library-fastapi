from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    author_id: str
    name: str
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

class AuthorResponse(BaseModel):
    author_id: str
    name: str
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

class AuthorSearch(BaseModel):
    author_id: Optional[str] = None
    name: Optional[str] = None
    nationality: Optional[str] = None
    birth_year: Optional[int] = None
    
    class Config:
        from_attributes = True