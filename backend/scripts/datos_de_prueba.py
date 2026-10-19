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

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Cuenta, CuentaAdmin, Nivel, PerfilAlumno, Plan, Suscripcion
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt

EMAIL_PRUEBA = "apoderado.prueba@logos.cl"
PASSWORD_PRUEBA = "Logos2026!"
ADMIN_EMAIL_PRUEBA = "admin.prueba@logos.cl"
ADMIN_PASSWORD_PRUEBA = "AdminLogos2026!"


def main() -> None:
    with Session(engine) as session:
        # Cuenta Admin de prueba (usada por suite E2E e2e/admin.spec.ts y accesibilidad)
        admin_existente = session.exec(select(CuentaAdmin).where(CuentaAdmin.email == ADMIN_EMAIL_PRUEBA)).first()
        if not admin_existente:
            admin = CuentaAdmin(
                email=ADMIN_EMAIL_PRUEBA,
                nombre="Administrador de Prueba",
                password_hash=HasheadorPasswordBcrypt().hashear(ADMIN_PASSWORD_PRUEBA),
            )
            session.add(admin)
            session.commit()
            print(f"Cuenta admin de prueba creada: {ADMIN_EMAIL_PRUEBA}")

        existente = session.exec(select(Cuenta).where(Cuenta.email == EMAIL_PRUEBA)).first()
        if existente:
            print(f"La cuenta de apoderado de prueba ya existe: {EMAIL_PRUEBA}")
            return

        # Usa el plan real "Por periodo de examinación" (ver scripts/sembrar_planes.py y
        # planificacion/09-modelo-de-negocio.md), asignado en origen "cortesia" — acceso
        # completo sin pago real, tal como pediste para las cuentas de prueba.
        plan_completo = session.exec(select(Plan).where(Plan.nombre == "Por periodo de examinación")).first()
        if not plan_completo:
            print("⚠️  Corre primero scripts/sembrar_planes.py (no hay planes creados).")
            return

        cuenta = Cuenta(
            email=EMAIL_PRUEBA,
            password_hash=HasheadorPasswordBcrypt().hashear(PASSWORD_PRUEBA),
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
            rut="21.345.678-4",
            nivel_id=nivel_4b.id,
        )
        alumno_2 = PerfilAlumno(
            cuenta_apoderado_id=cuenta.id,
            nombre="Mateo",
            apellidos="Pérez González",
            fecha_nacimiento=date(2014, 7, 25),
            rut="20.987.654-K",
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
