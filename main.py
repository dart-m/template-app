"""Модуль запуска приложения"""

from fastapi import FastAPI
from app.api.v1.api import router as api_router
from app.core.logger import logger

import uvicorn


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    logger.info("MAIN : Launch app")
    uvicorn.run("main:app", host="0.0.0.0", port=5005, log_level="info")
