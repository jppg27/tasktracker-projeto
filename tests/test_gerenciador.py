"""Testes automatizados das regras de negócio (src/gerenciador.py)."""

import json
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from gerenciador import GerenciadorTarefas, TarefaNaoEncontradaError  # noqa: E402
from models import STATUS_CONCLUIDA, STATUS_PENDENTE  # noqa: E402

HOJE = date(2026, 10, 8)


@pytest.fixture
def gerenciador(tmp_path):
    """Gerenciador que grava em um arquivo temporário (não altera data/)."""
    return GerenciadorTarefas(tmp_path / "tarefas.json")


def cadastrar(g, titulo="Tarefa", prioridade="Alta", data="20/10/2026", descricao=""):
    return g.cadastrar(titulo, descricao, prioridade, data, hoje=HOJE)


# ----------------------------- Cadastro --------------------------------
def test_cadastro_define_status_pendente_e_id_sequencial(gerenciador):
    t1 = cadastrar(gerenciador, "Primeira")
    t2 = cadastrar(gerenciador, "Segunda")
    assert (t1.id, t2.id) == (1, 2)
    assert t1.status == STATUS_PENDENTE
    assert len(gerenciador.pendentes) == 2


def test_cadastro_padroniza_campos(gerenciador):
    tarefa = cadastrar(gerenciador, "  Estudar Git  ", "media", descricao="  ler docs ")
    assert tarefa.titulo == "Estudar Git"
    assert tarefa.descricao == "ler docs"
    assert tarefa.prioridade == "Média"


@pytest.mark.parametrize("titulo", ["", "   "])
def test_cadastro_rejeita_titulo_vazio(gerenciador, titulo):
    with pytest.raises(ValueError):
        cadastrar(gerenciador, titulo)
    assert gerenciador.pendentes == []


def test_cadastro_rejeita_prioridade_invalida(gerenciador):
    with pytest.raises(ValueError):
        cadastrar(gerenciador, prioridade="Urgente")


def test_cadastro_rejeita_data_passada(gerenciador):
    with pytest.raises(ValueError):
        cadastrar(gerenciador, data="01/01/2026")


def test_ids_nao_sao_reutilizados_apos_remocao(gerenciador):
    t1 = cadastrar(gerenciador, "A")
    gerenciador.remover(t1.id)
    t2 = cadastrar(gerenciador, "B")
    assert t2.id == 2


# ---------------------------- Listagem ---------------------------------
def test_lista_vazia(gerenciador):
    assert gerenciador.listar_pendentes() == []


def test_listagem_ordena_por_prioridade_e_data(gerenciador):
    cadastrar(gerenciador, "Baixa", "Baixa", "10/10/2026")
    cadastrar(gerenciador, "Alta tarde", "Alta", "30/10/2026")
    cadastrar(gerenciador, "Media", "Média", "09/10/2026")
    cadastrar(gerenciador, "Alta cedo", "Alta", "15/10/2026")
    titulos = [t.titulo for t in gerenciador.listar_pendentes()]
    assert titulos == ["Alta cedo", "Alta tarde", "Media", "Baixa"]


# --------------------------- Conclusão ---------------------------------
def test_concluir_move_para_historico(gerenciador):
    tarefa = cadastrar(gerenciador)
    gerenciador.concluir(tarefa.id)
    assert gerenciador.pendentes == []
    assert gerenciador.concluidas[0].id == tarefa.id
    assert gerenciador.concluidas[0].status == STATUS_CONCLUIDA


def test_concluir_id_inexistente(gerenciador):
    cadastrar(gerenciador)
    with pytest.raises(TarefaNaoEncontradaError):
        gerenciador.concluir(99)


def test_nao_conclui_tarefa_ja_concluida(gerenciador):
    tarefa = cadastrar(gerenciador)
    gerenciador.concluir(tarefa.id)
    with pytest.raises(TarefaNaoEncontradaError):
        gerenciador.concluir(tarefa.id)


# ---------------------------- Remoção ----------------------------------
def test_remover_tarefa(gerenciador):
    tarefa = cadastrar(gerenciador)
    gerenciador.remover(tarefa.id)
    assert gerenciador.pendentes == []
    assert gerenciador.concluidas == []


def test_remover_id_inexistente(gerenciador):
    with pytest.raises(TarefaNaoEncontradaError):
        gerenciador.remover(1)


# ----------------------------- Resumo ----------------------------------
def test_resumo(gerenciador):
    t1 = cadastrar(gerenciador, "A")
    cadastrar(gerenciador, "B")
    gerenciador.concluir(t1.id)
    assert gerenciador.resumo() == {"pendentes": 1, "concluidas": 1, "total": 2}


# -------------------------- Persistência -------------------------------
def test_dados_sao_salvos_e_recarregados(tmp_path):
    caminho = tmp_path / "tarefas.json"
    g1 = GerenciadorTarefas(caminho)
    t1 = cadastrar(g1, "Persistir")
    cadastrar(g1, "Outra")
    g1.concluir(t1.id)

    g2 = GerenciadorTarefas(caminho)
    assert [t.titulo for t in g2.pendentes] == ["Outra"]
    assert [t.titulo for t in g2.concluidas] == ["Persistir"]
    assert g2.proximo_id == 3


def test_arquivo_salvo_em_utf8_legivel(tmp_path):
    caminho = tmp_path / "tarefas.json"
    g = GerenciadorTarefas(caminho)
    cadastrar(g, "Revisão", "Média")
    conteudo = caminho.read_text(encoding="utf-8")
    assert "Revisão" in conteudo and "Média" in conteudo
    assert json.loads(conteudo)["proximo_id"] == 2


def test_arquivo_corrompido_inicia_lista_vazia(tmp_path):
    caminho = tmp_path / "tarefas.json"
    caminho.write_text("{ isto não é json", encoding="utf-8")
    g = GerenciadorTarefas(caminho)
    assert g.pendentes == [] and g.concluidas == []
    assert g.aviso_carregamento
