from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    nationality = Column(String, nullable=True)
    birth_year = Column(Integer, nullable=True)
    books = relationship("Book", back_populates="author")
    