from fastapi import FastAPI

from app.routes import health

app = FastAPI(title="Meu Dia")

app.include_router(health.router)
