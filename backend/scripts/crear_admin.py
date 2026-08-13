"""Crea una cuenta del panel de administración comercial (planificacion/18-panel-
administrador.md). No existe endpoint público de registro a propósito — este script es el
único punto de entrada, para que solo el dueño del proyecto (o quien él ejecute esto por
encargo) pueda crear cuentas admin.

Uso:
    python scripts/crear_admin.py
"""

import sys
from getpass import getpass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import crear_tablas, engine
from app.infrastructure.persistence.orm_models import CuentaAdmin
from app.infrastructure.seguridad.bcrypt_hasheador import HasheadorPasswordBcrypt


def main() -> None:
    crear_tablas()
    email = input("Email de la cuenta admin: ").strip()
    nombre = input("Nombre: ").strip()
    password = getpass("Password: ")
    password_confirmacion = getpass("Confirma el password: ")

    if password != password_confirmacion:
        print("Los passwords no coinciden.")
        return

    with Session(engine) as session:
        existente = session.exec(select(CuentaAdmin).where(CuentaAdmin.email == email)).first()
        if existente:
            print(f"Ya existe una cuenta admin con el correo {email}.")
            return

        cuenta = CuentaAdmin(
            email=email, nombre=nombre, password_hash=HasheadorPasswordBcrypt().hashear(password)
        )
        session.add(cuenta)
        session.commit()
        print(f"Cuenta admin creada: {email}")


if __name__ == "__main__":
    main()
