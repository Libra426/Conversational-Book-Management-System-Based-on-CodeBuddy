"""图书标题与馆藏副本仓储。"""
from sqlalchemy.orm import Session

from ..domain.models import BookTitle, LibraryItem


class BookTitleRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, title_id: int) -> BookTitle | None:
        return self.db.get(BookTitle, title_id)

    def find_by_isbn(self, isbn: str) -> BookTitle | None:
        return self.db.query(BookTitle).filter(BookTitle.isbn == isbn).first()

    def search(self, title: str | None, author: str | None, isbn: str | None):
        q = self.db.query(BookTitle)
        if title:
            q = q.filter(BookTitle.title.contains(title))
        if author:
            q = q.filter(BookTitle.author.contains(author))
        if isbn:
            q = q.filter(BookTitle.isbn == isbn)
        return q.all()

    def create(self, title: BookTitle) -> BookTitle:
        self.db.add(title)
        self.db.flush()
        return title

    def delete(self, title: BookTitle) -> None:
        self.db.delete(title)
        self.db.flush()


class LibraryItemRepo:
    def __init__(self, db: Session):
        self.db = db

    def find_by_barcode(self, barcode: str) -> LibraryItem | None:
        return self.db.query(LibraryItem).filter(LibraryItem.barcode == barcode).first()

    def create(self, item: LibraryItem) -> LibraryItem:
        self.db.add(item)
        self.db.flush()
        return item
