from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.main import app

client = TestClient(app)


def test_health():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["status"] == "ok"
    assert dados["app"] == "Meu Dia"


def test_health_database_conectado():
    """Usa o MySQL real: precisa do .env preenchido e do MySQL rodando."""
    resposta = client.get("/health/database")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["status"] == "ok"
    assert dados["database"] == "agenda"
    assert dados["connection"] == "ok"


def test_health_database_falha_sem_expor_senha(monkeypatch):
    """Simula o banco fora do ar e confere que nada sensível aparece."""

    class EngineQuebrada:
        def connect(self):
            raise SQLAlchemyError("falha simulada")

    monkeypatch.setattr("app.routes.health.engine", EngineQuebrada())

    resposta = client.get("/health/database")

    assert resposta.status_code == 503
    dados = resposta.json()
    assert dados["status"] == "error"
    assert dados["connection"] == "failed"
    if settings.db_password:
        assert settings.db_password not in resposta.text