"""管理员与规则维护 DTO。"""
from pydantic import BaseModel, ConfigDict, Field

from ..domain.enums import ItemType, ReaderType


class BorrowPolicyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reader_type: ReaderType
    max_borrow_count: int
    borrow_days: int


class FineRuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_type: ItemType
    fine_per_day: float


class StaffOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BorrowPolicyUpsert(BaseModel):
    reader_type: ReaderType
    max_borrow_count: int = Field(ge=0)
    borrow_days: int = Field(ge=0)


class FineRuleUpsert(BaseModel):
    item_type: ItemType
    fine_per_day: float = Field(ge=0)


class LibrarianCreate(BaseModel):
    name: str


class SystemAdminCreate(BaseModel):
    name: str
