"""Regras de tarefas. Toda consulta filtra pelo usuário logado."""
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.tempo import agora, hoje
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.schemas.tarefa import TarefaCreate, TarefaUpdate


class TransicaoInvalida(Exception):
    def __init__(self, mensagem: str):
        self.mensagem = mensagem


def criar_tarefa(db: Session, usuario: Usuario, dados: TarefaCreate) -> Tarefa:
    tarefa = Tarefa(usuario_id=usuario.id, **dados.model_dump())
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def listar_tarefas(
    db: Session,
    usuario: Usuario,
    status: str | None = None,
    data: date | None = None,
    atrasadas: bool | None = None,
) -> list[Tarefa]:
    consulta = select(Tarefa).where(Tarefa.usuario_id == usuario.id)
    if status is not None:
        consulta = consulta.where(Tarefa.status == status)
    if data is not None:
        consulta = consulta.where(Tarefa.data_prevista == data)
    if atrasadas:
        consulta = consulta.where(
            Tarefa.status != "concluida", Tarefa.data_prevista < hoje()
        )
    consulta = consulta.order_by(Tarefa.data_prevista, Tarefa.id)
    return list(db.scalars(consulta))


def buscar_tarefa(db: Session, usuario: Usuario, tarefa_id: int) -> Tarefa | None:
    """Só devolve a tarefa se ela for do usuário logado."""
    return db.scalar(
        select(Tarefa).where(Tarefa.id == tarefa_id, Tarefa.usuario_id == usuario.id)
    )


def atualizar_tarefa(db: Session, tarefa: Tarefa, dados: TarefaUpdate) -> Tarefa:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def excluir_tarefa(db: Session, tarefa: Tarefa) -> None:
    db.delete(tarefa)
    db.commit()


def iniciar_tarefa(db: Session, tarefa: Tarefa) -> Tarefa:
    if tarefa.status != "pendente":
        raise TransicaoInvalida("Só é possível iniciar uma tarefa pendente.")
    tarefa.status = "em_andamento"
    tarefa.iniciada_em = agora()
    db.commit()
    db.refresh(tarefa)
    return tarefa


def concluir_tarefa(db: Session, tarefa: Tarefa) -> Tarefa:
    if tarefa.status == "concluida":
        raise TransicaoInvalida("A tarefa já está concluída.")
    tarefa.status = "concluida"
    tarefa.concluida_em = agora()
    db.commit()
    db.refresh(tarefa)
    return tarefa