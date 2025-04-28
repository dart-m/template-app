"""Роутер"""

from fastapi import APIRouter
from app.api.v1.endpoints import endpoint

router = APIRouter()

router.include_router(endpoint.router, tags=["Task"])
