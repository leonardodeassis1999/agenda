"""Formatos de entrada e saída das tarefas."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Prioridade = Literal["baixa", "media", "alta"]
Status = Literal["pendente", "em_andamento", "concluida"]


class TarefaCreate(BaseModel):
    # extra="forbid": campos desconhecidos (ex.: status) dão erro 422.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    titulo: str = Field(min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=2000)
    categoria: str | None = Field(default=None, max_length=50)
    prioridade: Prioridade = "media"
    data_prevista: date
    tempo_estimado_min: int = Field(gt=0, le=1440)


class TarefaUpdate(BaseModel):
    """Todos os campos são opcionais: só muda o que for enviado."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    descricao: str | None = Field(default=None, max_length=2000)
    categoria: str | None = Field(default=None, max_length=50)
    prioridade: Prioridade | None = None
    data_prevista: date | None = None
    tempo_estimado_min: int | None = Field(default=None, gt=0, le=1440)

    @model_validator(mode="after")
    def obrigatorios_nao_podem_ser_nulos(self):
        for campo in ("titulo", "prioridade", "data_prevista", "tempo_estimado_min"):
            if campo in self.model_fields_set and getattr(self, campo) is None:
                raise ValueError(f"{campo} não pode ser nulo.")
        return self


class TarefaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str | None
    categoria: str | None
    prioridade: str
    data_prevista: date
    tempo_estimado_min: int
    status: str
    iniciada_em: datetime | None
    concluida_em: datetime | None
    criado_em: datetime
    atrasada: bool