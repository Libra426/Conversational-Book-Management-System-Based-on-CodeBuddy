"""管理员与规则维护 DTO。"""
from pydantic import BaseModel

from ..domain.enums import ItemType, ReaderType


class BorrowPolicyUpsert(BaseModel):
    reader_type: ReaderType
    max_borrow_count: int
    borrow_days: int


class FineRuleUpsert(BaseModel):
    item_type: ItemType
    fine_per_day: float


class LibrarianCreate(BaseModel):
    name: str


class SystemAdminCreate(BaseModel):
    name: str
