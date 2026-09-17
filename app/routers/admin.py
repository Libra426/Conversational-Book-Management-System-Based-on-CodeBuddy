"""系统管理员路由（权限：admin）。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_admin
from ..schemas.admin import (
    BorrowPolicyUpsert,
    FineRuleUpsert,
    LibrarianCreate,
    SystemAdminCreate,
)
from ..schemas.catalog import BookTitleCreate, BookTitleOut, LibraryItemCreate, LibraryItemOut
from ..schemas.reader import BorrowCardOut, IssueCardRequest
from ..services.admin_service import AdminService
from ..services.catalog_service import CatalogService
from ..services.fine_service import FineService
from ..services.policy_service import BorrowPolicyService
from ..services.reader_service import ReaderService

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/borrow-cards", response_model=BorrowCardOut, status_code=201)
def issue_card(
    data: IssueCardRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    return ReaderService(db).issue_card(data.reader_id)


@router.delete("/borrow-cards/{card_no}", response_model=BorrowCardOut)
def revoke_card(
    card_no: str,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    return ReaderService(db).revoke_card(card_no)


@router.post("/book-titles", response_model=BookTitleOut, status_code=201)
def add_title(
    data: BookTitleCreate,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    return CatalogService(db).add_title(data)


@router.delete("/book-titles/{title_id}", status_code=204)
def delete_title(
    title_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    CatalogService(db).delete_title(title_id)


@router.post("/library-items", response_model=LibraryItemOut, status_code=201)
def add_item(
    data: LibraryItemCreate,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    return CatalogService(db).add_item(data)


@router.delete("/library-items/{barcode}", response_model=LibraryItemOut)
def remove_item(
    barcode: str,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    return CatalogService(db).remove_item(barcode)


@router.post("/borrow-policies", status_code=200)
def upsert_policy(
    data: BorrowPolicyUpsert,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    policy = BorrowPolicyService(db).upsert(data)
    return {
        "reader_type": policy.reader_type.value,
        "max_borrow_count": policy.max_borrow_count,
        "borrow_days": policy.borrow_days,
    }


@router.post("/fine-rules", status_code=200)
def upsert_fine_rule(
    data: FineRuleUpsert,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    rule = FineService(db).upsert(data)
    return {"item_type": rule.item_type.value, "fine_per_day": rule.fine_per_day}


@router.post("/librarians", status_code=201)
def add_librarian(
    data: LibrarianCreate,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    librarian = AdminService(db).add_librarian(data.name)
    return {"id": librarian.id, "name": librarian.name}


@router.delete("/librarians/{librarian_id}", status_code=204)
def delete_librarian(
    librarian_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    AdminService(db).delete_librarian(librarian_id)


@router.post("/system-admins", status_code=201)
def add_system_admin(
    data: SystemAdminCreate,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    admin = AdminService(db).add_system_admin(data.name)
    return {"id": admin.id, "name": admin.name}


@router.delete("/system-admins/{admin_id}", status_code=204)
def delete_system_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    _: int = Depends(require_admin),
):
    AdminService(db).delete_system_admin(admin_id)
