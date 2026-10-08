"""Formatos de entrada e saída. A senha e o hash nunca saem na resposta."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class _Base(BaseModel):
    @field_validator("nome", "email", mode="before", check_fields=False)
    @classmethod
    def limpar_texto(cls, valor, info):
        if not isinstance(valor, str):
            return valor
        valor = valor.strip()
        return valor.lower() if info.field_name == "email" else valor


class CadastroIn(_Base):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=150, pattern=EMAIL_REGEX)
    senha: str = Field(min_length=8, max_length=72)

    @field_validator("senha")
    @classmethod
    def limite_do_bcrypt(cls, valor: str) -> str:
        if len(valor.encode("utf-8")) > 72:
            raise ValueError("Senha muito longa.")
        return valor


class LoginIn(_Base):
    email: str = Field(max_length=150)
    senha: str = Field(min_length=1, max_length=200)


class UsuarioUpdate(_Base):
    nome: str | None = Field(default=None, min_length=2, max_length=100)
    email: str | None = Field(default=None, max_length=150, pattern=EMAIL_REGEX)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    criado_em: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"