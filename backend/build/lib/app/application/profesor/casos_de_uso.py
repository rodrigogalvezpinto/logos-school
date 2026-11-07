from app.domain.auth.ports import HasheadorPassword
from app.domain.profesor.entities import CuentaProfesor
from app.domain.profesor.exceptions import CorreoYaRegistrado, CredencialesProfesorInvalidas
from app.domain.profesor.ports import RepositorioCuentasProfesor, ServicioTokenProfesor


class RegistrarProfesor:
    def __init__(
        self,
        repositorio: RepositorioCuentasProfesor,
        hasheador: HasheadorPassword,
        servicio_token: ServicioTokenProfesor,
    ):
        self._repositorio = repositorio
        self._hasheador = hasheador
        self._servicio_token = servicio_token

    def ejecutar(self, email: str, password: str, nombre: str) -> str:
        email = email.strip().lower()
        if self._repositorio.buscar_por_email(email):
            raise CorreoYaRegistrado()
        cuenta = CuentaProfesor.crear(email=email, nombre=nombre, password_hash=self._hasheador.hashear(password))
        cuenta = self._repositorio.guardar(cuenta)
        return self._servicio_token.generar_profesor(cuenta.id)


class IniciarSesionProfesor:
    def __init__(
        self,
        repositorio: RepositorioCuentasProfesor,
        hasheador: HasheadorPassword,
        servicio_token: ServicioTokenProfesor,
    ):
        self._repositorio = repositorio
        self._hasheador = hasheador
        self._servicio_token = servicio_token

    def ejecutar(self, email: str, password: str) -> str:
        cuenta = self._repositorio.buscar_por_email(email.strip().lower())
        if not cuenta or not self._hasheador.verificar(password, cuenta.password_hash):
            raise CredencialesProfesorInvalidas()
        # Login funciona igual con la cuenta "pendiente" — así el profesor puede ver el
        # aviso de "tu cuenta está en revisión" en vez de quedar bloqueado sin explicación.
        # Los endpoints que sí requieren aprobación se protegen aparte (ver
        # get_profesor_aprobado_actual en core/deps.py).
        return self._servicio_token.generar_profesor(cuenta.id)
