from app.domain.admin.exceptions import CredencialesAdminInvalidas
from app.domain.admin.ports import RepositorioCuentasAdmin, ServicioTokenAdmin
from app.domain.auth.ports import HasheadorPassword


class IniciarSesionAdmin:
    def __init__(
        self,
        repositorio_cuentas_admin: RepositorioCuentasAdmin,
        hasheador: HasheadorPassword,
        servicio_token: ServicioTokenAdmin,
    ):
        self._repositorio_cuentas_admin = repositorio_cuentas_admin
        self._hasheador = hasheador
        self._servicio_token = servicio_token

    def ejecutar(self, email: str, password: str) -> str:
        cuenta = self._repositorio_cuentas_admin.buscar_por_email(email)
        if not cuenta or not self._hasheador.verificar(password, cuenta.password_hash):
            raise CredencialesAdminInvalidas()
        return self._servicio_token.generar_admin(cuenta.id)
