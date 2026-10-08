from fastapi import FastAPI

from app.routes import auth, health, tarefas, usuarios

app = FastAPI(title="Meu Dia")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tarefas.router)