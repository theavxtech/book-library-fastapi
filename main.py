from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
from db.database import Base, SessionLocal, engine
from models.book import Book
from models.author import Author
from schemas.book import BookCreate, BookResponse
from schemas.author import AuthorCreate, AuthorResponse


app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")        

# ─── AUTHOR ROUTES ────────────────────────────────────────

@app.post("/authors", response_model=AuthorResponse,tags=["authors"])
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    existing_author = db.query(Author).filter(Author.name == author.name).first()
    if existing_author:
        raise HTTPException(status_code=400, detail="Author already exists")
    
    new_author = Author(
        name=author.name,
        nationality=author.nationality,
        birth_year=author.birth_year,
    )
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@app.get("/authors", response_model=list[AuthorResponse],tags=["authors"])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return authors

# ─── BOOK ROUTES ──────────────────────────────────────────

@app.post("/books", response_model=BookResponse,tags=["books"])
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.name == book.author_name).first()
    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found. Please create the author first."
        )
    new_book = Book(
        title=book.title,
        year=book.year,
        author_id=author.id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books", response_model=list[BookResponse],tags=["books"])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/search", response_model=list[BookResponse],tags=["books"])
def search_book(
    book_year: Optional[int] = None,
    book_title: Optional[str] = None,
    book_author: Optional[str] = None,
    book_id: Optional[int] = None,
    db: Session = Depends(get_db)):

    if not any([book_year, book_title, book_author, book_id]):
        raise HTTPException(status_code=400, detail="Please provide at least one search parameter")

    query = db.query(Book)
    if book_year:
        query = query.filter(Book.year == book_year)
    if book_title:
        query = query.filter(Book.title == book_title)
    if book_author:
        query = query.filter(Author.name == book_author)
    if book_id:
        query = query.filter(Book.id == book_id)

    books = query.all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found matching your search")
    return books

@app.get("/books/{book_id}", response_model=BookResponse,tags=["books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book