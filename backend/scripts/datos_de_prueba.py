"""Crea datos de prueba para poder navegar la app real sin tener que registrarte:
un Apoderado con 2 Alumnos en cursos distintos, con Plan activo (cortesía, sin pago).

Uso:
    python scripts/datos_de_prueba.py

Idempotente: si el apoderado de prueba ya existe, no duplica nada.
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.core.db import engine
from app.core.seguridad import hashear_password
from app.models import Cuenta, Nivel, PerfilAlumno, Plan, Suscripcion

EMAIL_PRUEBA = "apoderado.prueba@logos.cl"
PASSWORD_PRUEBA = "Logos2026!"


def main() -> None:
    with Session(engine) as session:
        existente = session.exec(select(Cuenta).where(Cuenta.email == EMAIL_PRUEBA)).first()
        if existente:
            print(f"La cuenta de prueba ya existe: {EMAIL_PRUEBA}")
            return

        # Plan de cortesía para pruebas (origen "cortesia", ver
        # planificacion/18-panel-administrador.md) — acceso completo sin pago.
        plan_completo = session.exec(select(Plan).where(Plan.nombre == "Completo")).first()
        if not plan_completo:
            plan_completo = Plan(nombre="Completo", nivel_de_acceso="completo", precio_clp=19990)
            session.add(plan_completo)
            session.commit()
            session.refresh(plan_completo)

        cuenta = Cuenta(
            email=EMAIL_PRUEBA,
            password_hash=hashear_password(PASSWORD_PRUEBA),
            nombre="Apoderado de Prueba",
        )
        session.add(cuenta)
        session.commit()
        session.refresh(cuenta)

        nivel_4b = session.exec(select(Nivel).where(Nivel.nombre == "4° básico")).first()
        nivel_6b = session.exec(select(Nivel).where(Nivel.nombre == "6° básico")).first()
        if not nivel_4b or not nivel_6b:
            print("⚠️  Corre primero scripts/importar_contenido.py (faltan Nivel 4°/6° básico).")
            return

        alumno_1 = PerfilAlumno(
            cuenta_apoderado_id=cuenta.id,
            nombre="Sofía",
            apellidos="Pérez González",
            fecha_nacimiento=date(2016, 3, 12),
            rut="21.345.678-9",
            nivel_id=nivel_4b.id,
        )
        alumno_2 = PerfilAlumno(
            cuenta_apoderado_id=cuenta.id,
            nombre="Mateo",
            apellidos="Pérez González",
            fecha_nacimiento=date(2014, 7, 25),
            rut="20.987.654-3",
            nivel_id=nivel_6b.id,
        )
        session.add(alumno_1)
        session.add(alumno_2)
        session.commit()
        session.refresh(alumno_1)
        session.refresh(alumno_2)

        for alumno in (alumno_1, alumno_2):
            session.add(
                Suscripcion(
                    perfil_alumno_id=alumno.id,
                    plan_id=plan_completo.id,
                    estado="activa",
                    origen="cortesia",
                )
            )
        session.commit()

        print("Datos de prueba creados:")
        print(f"  Login apoderado → email: {EMAIL_PRUEBA}  /  password: {PASSWORD_PRUEBA}")
        print(f"  Alumno 1: {alumno_1.nombre} {alumno_1.apellidos} — 4° básico (plan activo)")
        print(f"  Alumno 2: {alumno_2.nombre} {alumno_2.apellidos} — 6° básico (plan activo)")


if __name__ == "__main__":
    main()
