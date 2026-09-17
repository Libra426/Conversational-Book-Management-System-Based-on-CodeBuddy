"""读者相关路由。"""
from fastapi import APIRouter, Depends
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


@router.get("/readers/{reader_id}", response_model=ReaderOut)
def get_reader(reader_id: int, db: Session = Depends(get_db)):
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
