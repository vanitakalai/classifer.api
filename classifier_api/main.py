from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from classifier_api.config import SERVICE_NAME, ALLOWED_HOSTS, API_PREFIX
from classifier_api.errors import http_error_handler
from classifier_api.router import router as api_router


def get_application() -> FastAPI:
    application = FastAPI(title=SERVICE_NAME)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
