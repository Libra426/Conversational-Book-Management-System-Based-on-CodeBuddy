"""领域异常体系：统一携带 HTTP 状态码与语义化 code。"""


class DomainError(Exception):
    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class PermissionDeniedError(DomainError):
    status_code = 403
    code = "PERMISSION_DENIED"


class ConflictError(DomainError):
    status_code = 409
    code = "CONFLICT"


# 借书/还书相关
class InvalidCardError(PermissionDeniedError):
    code = "INVALID_CARD"


class TooManyLoansError(ConflictError):
    code = "TOO_MANY_LOANS"


class OverdueLoanError(ConflictError):
    code = "OVERDUE_LOAN"


class ItemNotBorrowableError(ConflictError):
    code = "ITEM_NOT_BORROWABLE"


class ItemNotFoundError(NotFoundError):
    code = "ITEM_NOT_FOUND"


class LoanNotFoundError(NotFoundError):
    code = "LOAN_NOT_FOUND"


# 读者/预约/馆藏相关
class ReaderNotFoundError(NotFoundError):
    code = "READER_NOT_FOUND"


class TitleNotFoundError(NotFoundError):
    code = "TITLE_NOT_FOUND"


class DuplicateReservationError(ConflictError):
    code = "DUPLICATE_RESERVATION"


class DuplicateCardError(ConflictError):
    code = "DUPLICATE_CARD"


class DuplicateIsbnError(ConflictError):
    code = "DUPLICATE_ISBN"


class DuplicateBarcodeError(ConflictError):
    code = "DUPLICATE_BARCODE"


class PolicyNotFoundError(NotFoundError):
    code = "POLICY_NOT_FOUND"
