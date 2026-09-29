from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.database.connection import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
def health():
    """Verifica apenas se a aplicação está no ar (não usa o banco)."""
    return {"status": "ok", "app": settings.app_name}


@router.get("/database")
def health_database():
    """Verifica se a aplicação consegue conectar no database agenda."""
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
    except SQLAlchemyError:
        # Não devolvemos detalhes do erro para não expor credenciais.
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "database": settings.db_name,
                "connection": "failed",
            },
        )

    return {"status": "ok", "database": settings.db_name, "connection": "ok"}
