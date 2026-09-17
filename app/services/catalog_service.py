"""图书标题与馆藏副本应用服务。"""
from sqlalchemy.orm import Session

from ..domain.enums import ItemStatus
from ..domain.models import BookTitle, LibraryItem
from ..exceptions import (
    DuplicateBarcodeError,
    DuplicateIsbnError,
    ItemNotFoundError,
    TitleNotFoundError,
)
from ..repositories.catalog_repo import BookTitleRepo, LibraryItemRepo
from ..schemas.catalog import BookTitleCreate, LibraryItemCreate


class CatalogService:
    def __init__(self, db: Session):
        self.db = db
        self.title_repo = BookTitleRepo(db)
        self.item_repo = LibraryItemRepo(db)

    def search(self, title: str | None, author: str | None, isbn: str | None) -> list[BookTitle]:
        return self.title_repo.search(title, author, isbn)

    def add_title(self, data: BookTitleCreate) -> BookTitle:
        if self.title_repo.find_by_isbn(data.isbn) is not None:
            raise DuplicateIsbnError("ISBN 已存在")
        title = BookTitle(
            title=data.title,
            author=data.author,
            isbn=data.isbn,
            publisher=data.publisher,
            item_type=data.item_type,
        )
        self.title_repo.create(title)
        self.db.commit()
        return title

    def delete_title(self, title_id: int) -> None:
        title = self.title_repo.get(title_id)
        if title is None:
            raise TitleNotFoundError("标题不存在")
        self.title_repo.delete(title)
        self.db.commit()

    def add_item(self, data: LibraryItemCreate) -> LibraryItem:
        if self.title_repo.get(data.title_id) is None:
            raise TitleNotFoundError("标题不存在")
        if self.item_repo.find_by_barcode(data.barcode) is not None:
            raise DuplicateBarcodeError("条码已存在")
        item = LibraryItem(
            barcode=data.barcode,
            title_id=data.title_id,
            status=ItemStatus.AVAILABLE,
        )
        self.item_repo.create(item)
        self.db.commit()
        return item

    def remove_item(self, barcode: str) -> LibraryItem:
        item = self.item_repo.find_by_barcode(barcode)
        if item is None:
            raise ItemNotFoundError("馆藏副本不存在")
        item.status = ItemStatus.REMOVED
        self.db.commit()
        return item
