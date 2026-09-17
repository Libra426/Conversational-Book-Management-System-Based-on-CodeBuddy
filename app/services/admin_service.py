"""系统管理员维护服务。"""
from sqlalchemy.orm import Session

from ..domain.models import Librarian, SystemAdmin
from ..exceptions import NotFoundError


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def add_librarian(self, name: str) -> Librarian:
        librarian = Librarian(name=name)
        self.db.add(librarian)
        self.db.commit()
        return librarian

    def delete_librarian(self, librarian_id: int) -> None:
        librarian = self.db.get(Librarian, librarian_id)
        if librarian is None:
            raise NotFoundError("图书管理员不存在")
        self.db.delete(librarian)
        self.db.commit()

    def add_system_admin(self, name: str) -> SystemAdmin:
        admin = SystemAdmin(name=name)
        self.db.add(admin)
        self.db.commit()
        return admin

    def delete_system_admin(self, admin_id: int) -> None:
        admin = self.db.get(SystemAdmin, admin_id)
        if admin is None:
            raise NotFoundError("系统管理员不存在")
        self.db.delete(admin)
        self.db.commit()
