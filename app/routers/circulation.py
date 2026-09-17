"""借还路由（仅图书管理员）。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_librarian
from ..schemas.circulation import (
    BorrowRequest,
    FineOut,
    LoanOut,
    ReturnOut,
    ReturnRequest,
)
from ..services.circulation_service import CirculationService

router = APIRouter(prefix="/api/circulation", tags=["circulation"])


@router.post("/borrow", response_model=LoanOut, status_code=201)
def borrow_book(
    data: BorrowRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_librarian),
):
    return CirculationService(db).borrow(data)


@router.post("/return", response_model=ReturnOut)
def return_book(
    data: ReturnRequest,
    db: Session = Depends(get_db),
    _: int = Depends(require_librarian),
):
    loan, fine = CirculationService(db).return_book(data)
    fine_out = None
    if fine is not None:
        fine_out = FineOut(overdue_days=fine.overdue_days, amount=fine.amount)
    return ReturnOut(loan_id=loan.id, returned_at=loan.returned_at, fine=fine_out)
