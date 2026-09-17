"""预约应用服务。"""
from sqlalchemy.orm import Session

from ..domain.enums import ReservationStatus
from ..domain.models import Reservation
from ..exceptions import (
    DuplicateReservationError,
    PermissionDeniedError,
    ReaderNotFoundError,
    TitleNotFoundError,
)
from ..repositories.catalog_repo import BookTitleRepo
from ..repositories.reader_repo import ReaderRepo
from ..repositories.reservation_repo import ReservationRepo
from ..schemas.reservation import ReservationRequest


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.reader_repo = ReaderRepo(db)
        self.title_repo = BookTitleRepo(db)
        self.res_repo = ReservationRepo(db)

    def reserve(self, data: ReservationRequest) -> Reservation:
        if self.reader_repo.get(data.reader_id) is None:
            raise ReaderNotFoundError("读者不存在")
        if self.title_repo.get(data.title_id) is None:
            raise TitleNotFoundError("标题不存在")
        if self.res_repo.find_active(data.reader_id, data.title_id) is not None:
            raise DuplicateReservationError("重复预约")

        reservation = Reservation(
            reader_id=data.reader_id,
            title_id=data.title_id,
            status=ReservationStatus.ACTIVE,
        )
        self.res_repo.create(reservation)
        self.db.commit()
        return reservation

    def list_by_reader(self, reader_id: int, role: str, user_id: int) -> list[Reservation]:
        if role not in ("librarian", "admin") and not (role == "reader" and user_id == reader_id):
            raise PermissionDeniedError("只能查询本人预约信息")
        return self.res_repo.list_by_reader(reader_id)
