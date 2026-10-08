"""Importar os models aqui faz o SQLAlchemy conhecer todas as tabelas."""
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario

__all__ = ["Usuario", "Tarefa"]