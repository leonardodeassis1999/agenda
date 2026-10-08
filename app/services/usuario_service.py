"""Regras de usuário: cadastro, login e atualização."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import CadastroIn, UsuarioUpdate
from app.services.seguranca import gerar_hash_senha, verificar_senha


class EmailJaCadastrado(Exception):
    pass


def buscar_por_email(db: Session, email: str) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email))


def criar_usuario(db: Session, dados: CadastroIn) -> Usuario:
    if buscar_por_email(db, dados.email):
        raise EmailJaCadastrado()
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
    )
    db.add(usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailJaCadastrado()
    db.refresh(usuario)
    return usuario


def autenticar(db: Session, email: str, senha: str) -> Usuario | None:
    usuario = buscar_por_email(db, email)
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


def atualizar_usuario(db: Session, usuario: Usuario, dados: UsuarioUpdate) -> Usuario:
    if dados.nome is not None:
        usuario.nome = dados.nome
    if dados.email is not None and dados.email != usuario.email:
        if buscar_por_email(db, dados.email):
            raise EmailJaCadastrado()
        usuario.email = dados.email
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailJaCadastrado()
    db.refresh(usuario)
    return usuario