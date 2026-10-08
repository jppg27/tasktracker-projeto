"""
utils.py - Funções utilitárias de validação do TaskTracker.

Concentra as regras de validação definidas no Planejamento Lógico (Fase 1):
    - Regra 1: o título é obrigatório (não pode ser vazio nem só espaços);
    - Regra 2: a prioridade deve ser apenas Alta, Média (ou Media) ou Baixa;
    - Regra 3: a data limite deve ser válida (DD/MM/AAAA) e não pode ser
      anterior à data atual no momento do cadastro.
"""

import re
from datetime import date, datetime

FORMATO_DATA = "%d/%m/%Y"
_PADRAO_DATA = re.compile(r"\d{2}/\d{2}/\d{4}")

# Entradas aceitas (comparadas sem diferenciar maiúsculas/minúsculas)
# e o valor padronizado que será gravado na tarefa.
PRIORIDADES_VALIDAS = {
    "alta": "Alta",
    "média": "Média",
    "media": "Média",
    "baixa": "Baixa",
}

# Ordem usada na listagem: Alta > Média > Baixa.
ORDEM_PRIORIDADE = {"Alta": 0, "Média": 1, "Baixa": 2}


def validar_titulo(titulo: str) -> bool:
    """Retorna True se o título não estiver vazio nem for composto só de espaços."""
    return titulo is not None and titulo.strip() != ""


def normalizar_prioridade(prioridade: str):
    """Retorna a prioridade padronizada ("Alta", "Média" ou "Baixa").

    Retorna None quando o valor informado não for uma prioridade válida.
    """
    if prioridade is None:
        return None
    return PRIORIDADES_VALIDAS.get(prioridade.strip().lower())


def validar_prioridade(prioridade: str) -> bool:
    """Retorna True se a prioridade for Alta, Média/Media ou Baixa."""
    return normalizar_prioridade(prioridade) is not None


def converter_data(texto: str):
    """Converte um texto no formato DD/MM/AAAA em objeto date.

    Retorna None se o texto não seguir o formato ou se a data não existir
    (ex.: 31/02/2026).
    """
    if texto is None:
        return None
    texto = texto.strip()
    if not _PADRAO_DATA.fullmatch(texto):
        return None
    try:
        return datetime.strptime(texto, FORMATO_DATA).date()
    except ValueError:
        return None


def validar_data_limite(texto: str, hoje: date = None):
    """Valida a data limite de uma tarefa.

    Retorna uma tupla (valida, mensagem). Quando a data é válida, a
    mensagem é uma string vazia; caso contrário, explica o erro.
    """
    hoje = hoje or date.today()
    data = converter_data(texto)
    if data is None:
        return False, "Data inválida. Use o formato DD/MM/AAAA (ex.: 25/12/2026)."
    if data < hoje:
        return False, (
            "A data limite não pode ser anterior à data atual "
            f"({hoje.strftime(FORMATO_DATA)})."
        )
    return True, ""
