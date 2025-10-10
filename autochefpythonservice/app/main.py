from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api import endpoints
import logging

app = FastAPI(title="AutoChef Python LLM Service")
app.include_router(endpoints.router, prefix="/api/v1")

logger = logging.getLogger("autochefpythonservice")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc}")
    return JSONResponse(status_code=400, content={"code": "BAD_REQUEST", "message": "Malformed request or invalid JSON."})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if exc.status_code >= 400 and exc.status_code < 500:
        if isinstance(detail, dict) and "code" in detail and "message" in detail:
            logger.warning(f"{detail['code']} - {detail['message']} on {request.url.path}")
            return JSONResponse(status_code=exc.status_code, content=detail)
        logger.warning(f"Client error {exc.status_code}: {detail} on {request.url.path}")
        return JSONResponse(status_code=exc.status_code, content={"code": "BAD_REQUEST", "message": str(detail)})
    logger.error(f"Server HTTP error {exc.status_code}: {detail} on {request.url.path}")
    return JSONResponse(status_code=500, content={"code": "GENERATION_FAILED", "message": "An unexpected error occurred during generation."})


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"code": "GENERATION_FAILED", "message": "An unexpected error occurred during generation."})


@app.get("/health")
async def health():
    return {"status": "ok"}
