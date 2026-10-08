from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_pagina_inicial_e_arquivos_estaticos():
    assert "Meu Dia" in client.get("/").text
    assert client.get("/js/api.js").status_code == 200
    assert client.get("/css/estilo.css").status_code == 200


def test_api_continua_acima_do_frontend():
    assert client.get("/health").json()["status"] == "ok"


def test_tela_de_perfil_existe():
    assert "Perfil" in client.get("/perfil.html").text
    assert client.get("/js/perfil.js").status_code == 200
    assert client.get("/js/menu.js").status_code == 200


def test_telas_de_tarefas_existem():
    for pagina in ("tarefa.html", "tarefas.html", "meu-dia.html"):
        assert client.get("/" + pagina).status_code == 200
    for script in ("comum.js", "tarefa.js", "tarefas.js", "meu-dia.js"):
        assert client.get("/js/" + script).status_code == 200