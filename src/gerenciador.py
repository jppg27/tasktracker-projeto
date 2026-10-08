"""
gerenciador.py - Regras de negócio do TaskTracker.

A classe GerenciadorTarefas é responsável por cadastrar, listar, concluir
e remover tarefas, além de gerar o resumo de progresso. As tarefas ficam
gravadas em data/tarefas.json, já que a Fase 1 não prevê banco de dados.
"""

import json
from datetime import date
from pathlib import Path

from models import STATUS_CONCLUIDA, Tarefa
from utils import (
    ORDEM_PRIORIDADE,
    converter_data,
    normalizar_prioridade,
    validar_data_limite,
    validar_titulo,
)

# Caminho padrão: <raiz do projeto>/data/tarefas.json
CAMINHO_PADRAO = Path(__file__).resolve().parent.parent / "data" / "tarefas.json"


class TarefaNaoEncontradaError(LookupError):
    """Erro lançado quando o ID informado não existe na lista de pendentes."""


class GerenciadorTarefas:
    """Gerencia a lista de tarefas pendentes e o histórico de concluídas."""

    def __init__(self, caminho_arquivo=CAMINHO_PADRAO):
        self.caminho_arquivo = Path(caminho_arquivo)
        self.pendentes = []
        self.concluidas = []
        self.proximo_id = 1
        self.aviso_carregamento = ""
        self.carregar()

    # ------------------------------------------------------------------
    # Persistência em arquivo JSON
    # ------------------------------------------------------------------
    def carregar(self):
        """Lê as tarefas gravadas em disco (se o arquivo existir)."""
        if not self.caminho_arquivo.exists():
            return
        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.pendentes = [Tarefa.from_dict(t) for t in dados.get("pendentes", [])]
            self.concluidas = [Tarefa.from_dict(t) for t in dados.get("concluidas", [])]
            maior_id = max((t.id for t in self.pendentes + self.concluidas), default=0)
            self.proximo_id = max(int(dados.get("proximo_id", 1)), maior_id + 1)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            self.pendentes, self.concluidas, self.proximo_id = [], [], 1
            self.aviso_carregamento = (
                f"Não foi possível ler '{self.caminho_arquivo.name}'. "
                "O TaskTracker foi iniciado com uma lista vazia."
            )

    def salvar(self):
        """Grava as tarefas pendentes e concluídas em disco."""
        self.caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        dados = {
            "proximo_id": self.proximo_id,
            "pendentes": [t.to_dict() for t in self.pendentes],
            "concluidas": [t.to_dict() for t in self.concluidas],
        }
        with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    # ------------------------------------------------------------------
    # Cadastro
    # ------------------------------------------------------------------
    def cadastrar(self, titulo, descricao, prioridade, data_limite, hoje=None):
        """Cadastra uma nova tarefa com status "Pendente".

        Aplica novamente as regras de validação para garantir a integridade
        dos dados e lança ValueError caso algum campo seja inválido.
        """
        if not validar_titulo(titulo):
            raise ValueError("O título da tarefa é obrigatório.")

        prioridade_padronizada = normalizar_prioridade(prioridade)
        if prioridade_padronizada is None:
            raise ValueError("Prioridade inválida. Use Alta, Média ou Baixa.")

        data_valida, mensagem = validar_data_limite(data_limite, hoje)
        if not data_valida:
            raise ValueError(mensagem)

        tarefa = Tarefa(
            id=self.proximo_id,  # Regra 4: ID único e sequencial
            titulo=titulo.strip(),
            descricao=(descricao or "").strip(),
            prioridade=prioridade_padronizada,
            data_limite=data_limite.strip(),
        )
        self.pendentes.append(tarefa)
        self.proximo_id += 1
        self.salvar()
        return tarefa

    # ------------------------------------------------------------------
    # Consulta
    # ------------------------------------------------------------------
    def listar_pendentes(self):
        """Retorna as pendentes ordenadas por prioridade e data limite."""
        return sorted(
            self.pendentes,
            key=lambda t: (
                ORDEM_PRIORIDADE.get(t.prioridade, len(ORDEM_PRIORIDADE)),
                converter_data(t.data_limite) or date.max,
                t.id,
            ),
        )

    def listar_concluidas(self):
        """Retorna o histórico de tarefas concluídas (ordem de conclusão)."""
        return list(self.concluidas)

    def buscar_pendente(self, id_tarefa):
        """Retorna a tarefa pendente com o ID informado ou None."""
        for tarefa in self.pendentes:
            if tarefa.id == id_tarefa:
                return tarefa
        return None

    # ------------------------------------------------------------------
    # Conclusão e remoção
    # ------------------------------------------------------------------
    def concluir(self, id_tarefa):
        """Move a tarefa da lista de pendentes para o histórico de concluídas."""
        tarefa = self.buscar_pendente(id_tarefa)
        if tarefa is None:  # Regra 5
            raise TarefaNaoEncontradaError(
                f"Não existe tarefa pendente com o ID {id_tarefa}."
            )
        self.pendentes.remove(tarefa)
        tarefa.status = STATUS_CONCLUIDA
        self.concluidas.append(tarefa)  # Regra 6: histórico separado
        self.salvar()
        return tarefa

    def remover(self, id_tarefa):
        """Exclui definitivamente uma tarefa da lista de pendentes."""
        tarefa = self.buscar_pendente(id_tarefa)
        if tarefa is None:  # Regra 5
            raise TarefaNaoEncontradaError(
                f"Não existe tarefa pendente com o ID {id_tarefa}."
            )
        self.pendentes.remove(tarefa)
        self.salvar()
        return tarefa

    # ------------------------------------------------------------------
    # Resumo
    # ------------------------------------------------------------------
    def resumo(self):
        """Retorna o total de tarefas pendentes, concluídas e geral."""
        total_pendentes = len(self.pendentes)
        total_concluidas = len(self.concluidas)
        return {
            "pendentes": total_pendentes,
            "concluidas": total_concluidas,
            "total": total_pendentes + total_concluidas,
        }
