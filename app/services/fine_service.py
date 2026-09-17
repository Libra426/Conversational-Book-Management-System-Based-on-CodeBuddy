"""罚款规则策略（Strategy）：按借出物类型计算每日罚款。"""
from datetime import date

from sqlalchemy.orm import Session

from ..domain.enums import ItemType
from ..domain.models import FineRule
from ..exceptions import PolicyNotFoundError
from ..schemas.admin import FineRuleUpsert


class FineService:
    def __init__(self, db: Session):
        self.db = db

    def get_rule(self, item_type: ItemType) -> FineRule:
        rule = self.db.query(FineRule).filter(FineRule.item_type == item_type).first()
        if rule is None:
            raise PolicyNotFoundError(f"缺少借出物类型 {item_type} 的罚款规则")
        return rule

    def overdue_days(self, due_date: date, return_date: date) -> int:
        return (return_date - due_date).days

    def calculate_fine(self, item_type: ItemType, overdue_days: int) -> float:
        return self.get_rule(item_type).calculate(overdue_days)

    def list_all(self) -> list[FineRule]:
        return self.db.query(FineRule).order_by(FineRule.id).all()

    def upsert(self, data: FineRuleUpsert) -> FineRule:
        rule = self.db.query(FineRule).filter(FineRule.item_type == data.item_type).first()
        if rule is None:
            rule = FineRule(item_type=data.item_type)
            self.db.add(rule)
        rule.fine_per_day = data.fine_per_day
        self.db.commit()
        return rule
