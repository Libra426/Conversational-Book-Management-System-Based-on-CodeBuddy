"""表现层权限依赖：基于角色的简单权限校验。

身份来源（二选一，Bearer 优先）：
- /docs 右上角 Authorize 按钮填入 Bearer 令牌，令牌即角色：
  `reader` / `librarian` / `admin`，可带用户 id，如 `admin:1`。
- 请求头 `X-Role` / `X-User-Id`（未填时默认 reader / 0），保留向后兼容。
"""
from fastapi import Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer(
    auto_error=False,
    description="登录角色：reader / librarian / admin；可带用户 id，如 admin:1",
)


def _resolve_identity(
    x_role: str,
    x_user_id: int,
    credentials: HTTPAuthorizationCredentials | None,
) -> tuple[str, int]:
    """Bearer 令牌优先，否则回退到请求头。"""
    if credentials is not None:
        token = credentials.credentials
        if ":" in token:
            role, _, uid = token.partition(":")
            return role, int(uid)
        return token, x_user_id
    return x_role, x_user_id


def get_identity(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    x_role: str = Header(default="reader"),
    x_user_id: int = Header(default=0),
) -> tuple[str, int]:
    """返回 (角色, 用户 id)，供需要区分角色但不锁定单一角色的接口使用。"""
    return _resolve_identity(x_role, x_user_id, credentials)


def require_role(role: str):
    """返回一个 FastAPI 依赖，校验当前角色是否为指定值。"""

    def _dependency(identity: tuple[str, int] = Depends(get_identity)) -> int:
        actual_role, actual_uid = identity
        if actual_role != role:
            raise HTTPException(status_code=403, detail=f"需要 {role} 权限")
        return actual_uid

    return _dependency


require_librarian = require_role("librarian")
require_admin = require_role("admin")
