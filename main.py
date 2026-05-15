from fastapi import FastAPI, Depends,HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.database import SessionLocal, engine
import models.models as models, schemas.schemas as schemas
from typing import Optional

app = FastAPI()

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.get("/books/search", response_model=list[schemas.BookResponse])
def search_book(
    book_year: Optional[int] = None,
    book_title: Optional[str] = None,
    book_author: Optional[str] = None,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)):

    if not any([book_year, book_title, book_author, book_id]):
        raise HTTPException(status_code=400, detail="Please provide at least one search parameter")

    query = db.query(models.Book)
    if book_year:
        query = query.filter(models.Book.year == book_year)
    if book_title:
        query = query.filter(models.Book.title == book_title)
    if book_author:
        query = query.filter(models.Book.author == book_author)
    if book_id:
        query = query.filter(models.Book.id == book_id)

    books = query.all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found matching your search")

    return books

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        return {"error": "Book not found"}
    return book
