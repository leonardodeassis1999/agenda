"""Testes de tarefas (usam o MySQL real)."""
from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.tempo import hoje
from app.database.connection import SessionLocal
from app.main import app
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario

client = TestClient(app)
PADRAO_EMAIL = "teste\\_%@teste.local"


@pytest.fixture(autouse=True)
def limpar_dados_de_teste():
    yield
    with SessionLocal() as db:
        ids = select(Usuario.id).where(Usuario.email.like(PADRAO_EMAIL))
        db.execute(delete(Tarefa).where(Tarefa.usuario_id.in_(ids)))
        db.execute(delete(Usuario).where(Usuario.email.like(PADRAO_EMAIL)))
        db.commit()


def logar() -> dict:
    email = f"teste_{uuid4().hex[:10]}@teste.local"
    client.post(
        "/auth/cadastro",
        json={"nome": "Aluno Teste", "email": email, "senha": "senha12345"},
    )
    resposta = client.post("/auth/login", json={"email": email, "senha": "senha12345"})
    return {"Authorization": f"Bearer {resposta.json()['access_token']}"}


def dados(**extra) -> dict:
    base = {
        "titulo": "Estudar Python",
        "prioridade": "alta",
        "data_prevista": hoje().isoformat(),
        "tempo_estimado_min": 30,
    }
    base.update(extra)
    return base


def criar(cabecalho: dict, **extra) -> dict:
    resposta = client.post("/tarefas", json=dados(**extra), headers=cabecalho)
    assert resposta.status_code == 201
    return resposta.json()


def test_exige_login():
    assert client.get("/tarefas").status_code == 401
    assert client.post("/tarefas", json=dados()).status_code == 401


def test_criar_e_ver():
    cab = logar()
    tarefa = criar(cab)
    assert tarefa["status"] == "pendente"
    assert tarefa["atrasada"] is False
    assert tarefa["iniciada_em"] is None

    ver = client.get(f"/tarefas/{tarefa['id']}", headers=cab)
    assert ver.status_code == 200
    assert ver.json()["titulo"] == "Estudar Python"


def test_validacoes():
    cab = logar()

    def post(**extra):
        return client.post("/tarefas", json=dados(**extra), headers=cab).status_code

    assert post(tempo_estimado_min=0) == 422
    assert post(prioridade="urgente") == 422
    assert post(titulo="   ") == 422
    assert post(status="concluida") == 422  # status não pode ser enviado
    sem_data = dados()
    del sem_data["data_prevista"]
    assert client.post("/tarefas", json=sem_data, headers=cab).status_code == 422


def test_listar_com_filtros():
    cab = logar()
    ontem = (hoje() - timedelta(days=1)).isoformat()
    amanha = (hoje() + timedelta(days=1)).isoformat()
    criar(cab, titulo="Hoje")
    atrasada = criar(cab, titulo="Ontem", data_prevista=ontem)
    criar(cab, titulo="Amanhã", data_prevista=amanha)

    assert atrasada["atrasada"] is True
    assert len(client.get("/tarefas", headers=cab).json()) == 3

    do_dia = client.get("/tarefas", params={"data": hoje().isoformat()}, headers=cab)
    assert [t["titulo"] for t in do_dia.json()] == ["Hoje"]

    lista = client.get("/tarefas", params={"atrasadas": "true"}, headers=cab).json()
    assert [t["titulo"] for t in lista] == ["Ontem"]

    assert client.get("/tarefas", params={"status": "concluida"}, headers=cab).json() == []
    assert client.get("/tarefas", params={"status": "xyz"}, headers=cab).status_code == 422

    # Concluída deixa de ser atrasada.
    client.post(f"/tarefas/{atrasada['id']}/concluir", headers=cab)
    assert client.get("/tarefas", params={"atrasadas": "true"}, headers=cab).json() == []


def test_usuario_nao_ve_tarefa_de_outro():
    dono, intruso = logar(), logar()
    tarefa = criar(dono)
    url = f"/tarefas/{tarefa['id']}"

    assert client.get(url, headers=intruso).status_code == 404
    assert client.put(url, json={"titulo": "Invadido"}, headers=intruso).status_code == 404
    assert client.delete(url, headers=intruso).status_code == 404
    assert client.post(f"{url}/concluir", headers=intruso).status_code == 404
    assert client.get("/tarefas", headers=intruso).json() == []
    assert client.get(url, headers=dono).json()["titulo"] == "Estudar Python"


def test_editar():
    cab = logar()
    tarefa = criar(cab, descricao="texto")
    url = f"/tarefas/{tarefa['id']}"

    alterada = client.put(url, json={"titulo": "Novo título"}, headers=cab)
    assert alterada.status_code == 200
    assert alterada.json()["titulo"] == "Novo título"
    assert alterada.json()["descricao"] == "texto"  # não enviado, não muda

    limpa = client.put(url, json={"descricao": None}, headers=cab)
    assert limpa.json()["descricao"] is None

    assert client.put(url, json={"titulo": None}, headers=cab).status_code == 422
    assert client.put(url, json={"status": "concluida"}, headers=cab).status_code == 422


def test_iniciar_e_concluir():
    cab = logar()
    url = f"/tarefas/{criar(cab)['id']}"

    iniciada = client.post(f"{url}/iniciar", headers=cab)
    assert iniciada.status_code == 200
    assert iniciada.json()["status"] == "em_andamento"
    assert iniciada.json()["iniciada_em"] is not None
    assert client.post(f"{url}/iniciar", headers=cab).status_code == 409

    concluida = client.post(f"{url}/concluir", headers=cab)
    assert concluida.status_code == 200
    assert concluida.json()["status"] == "concluida"
    assert concluida.json()["concluida_em"] is not None
    assert client.post(f"{url}/concluir", headers=cab).status_code == 409
    assert client.post(f"{url}/iniciar", headers=cab).status_code == 409


def test_excluir():
    cab = logar()
    url = f"/tarefas/{criar(cab)['id']}"

    assert client.delete(url, headers=cab).status_code == 204
    assert client.get(url, headers=cab).status_code == 404
    assert client.delete(url, headers=cab).status_code == 404