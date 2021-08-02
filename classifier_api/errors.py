from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)
