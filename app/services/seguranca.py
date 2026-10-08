"""Senha (bcrypt) e token (JWT)."""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings

ALGORITMO = "HS256"


def gerar_hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))
    except ValueError:
        return False


def criar_token(usuario_id: int) -> str:
    agora = datetime.now(timezone.utc)
    dados = {
        "sub": str(usuario_id),
        "iat": agora,
        "exp": agora + timedelta(minutes=settings.jwt_expira_minutos),
    }
    return jwt.encode(dados, settings.jwt_secret, algorithm=ALGORITMO)


def ler_token(token: str) -> int | None:
    """Devolve o id do usuário, ou None se o token for inválido ou expirado."""
    try:
        dados = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITMO])
        return int(dados["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        return None