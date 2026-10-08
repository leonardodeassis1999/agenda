from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencias import get_db, get_usuario_atual
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioOut, UsuarioUpdate
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/me", response_model=UsuarioOut)
def ver_perfil(usuario: Usuario = Depends(get_usuario_atual)):
    return usuario


@router.put("/me", response_model=UsuarioOut)
def atualizar_perfil(
    dados: UsuarioUpdate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    try:
        return usuario_service.atualizar_usuario(db, usuario, dados)
    except usuario_service.EmailJaCadastrado:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")