from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencias import get_db
from app.schemas.usuario import CadastroIn, LoginIn, TokenOut, UsuarioOut
from app.services import usuario_service
from app.services.seguranca import criar_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/cadastro", response_model=UsuarioOut, status_code=201)
def cadastro(dados: CadastroIn, db: Session = Depends(get_db)):
    try:
        return usuario_service.criar_usuario(db, dados)
    except usuario_service.EmailJaCadastrado:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")


@router.post("/login", response_model=TokenOut)
def login(dados: LoginIn, db: Session = Depends(get_db)):
    usuario = usuario_service.autenticar(db, dados.email, dados.senha)
    if usuario is None:
        # Mesma mensagem para e-mail ou senha errados.
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    return TokenOut(access_token=criar_token(usuario.id))