"""Tabela tarefas."""
from datetime import date, datetime

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    titulo: Mapped[str] = mapped_column(String(150))
    descricao: Mapped[str | None] = mapped_column(Text)
    categoria: Mapped[str | None] = mapped_column(String(50))
    prioridade: Mapped[str] = mapped_column(String(10), default="media")
    data_prevista: Mapped[date] = mapped_column(index=True)
    # Em minutos, para somar e comparar com o tempo disponível do dia.
    tempo_estimado_min: Mapped[int]
    status: Mapped[str] = mapped_column(String(20), default="pendente")
    iniciada_em: Mapped[datetime | None]
    concluida_em: Mapped[datetime | None]
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())