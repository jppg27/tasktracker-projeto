"""Testes automatizados das funções de validação (src/utils.py)."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from utils import (  # noqa: E402
    converter_data,
    normalizar_prioridade,
    validar_data_limite,
    validar_prioridade,
    validar_titulo,
)

HOJE = date(2026, 10, 8)


# ---------------------------- Título ----------------------------------
def test_titulo_valido():
    assert validar_titulo("Estudar lógica de programação")


def test_titulo_vazio_e_rejeitado():
    assert not validar_titulo("")


def test_titulo_somente_espacos_e_rejeitado():
    assert not validar_titulo("     ")
    assert not validar_titulo("\t  \n")


# --------------------------- Prioridade --------------------------------
def test_prioridades_validas_sao_padronizadas():
    assert normalizar_prioridade("Alta") == "Alta"
    assert normalizar_prioridade("Média") == "Média"
    assert normalizar_prioridade("Media") == "Média"
    assert normalizar_prioridade("Baixa") == "Baixa"


def test_prioridade_ignora_maiusculas_e_espacos():
    assert normalizar_prioridade("  ALTA ") == "Alta"
    assert normalizar_prioridade("média") == "Média"


def test_prioridades_invalidas_sao_rejeitadas():
    for valor in ["", "   ", "Urgente", "alta prioridade", "1", "Normal"]:
        assert not validar_prioridade(valor)
        assert normalizar_prioridade(valor) is None


# ------------------------------ Data -----------------------------------
def test_converter_data_valida():
    assert converter_data("25/12/2026") == date(2026, 12, 25)


def test_converter_data_formato_errado():
    assert converter_data("2026-12-25") is None
    assert converter_data("1/1/2026") is None
    assert converter_data("amanhã") is None


def test_converter_data_inexistente():
    assert converter_data("31/02/2026") is None


def test_data_de_hoje_e_aceita():
    valida, _ = validar_data_limite("08/10/2026", hoje=HOJE)
    assert valida


def test_data_futura_e_aceita():
    valida, mensagem = validar_data_limite("15/11/2026", hoje=HOJE)
    assert valida
    assert mensagem == ""


def test_data_passada_e_rejeitada():
    valida, mensagem = validar_data_limite("07/10/2026", hoje=HOJE)
    assert not valida
    assert "anterior" in mensagem


def test_data_em_formato_invalido_e_rejeitada():
    valida, mensagem = validar_data_limite("32/13/2026", hoje=HOJE)
    assert not valida
    assert "DD/MM/AAAA" in mensagem
