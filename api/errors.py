from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class AppError(Exception):
    """우리 앱의 기본 예외"""
    def __init__(self, code: str, message: str, http_status: int = 400):
        self.code = code
        self.message = message
        self.http_status = http_status

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.http_status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

def register_error_handlers(app: FastAPI) -> None:
    """main.py에서 이 함수를 불러 핸들러를 등록"""
    app.add_exception_handler(AppError, app_error_handler)