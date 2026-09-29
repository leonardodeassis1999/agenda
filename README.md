# Meu Dia

Sistema web responsivo para gerenciamento de rotinas diárias.
Esta é a **Etapa 01 — Fundação técnica**: só a base do projeto, sem telas nem regras de negócio.

## Objetivo

Ajudar o usuário a organizar o dia, definir prioridades e saber se as atividades cabem no tempo disponível (funcionalidades das próximas etapas).

## Tecnologias

- Python + FastAPI
- MySQL (SQLAlchemy 2.x + PyMySQL)
- pydantic-settings (configuração via `.env`)
- pytest + httpx (testes)
- Frontend futuro: HTML, CSS e JavaScript puro

## Estrutura inicial

```
C:\agenda
├── app
│   ├── main.py            # aplicação FastAPI
│   ├── core/config.py     # configurações (.env)
│   ├── database/connection.py  # engine e sessão do MySQL
│   ├── models/
│   ├── schemas/
│   ├── routes/health.py   # rotas /health e /health/database
│   └── services/
├── tests/test_health.py
├── .env            # NÃO vai para o Git
├── .env.example    # modelo do .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Banco de dados

Database obrigatório: **agenda** (já existente no MySQL local).
Nesta etapa nenhuma tabela é criada ou alterada.

## Configurando o .env

1. Copie o modelo: `copy .env.example .env`
2. Abra o `.env` e preencha `DB_USER` e `DB_PASSWORD` com os dados do MySQL do seu computador.
3. Mantenha `DB_NAME=agenda`.

O `.env` nunca deve ser enviado ao GitHub.

## Instalando as dependências

```
pip install -r requirements.txt
```

## Executando a aplicação

```
uvicorn app.main:app --reload
```

## Executando os testes

```
pytest
```

## URLs locais

- Aplicação: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health
- Health do banco: http://127.0.0.1:8000/health/database
