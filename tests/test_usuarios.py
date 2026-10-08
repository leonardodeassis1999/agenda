"""Testes de cadastro, login e perfil (usam o MySQL real)."""
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.database.connection import SessionLocal
from app.main import app
from app.models.usuario import Usuario

client = TestClient(app)


def novo_email() -> str:
    return f"teste_{uuid4().hex[:10]}@teste.local"


@pytest.fixture(autouse=True)
def limpar_usuarios_de_teste():
    yield
    with SessionLocal() as db:
        db.execute(delete(Usuario).where(Usuario.email.like("teste\\_%@teste.local")))
        db.commit()


def cadastrar(email: str, senha: str = "senha12345"):
    return client.post(
        "/auth/cadastro", json={"nome": "Aluno Teste", "email": email, "senha": senha}
    )


def token_de(email: str, senha: str = "senha12345") -> dict:
    resposta = client.post("/auth/login", json={"email": email, "senha": senha})
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


def test_cadastro_nao_devolve_senha():
    resposta = cadastrar(novo_email())
    assert resposta.status_code == 201
    assert "senha" not in resposta.text
    assert "hash" not in resposta.text


def test_email_duplicado():
    email = novo_email()
    cadastrar(email)
    assert cadastrar(email).status_code == 409


def test_senha_curta_e_email_invalido():
    assert cadastrar(novo_email(), senha="123").status_code == 422
    assert cadastrar("nao-e-email").status_code == 422


def test_login_ok_e_senha_errada():
    email = novo_email()
    cadastrar(email)
    ok = client.post("/auth/login", json={"email": email, "senha": "senha12345"})
    assert ok.status_code == 200
    assert ok.json()["token_type"] == "bearer"
    errada = client.post("/auth/login", json={"email": email, "senha": "errada999"})
    assert errada.status_code == 401


def test_perfil_exige_token():
    assert client.get("/usuarios/me").status_code == 401
    cabecalho = {"Authorization": "Bearer token-falso"}
    assert client.get("/usuarios/me", headers=cabecalho).status_code == 401


def test_ver_perfil():
    email = novo_email()
    cadastrar(email)
    resposta = client.get("/usuarios/me", headers=token_de(email))
    assert resposta.status_code == 200
    assert resposta.json()["email"] == email
    assert "senha" not in resposta.text


def test_atualizar_perfil_e_conflito_de_email():
    email_a, email_b = novo_email(), novo_email()
    cadastrar(email_a)
    cadastrar(email_b)
    cabecalho = token_de(email_a)

    novo_nome = client.put("/usuarios/me", json={"nome": "Nome Novo"}, headers=cabecalho)
    assert novo_nome.status_code == 200
    assert novo_nome.json()["nome"] == "Nome Novo"

    conflito = client.put("/usuarios/me", json={"email": email_b}, headers=cabecalho)
    assert conflito.status_code == 409