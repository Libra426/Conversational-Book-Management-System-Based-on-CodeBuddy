"""预约仓储。"""
from sqlalchemy.orm import Session

from ..domain.enums import ReservationStatus
from ..domain.models import Reservation


class ReservationRepo:
    def __init__(self, db: Session):
        self.db = db

    def find_active(self, reader_id: int, title_id: int) -> Reservation | None:
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.reader_id == reader_id,
                Reservation.title_id == title_id,
                Reservation.status == ReservationStatus.ACTIVE,
            )
            .first()
        )

    def list_by_reader(self, reader_id: int) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.reader_id == reader_id)
            .order_by(Reservation.created_at.asc())
            .all()
        )

    def create(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.flush()
        return reservation
