from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.dependencias import get_db, get_usuario_atual
from app.models.tarefa import Tarefa
from app.models.usuario import Usuario
from app.schemas.tarefa import Status, TarefaCreate, TarefaOut, TarefaUpdate
from app.services import tarefa_service

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


def obter_ou_404(db: Session, usuario: Usuario, tarefa_id: int) -> Tarefa:
    tarefa = tarefa_service.buscar_tarefa(db, usuario, tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return tarefa


@router.post("", response_model=TarefaOut, status_code=201)
def criar(
    dados: TarefaCreate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    return tarefa_service.criar_tarefa(db, usuario, dados)


@router.get("", response_model=list[TarefaOut])
def listar(
    status: Status | None = None,
    data: date | None = None,
    atrasadas: bool | None = None,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    return tarefa_service.listar_tarefas(db, usuario, status, data, atrasadas)


@router.get("/{tarefa_id}", response_model=TarefaOut)
def ver(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    return obter_ou_404(db, usuario, tarefa_id)


@router.put("/{tarefa_id}", response_model=TarefaOut)
def editar(
    tarefa_id: int,
    dados: TarefaUpdate,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    tarefa = obter_ou_404(db, usuario, tarefa_id)
    return tarefa_service.atualizar_tarefa(db, tarefa, dados)


@router.delete("/{tarefa_id}", status_code=204)
def excluir(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    tarefa = obter_ou_404(db, usuario, tarefa_id)
    tarefa_service.excluir_tarefa(db, tarefa)
    return Response(status_code=204)


@router.post("/{tarefa_id}/iniciar", response_model=TarefaOut)
def iniciar(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    tarefa = obter_ou_404(db, usuario, tarefa_id)
    try:
        return tarefa_service.iniciar_tarefa(db, tarefa)
    except tarefa_service.TransicaoInvalida as erro:
        raise HTTPException(status_code=409, detail=erro.mensagem)


@router.post("/{tarefa_id}/concluir", response_model=TarefaOut)
def concluir(
    tarefa_id: int,
    usuario: Usuario = Depends(get_usuario_atual),
    db: Session = Depends(get_db),
):
    tarefa = obter_ou_404(db, usuario, tarefa_id)
    try:
        return tarefa_service.concluir_tarefa(db, tarefa)
    except tarefa_service.TransicaoInvalida as erro:
        raise HTTPException(status_code=409, detail=erro.mensagem)