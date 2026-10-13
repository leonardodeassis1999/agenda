# Meu Dia

Sistema web responsivo para gerenciamento de rotinas diárias. Nasceu de um problema real: ajudar pessoas a organizar o dia, definir prioridades e cumprir suas tarefas.

## Funcionalidades

- Cadastro e login de usuários com autenticação JWT
- Perfil do usuário
- CRUD de tarefas com título, descrição, categoria, prioridade, data prevista e tempo estimado
- Controle do andamento: iniciar e concluir tarefas, com registro dos horários
- Identificação de tarefas atrasadas
- Filtros de tarefas
- Telas de "Minhas tarefas" e "Meu dia"
- Testes automatizados

## Tecnologias

- **Backend:** Python, FastAPI
- **Banco de dados:** MySQL (SQLAlchemy 2.x + PyMySQL)
- **Autenticação:** JWT
- **Configuração:** pydantic-settings (variáveis em `.env`)
- **Frontend:** HTML, CSS e JavaScript puro
- **Testes:** pytest + httpx

## Estrutura

```
agenda
├── app
│   ├── main.py                 # aplicação FastAPI
│   ├── core/config.py          # configurações (.env)
│   ├── database/connection.py  # engine e sessão do MySQL
│   ├── models/                 # modelos do banco
│   ├── schemas/                # validação de dados
│   ├── routes/                 # rotas da API
│   └── services/               # regras de negócio
├── frontend/                   # telas do sistema
├── tests/                      # testes automatizados
├── .env.example                # modelo do .env
├── requirements.txt
└── README.md
```

## Como rodar

### 1. Clone o repositório

```
git clone https://github.com/leonardodeassis1999/agenda.git
cd agenda
```

### 2. Banco de dados

É necessário ter o MySQL instalado. No MySQL Workbench:

1. Abra **File → Open SQL Script** e escolha o arquivo `banco.sql` deste repositório.
2. Clique no raio ⚡ para executar. Ele cria o banco `agenda` e as tabelas `usuarios` e `tarefas`.

```sql
CREATE DATABASE agenda;
```

### 3. Configure o .env

1. Copie o modelo: `copy .env.example .env`
2. Abra o `.env` e preencha `DB_USER` e `DB_PASSWORD` com os dados do MySQL do seu computador.
3. Mantenha `DB_NAME=agenda`.

O `.env` nunca deve ser enviado ao GitHub.

### 4. Instale as dependências

```
pip install -r requirements.txt
```

### 5. Execute a aplicação

```
uvicorn app.main:app --reload
```

## Testes

```
pytest
```

## URLs locais

- Aplicação: http://127.0.0.1:8000
- Documentação da API (Swagger): http://127.0.0.1:8000/docs

## Autor

Leonardo de Assis, estudante de Desenvolvimento Web, Fraiburgo (SC).

[LinkedIn](https://www.linkedin.com/in/leonardo-assis-3b7729443/) | [GitHub](https://github.com/leonardodeassis1999)
