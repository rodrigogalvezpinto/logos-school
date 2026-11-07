from sqlmodel import SQLModel, Session, create_engine

from app.core.config import settings

connect_args = {"options": "-c timezone=utc"} if "postgres" in settings.database_url else {}
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


def crear_tablas() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
