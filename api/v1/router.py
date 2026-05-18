"""V1 API router — combines all routes."""
from __future__ import annotations
from fastapi import APIRouter
from api.v1.authors import router as authors_router
from api.v1.books import router as books_router

router = APIRouter(prefix="/api/v1")

router.include_router(authors_router)
router.include_router(books_router)