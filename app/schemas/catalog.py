"""图书与馆藏 DTO。"""
from pydantic import BaseModel, ConfigDict

from ..domain.enums import ItemStatus, ItemType


class BookTitleCreate(BaseModel):
    title: str
    author: str
    isbn: str
    publisher: str | None = None
    item_type: ItemType


class BookTitleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str
    publisher: str | None = None
    item_type: ItemType
    total_count: int
    available_count: int


class LibraryItemCreate(BaseModel):
    title_id: int
    barcode: str


class LibraryItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    barcode: str
    title_id: int
    status: ItemStatus
