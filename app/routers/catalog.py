"""图书查询路由。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.catalog import BookTitleOut
from ..services.catalog_service import CatalogService

router = APIRouter(prefix="/api", tags=["catalog"])


@router.get("/catalog/books", response_model=list[BookTitleOut])
def search_books(
    title: str | None = None,
    author: str | None = None,
    isbn: str | None = None,
    db: Session = Depends(get_db),
):
    return CatalogService(db).search(title, author, isbn)
