from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter
from app.core.logging_config import LoggingMiddleware, configurar_logging
from app.routers import admin_auth, auth, comercial, contenido, evaluaciones, progreso

configurar_logging()

app = FastAPI(
    title="Logos API",
    description="Backend de la plataforma de preparación para Exámenes Libres (Mineduc, Chile).",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    # En Desarrollo, el frontend corre en localhost:4300 (ver planificacion/17-...).
    # En Producción se restringe al dominio real cuando exista.
    allow_origins=["http://localhost:4300", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contenido.router)
app.include_router(evaluaciones.router)
app.include_router(progreso.router)
app.include_router(admin_auth.router)
app.include_router(comercial.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
