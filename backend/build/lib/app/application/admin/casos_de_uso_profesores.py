"""Aprobación de cuentas de Profesor desde el panel Admin ya existente — ver
planificacion/01-roles-y-permisos.md: la identidad del Profesor la revisa manualmente un
Administrador antes de activar la cuenta. Archivo separado de application/admin/casos_de_uso.py
(que solo tiene el login de CuentaAdmin) para no mezclar los dos temas."""

from app.domain.profesor.entities import CuentaProfesor
from app.domain.profesor.exceptions import CuentaProfesorNoEncontrada
from app.domain.profesor.ports import RepositorioCuentasProfesor


class ListarProfesoresPendientes:
    def __init__(self, repositorio: RepositorioCuentasProfesor):
        self._repositorio = repositorio

    def ejecutar(self) -> list[CuentaProfesor]:
        return self._repositorio.listar_pendientes()


class AprobarProfesor:
    def __init__(self, repositorio: RepositorioCuentasProfesor):
        self._repositorio = repositorio

    def ejecutar(self, cuenta_profesor_id: int) -> CuentaProfesor:
        cuenta = self._repositorio.buscar_por_id(cuenta_profesor_id)
        if not cuenta:
            raise CuentaProfesorNoEncontrada()
        cuenta.aprobar()
        return self._repositorio.guardar(cuenta)


class RechazarProfesor:
    def __init__(self, repositorio: RepositorioCuentasProfesor):
        self._repositorio = repositorio

    def ejecutar(self, cuenta_profesor_id: int) -> CuentaProfesor:
        cuenta = self._repositorio.buscar_por_id(cuenta_profesor_id)
        if not cuenta:
            raise CuentaProfesorNoEncontrada()
        cuenta.rechazar()
        return self._repositorio.guardar(cuenta)
