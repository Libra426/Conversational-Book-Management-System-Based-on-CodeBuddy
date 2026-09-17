"""领域枚举。"""
import enum


class ReaderType(str, enum.Enum):
    UNDERGRADUATE = "UNDERGRADUATE"    # 本科生
    JUNIOR_COLLEGE = "JUNIOR_COLLEGE"  # 专科生
    GRADUATE = "GRADUATE"              # 研究生
    DOCTOR = "DOCTOR"                  # 博士生
    TEACHER = "TEACHER"                # 教师


class ItemType(str, enum.Enum):
    CHINESE_BOOK = "CHINESE_BOOK"              # 中文图书
    FOREIGN_BOOK = "FOREIGN_BOOK"              # 外文图书
    CHINESE_MAGAZINE = "CHINESE_MAGAZINE"      # 中文杂志
    FOREIGN_MAGAZINE = "FOREIGN_MAGAZINE"      # 外文杂志
    THESIS = "THESIS"                          # 论文


class ItemStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    BORROWED = "BORROWED"
    RESERVED = "RESERVED"
    REMOVED = "REMOVED"


class LoanStatus(str, enum.Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class CardStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"


class ReservationStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"


class FineStatus(str, enum.Enum):
    UNPAID = "UNPAID"
    PAID = "PAID"
