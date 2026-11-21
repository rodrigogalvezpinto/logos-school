"""Chequeo de salud para Render y UptimeRobot (2026-11-21): responde 200 si la API y la base de datos funcionan."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlmodel import Session

from app.core.deps import get_session

router = APIRouter(tags=["salud"])


@router.get("/salud")
def salud(session: Session = Depends(get_session)):
    try:
        session.exec(text("SELECT 1"))
    except Exception:
        return JSONResponse(status_code=503, content={"estado": "sin base de datos"})
    return {"estado": "ok"}
