"""Cuenta demo para recorrer la app completa en desarrollo (2026-11-17).

Un apoderado con un hijo en cada curso, de 1.° básico a 4.° medio (12 alumnos), todos con plan activo de cortesía
(sin pago). El botón «Entrar con la cuenta demo» del login usa estas credenciales; solo existe en la compilación de
desarrollo (environment.ts), nunca en producción (environment.prod.ts).

Uso:  python scripts/crear_cuenta_demo.py      (idempotente: completa lo que falte)
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Cuenta, Nivel, PerfilAlumno, Plan, Suscripcion
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt

EMAIL_DEMO = "demo@logos.cl"
PASSWORD_DEMO = "DemoLogos2026!"

# (nivel, nombre, año de nacimiento aproximado para la edad del curso)
HIJOS = [
    ("1° básico", "Emilia", 2019), ("2° básico", "Tomás", 2018), ("3° básico", "Isidora", 2017),
    ("4° básico", "Benjamín", 2016), ("5° básico", "Florencia", 2015), ("6° básico", "Vicente", 2014),
    ("7° básico", "Antonia", 2013), ("8° básico", "Agustín", 2012), ("1° medio", "Martina", 2011),
    ("2° medio", "Joaquín", 2010), ("3° medio", "Catalina", 2009), ("4° medio", "Maximiliano", 2008),
]


def dv(cuerpo: int) -> str:
    s, m = 0, 2
    for d in reversed(str(cuerpo)):
        s += int(d) * m
        m = 2 if m == 7 else m + 1
    r = 11 - s % 11
    return "0" if r == 11 else "K" if r == 10 else str(r)


def main() -> None:
    with Session(engine) as session:
        plan = session.exec(select(Plan).where(Plan.nombre == "Por periodo de examinación")).first()
        if not plan:
            sys.exit("Corre primero scripts/sembrar_planes.py (no hay planes).")
        cuenta = session.exec(select(Cuenta).where(Cuenta.email == EMAIL_DEMO)).first()
        if not cuenta:
            cuenta = Cuenta(email=EMAIL_DEMO, nombre="Apoderado Demo",
                            password_hash=HasheadorPasswordBcrypt().hashear(PASSWORD_DEMO))
            session.add(cuenta)
            session.commit()
            session.refresh(cuenta)
        existentes = {a.nombre for a in session.exec(select(PerfilAlumno).where(PerfilAlumno.cuenta_apoderado_id == cuenta.id))}
        for i, (nivel_nombre, nombre, anio) in enumerate(HIJOS):
            if nombre in existentes:
                continue
            nivel = session.exec(select(Nivel).where(Nivel.nombre == nivel_nombre)).first()
            if not nivel:
                sys.exit(f"Falta el nivel {nivel_nombre}: corre primero scripts/importar_contenido.py.")
            cuerpo = 24_100_000 + i * 1_111
            alumno = PerfilAlumno(cuenta_apoderado_id=cuenta.id, nombre=nombre, apellidos="Demo Logos",
                                  fecha_nacimiento=date(anio, 4, 15), rut=f"{cuerpo:,}".replace(",", ".") + f"-{dv(cuerpo)}",
                                  nivel_id=nivel.id)
            session.add(alumno)
            session.commit()
            session.refresh(alumno)
            session.add(Suscripcion(perfil_alumno_id=alumno.id, plan_id=plan.id, estado="activa", origen="cortesia"))
            session.commit()
        print(f"Cuenta demo lista: {EMAIL_DEMO} / {PASSWORD_DEMO} — {len(HIJOS)} alumnos, 1.° básico a 4.° medio, plan activo.")


if __name__ == "__main__":
    main()
