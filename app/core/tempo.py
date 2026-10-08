"""Data e hora no fuso de Brasília. 'Hoje' sempre vem daqui."""
from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("America/Sao_Paulo")


def agora() -> datetime:
    """Data e hora atuais de Brasília (sem fuso, como o MySQL guarda)."""
    return datetime.now(FUSO).replace(tzinfo=None)


def hoje() -> date:
    return datetime.now(FUSO).date()