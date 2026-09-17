"""读者相关路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_identity
from ..schemas.circulation import LoanOut
from ..schemas.reader import ReaderCreate, ReaderOut
from ..schemas.reservation import ReservationOut
from ..services.circulation_service import CirculationService
from ..services.reader_service import ReaderService
from ..services.reservation_service import ReservationService

router = APIRouter(prefix="/api", tags=["readers"])


@router.post("/readers", response_model=ReaderOut, status_code=201)
def register_reader(data: ReaderCreate, db: Session = Depends(get_db)):
    return ReaderService(db).register(data)


@router.get("/readers", response_model=list[ReaderOut])
def list_readers(
    db: Session = Depends(get_db),
    identity: tuple[str, int] = Depends(get_identity),
):
    role, _ = identity
    if role not in ("librarian", "admin"):
        raise HTTPException(status_code=403, detail="需要图书管理员或系统管理员权限")
    return ReaderService(db).list_readers()


@router.get("/readers/by-card/{card_no}", response_model=ReaderOut)
def get_reader_by_card(card_no: str, db: Session = Depends(get_db)):
    return ReaderService(db).get_reader_by_card(card_no)


@router.get("/readers/{reader_id}", response_model=ReaderOut)
def get_reader(
    reader_id: int,
    db: Session = Depends(get_db),
    identity: tuple[str, int] = Depends(get_identity),
):
    role, user_id = identity
    if role not in ("librarian", "admin") and not (role == "reader" and user_id == reader_id):
        raise HTTPException(status_code=403, detail="只能查询本人信息")
    return ReaderService(db).get_reader(reader_id)


@router.get("/readers/{reader_id}/loans", response_model=list[LoanOut])
def query_loans(
    reader_id: int,
    db: Session = Depends(get_db),
    identity: tuple[str, int] = Depends(get_identity),
):
    role, user_id = identity
    return CirculationService(db).query_loans(reader_id, role, user_id)


@router.get("/readers/{reader_id}/reservations", response_model=list[ReservationOut])
def query_reservations(
    reader_id: int,
    db: Session = Depends(get_db),
    identity: tuple[str, int] = Depends(get_identity),
):
    role, user_id = identity
    return ReservationService(db).list_by_reader(reader_id, role, user_id)
