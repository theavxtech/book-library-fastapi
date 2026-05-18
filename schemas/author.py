from pydantic import BaseModel
from typing import Optional

class AuthorCreate(BaseModel):
    name: str
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

class AuthorResponse(BaseModel):
    id: int
    name: str
    nationality: Optional[str] = None
    birth_year: Optional[int] = None

    class Config:
        from_attributes = True