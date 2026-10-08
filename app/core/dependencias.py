"""Sessão do banco e usuário logado, reutilizados pelas rotas."""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.usuario import Usuario
from app.services.seguranca import ler_token

bearer = HTTPBearer(auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    erro = HTTPException(
        status_code=401,
        detail="Não autenticado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credenciais is None:
        raise erro
    usuario_id = ler_token(credenciais.credentials)
    if usuario_id is None:
        raise erro
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise erro
    return usuario