"""Conexão com o MySQL (database: agenda).

Nesta etapa apenas PREPARAMOS a conexão.
Não criamos tabelas (nada de Base.metadata.create_all).
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# URL.create trata caracteres especiais da senha automaticamente.
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base para os models das próximas etapas."""
    pass
