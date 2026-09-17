"""应用入口：装配 FastAPI、全局异常处理与路由。"""
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# 允许直接 `python app/main.py` 运行：脚本方式下 __package__ 为 None，
# 把项目根目录加入 sys.path，使下面的 `from app.* import ...` 绝对导入可解析。
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.exceptions import DomainError
from app.routers import admin, catalog, circulation, readers, reservations
from app.seed import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="图书管理系统", version="1.0.0", lifespan=lifespan)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


app.include_router(readers.router)
app.include_router(catalog.router)
app.include_router(circulation.router)
app.include_router(reservations.router)
app.include_router(admin.router)

# 简单前端页面（可选）：访问 http://127.0.0.1:8000/ 即可使用。
# 如需移除前端，删除 static/ 目录并删掉下面两处即可，不影响任何 API。
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
