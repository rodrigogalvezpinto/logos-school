from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la app, leída de variables de entorno.

    Nunca se hardcodean secretos aquí — ver planificacion/17-infraestructura-y-entornos.md
    (regla de ambientes Desarrollo/Producción separados, cada uno con su propio .env).
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    entorno: str = "desarrollo"
    database_url: str = "postgresql://logos_dev:logos_dev_local@localhost:5432/logos_dev"
    jwt_secret: str = "cambiar-en-produccion-nunca-usar-este-valor"
    jwt_algoritmo: str = "HS256"
    jwt_expiracion_minutos: int = 60 * 12  # 12 horas (una evaluación larga no debe expulsar al alumno)

    google_client_id: str = ""
    resend_api_key: str = ""
    resend_remitente: str = "Logos <no-responder@logos.cl>"


settings = Settings()
