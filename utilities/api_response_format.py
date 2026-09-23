from fastapi.responses import JSONResponse
from typing import Any, Optional


def api_response_format(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200,
):
    payload = {
        "message": message,
        "data": data if data is not None else {},
    }
    return JSONResponse(content=payload, status_code=status_code)