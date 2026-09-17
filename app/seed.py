"""数据库初始化与默认规则/演示数据种子。"""
from sqlalchemy.orm import Session

from .database import Base, SessionLocal, engine
from .domain.enums import CardStatus, ItemStatus, ItemType, ReaderType
from .domain.models import (
    BookTitle,
    BorrowCard,
    BorrowPolicy,
    FineRule,
    LibraryItem,
    Reader,
)

DEFAULT_POLICIES: list[tuple[ReaderType, int, int]] = [
    (ReaderType.UNDERGRADUATE, 5, 30),
    (ReaderType.JUNIOR_COLLEGE, 3, 30),
    (ReaderType.GRADUATE, 10, 60),
    (ReaderType.DOCTOR, 15, 90),
    (ReaderType.TEACHER, 20, 90),
]

DEFAULT_FINES: list[tuple[ItemType, float]] = [
    (ItemType.CHINESE_BOOK, 0.10),
    (ItemType.FOREIGN_BOOK, 0.20),
    (ItemType.CHINESE_MAGAZINE, 0.05),
    (ItemType.FOREIGN_MAGAZINE, 0.10),
    (ItemType.THESIS, 0.50),
]

# 演示数据：书名/作者/isbn/出版社/类型/馆藏条码
DEMO_TITLES: list[tuple[str, str, str, str, ItemType, list[str]]] = [
    ("软件工程", "张海藩", "9787111544937", "机械工业出版社", ItemType.CHINESE_BOOK,
     ["BC-1001", "BC-1002", "BC-1003"]),
    ("算法导论", "Thomas H. Cormen", "9780262033848", "MIT Press", ItemType.FOREIGN_BOOK,
     ["BC-2001", "BC-2002"]),
    ("计算机学报", "中国计算机学会", "CN11-1826/TP", "科学出版社", ItemType.CHINESE_MAGAZINE,
     ["BC-3001"]),
    ("Nature", "Springer Nature", "0028-0836", "Nature Publishing Group", ItemType.FOREIGN_MAGAZINE,
     ["BC-4001", "BC-4002"]),
    ("基于深度学习的图像识别研究", "李明", "THESIS-0001", "武汉理工大学", ItemType.THESIS,
     ["BC-5001"]),
]

# 演示读者：姓名/院系/类型，配一张借阅证（证号 1/2/3）
DEMO_READERS: list[tuple[str, str, ReaderType]] = [
    ("张三", "计算机学院", ReaderType.UNDERGRADUATE),
    ("李四", "人工智能学院", ReaderType.GRADUATE),
    ("王五", "计算机学院", ReaderType.TEACHER),
]


def seed_policies_and_fines(db: Session) -> None:
    if db.query(BorrowPolicy).count() == 0:
        for reader_type, max_count, days in DEFAULT_POLICIES:
            db.add(BorrowPolicy(
                reader_type=reader_type,
                max_borrow_count=max_count,
                borrow_days=days,
            ))
    if db.query(FineRule).count() == 0:
        for item_type, fine_per_day in DEFAULT_FINES:
            db.add(FineRule(item_type=item_type, fine_per_day=fine_per_day))
    db.commit()


def seed_demo_data(db: Session) -> None:
    """写入演示书籍/馆藏副本/读者/借阅证（幂等：已有书目则跳过）。"""
    if db.query(BookTitle).count() > 0:
        return

    for title, author, isbn, publisher, item_type, barcodes in DEMO_TITLES:
        book = BookTitle(
            title=title, author=author, isbn=isbn, publisher=publisher, item_type=item_type
        )
        db.add(book)
        db.flush()  # 取得 book.id
        for barcode in barcodes:
            db.add(LibraryItem(barcode=barcode, title_id=book.id, status=ItemStatus.AVAILABLE))

    for idx, (name, department, reader_type) in enumerate(DEMO_READERS, start=1):
        reader = Reader(name=name, department=department, reader_type=reader_type)
        db.add(reader)
        db.flush()  # 取得 reader.id
        db.add(BorrowCard(card_no=str(idx), reader_id=reader.id, status=CardStatus.ACTIVE))

    db.commit()


def init_db() -> None:
    """创建表并写入默认规则与演示数据（幂等）。"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_policies_and_fines(db)
        seed_demo_data(db)
    finally:
        db.close()
