from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_JWT_SECRET_INSEGURO = "cambiar-en-produccion-nunca-usar-este-valor"


class Settings(BaseSettings):
    """Configuración de la app, leída de variables de entorno.

    Nunca se hardcodean secretos aquí — ver planificacion/17-infraestructura-y-entornos.md
    (regla de ambientes Desarrollo/Producción separados, cada uno con su propio .env).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    entorno: str = "desarrollo"
    database_url: str = "postgresql://logos_dev:logos_dev_local@localhost:5432/logos_dev"

    # Rate limiting de /auth/registro y /auth/login (fuerza bruta / creación masiva de
    # cuentas) — valores de producción por defecto. En Desarrollo, la suite Playwright
    # completa registra decenas de cuentas de prueba en corridas rápidas y consecutivas
    # (workers=1, cada test toma ~1s), lo que puede superar el límite pensado para tráfico
    # real dentro de la misma ventana de un minuto — un `.env` local relajado (nunca el de
    # Producción, ver planificacion/17-infraestructura-y-entornos.md) evita ese choque sin
    # tocar la protección real. `tests/test_auth.py` verifica el mecanismo contra el valor
    # configurado, no un número fijo, así que sigue siendo una prueba real del rate limit
    # sea cual sea el valor activo.
    limite_registro_por_minuto: int = 5
    limite_login_por_minuto: int = 10

    # Auditoría de seguridad (2026-08-17): de más de 30 endpoints de escritura, solo estos 2
    # tenían protección de rate limit — el resto, incluido el login de Admin (la cuenta de
    # mayor privilegio de todo el sistema), no tenía ninguna. `limite_global_por_minuto` es
    # una red de seguridad por defecto para CUALQUIER endpoint (presente o futuro, ver
    # `SlowAPIMiddleware` en `main.py`); los siguientes son límites más estrictos para
    # endpoints puntuales de mayor riesgo (fuerza bruta o inundar la base de datos con
    # filas). Mismo criterio que arriba: valores de producción por defecto, `.env` de
    # Desarrollo los relaja para no chocar con la suite Playwright completa.
    limite_global_por_minuto: int = 300
    limite_admin_login_por_minuto: int = 5
    limite_registro_profesor_por_minuto: int = 5
    limite_login_profesor_por_minuto: int = 10
    limite_agregar_alumno_por_minuto: int = 10
    limite_sugerencia_por_minuto: int = 5
    limite_reportar_error_por_minuto: int = 10
    limite_comunicado_por_minuto: int = 10

    jwt_secret: str = _JWT_SECRET_INSEGURO
    jwt_algoritmo: str = "HS256"
    jwt_expiracion_minutos: int = 60 * 12  # 12 horas (una evaluación larga no debe expulsar al alumno)

    google_client_id: str = ""
    resend_api_key: str = ""
    resend_remitente: str = "Logos <no-responder@logos.cl>"

    @model_validator(mode="after")
    def _no_arrancar_produccion_con_jwt_secret_inseguro(self) -> "Settings":
        """Auditoría de seguridad (2026-08-17): el valor por defecto de `jwt_secret` está
        en el código fuente, público en el repo — si `ENTORNO=produccion` arranca sin un
        `JWT_SECRET` propio configurado en su `.env`, cualquiera que lea el repo podría
        forjar tokens válidos de cualquier cuenta. Mejor que la app no arranque en absoluto
        a que arranque insegura en silencio."""
        if self.entorno == "produccion" and self.jwt_secret == _JWT_SECRET_INSEGURO:
            raise ValueError(
                "JWT_SECRET no está configurado (sigue con el valor por defecto inseguro) "
                "y ENTORNO=produccion — configura un JWT_SECRET propio en el .env de "
                "Producción antes de arrancar."
            )
        return self


settings = Settings()
