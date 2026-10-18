from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.limiter import limiter
from app.core.logging_config import LoggingMiddleware, configurar_logging
from app.core.security_headers import SecurityHeadersMiddleware
from app.routers import (
    admin_auth,
    admin_evaluaciones,
    admin_profesores,
    apoderado,
    auth,
    bienestar,
    calificaciones,
    comercial,
    contenido,
    curso_seccion,
    evaluaciones,
    gamificacion,
    notificaciones,
    onboarding,
    plan_estudio,
    plan_lector,
    prediccion,
    profesor_auth,
    progreso,
    sugerencias,
    utiles_escolares,
)

configurar_logging()

app = FastAPI(
    title="Logos API",
    description="Backend de la plataforma de preparación para Exámenes Libres (Mineduc, Chile).",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Auditoría de seguridad (2026-08-17): sin este middleware, `default_limits` del Limiter
# nunca se aplica — solo los endpoints decorados explícitamente con `@limiter.limit(...)`
# quedaban protegidos. Con esto, TODO endpoint tiene una red de seguridad por defecto.
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
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
app.include_router(apoderado.router)
app.include_router(contenido.router)
app.include_router(evaluaciones.router)
app.include_router(progreso.router)
app.include_router(admin_auth.router)
app.include_router(comercial.router)
app.include_router(plan_estudio.router)
app.include_router(profesor_auth.router)
app.include_router(curso_seccion.router)
app.include_router(admin_profesores.router)
app.include_router(admin_evaluaciones.router)
app.include_router(gamificacion.router)
app.include_router(onboarding.router)
app.include_router(bienestar.router)
app.include_router(plan_lector.router)
app.include_router(utiles_escolares.router)
app.include_router(notificaciones.router)
app.include_router(sugerencias.router)
app.include_router(calificaciones.router)
app.include_router(prediccion.router)


@app.get("/salud")
def salud():
    return {"estado": "ok"}
