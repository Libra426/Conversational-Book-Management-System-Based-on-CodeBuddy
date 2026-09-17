"""策略单元测试：借阅规则与罚款规则。"""
from datetime import date

from app.domain.enums import ItemType, ReaderType
from app.services.fine_service import FineService
from app.services.policy_service import BorrowPolicyService


def test_borrow_policy_defaults(db):
    svc = BorrowPolicyService(db)
    assert svc.get_max_borrow_count(ReaderType.UNDERGRADUATE) == 5
    assert svc.get_borrow_days(ReaderType.UNDERGRADUATE) == 30
    assert svc.get_max_borrow_count(ReaderType.JUNIOR_COLLEGE) == 3
    assert svc.get_borrow_days(ReaderType.JUNIOR_COLLEGE) == 30
    assert svc.get_max_borrow_count(ReaderType.GRADUATE) == 10
    assert svc.get_borrow_days(ReaderType.GRADUATE) == 60
    assert svc.get_max_borrow_count(ReaderType.DOCTOR) == 15
    assert svc.get_borrow_days(ReaderType.DOCTOR) == 90
    assert svc.get_max_borrow_count(ReaderType.TEACHER) == 20
    assert svc.get_borrow_days(ReaderType.TEACHER) == 90


def test_borrow_policy_can_borrow(db):
    svc = BorrowPolicyService(db)
    assert svc.can_borrow(ReaderType.UNDERGRADUATE, 4) is True
    assert svc.can_borrow(ReaderType.UNDERGRADUATE, 5) is False


def test_due_date(db):
    svc = BorrowPolicyService(db)
    assert svc.due_date(ReaderType.UNDERGRADUATE, date(2025, 1, 1)) == date(2025, 1, 31)


def test_fine_rule_defaults(db):
    svc = FineService(db)
    assert svc.calculate_fine(ItemType.CHINESE_BOOK, 5) == 0.5
    assert svc.calculate_fine(ItemType.FOREIGN_BOOK, 5) == 1.0
    assert svc.calculate_fine(ItemType.CHINESE_MAGAZINE, 5) == 0.25
    assert svc.calculate_fine(ItemType.THESIS, 5) == 2.5


def test_fine_zero_or_negative(db):
    svc = FineService(db)
    assert svc.calculate_fine(ItemType.CHINESE_BOOK, 0) == 0.0
    assert svc.calculate_fine(ItemType.CHINESE_BOOK, -3) == 0.0
