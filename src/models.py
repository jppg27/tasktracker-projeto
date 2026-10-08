"""
models.py - Estrutura de dados da tarefa do TaskTracker.

Define a classe Tarefa, que representa cada atividade cadastrada pelo
usuário, além das constantes de status utilizadas pelo sistema.
"""

from dataclasses import asdict, dataclass

STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"


@dataclass
class Tarefa:
    """Representa uma tarefa do TaskTracker.

    Campos:
        id: identificador único e sequencial gerado pelo sistema.
        titulo: texto obrigatório que identifica a tarefa.
        descricao: detalhamento livre (opcional) da tarefa.
        prioridade: "Alta", "Média" ou "Baixa".
        data_limite: data planejada para conclusão (DD/MM/AAAA).
        status: definido automaticamente como "Pendente" no cadastro.
    """

    id: int
    titulo: str
    descricao: str
    prioridade: str
    data_limite: str
    status: str = STATUS_PENDENTE

    def to_dict(self) -> dict:
        """Converte a tarefa em dicionário (usado na gravação em JSON)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, dados: dict) -> "Tarefa":
        """Cria uma tarefa a partir de um dicionário lido do JSON."""
        return cls(
            id=int(dados["id"]),
            titulo=dados["titulo"],
            descricao=dados.get("descricao", ""),
            prioridade=dados["prioridade"],
            data_limite=dados["data_limite"],
            status=dados.get("status", STATUS_PENDENTE),
        )
