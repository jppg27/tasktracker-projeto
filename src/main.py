"""
main.py - Ponto de entrada do TaskTracker (aplicação CLI).

Exibe o menu principal em loop contínuo e conduz a interação com o
usuário, seguindo a "receita lógica" definida no Planejamento Lógico
(Fase 1). As validações ficam em utils.py.

Execução (a partir da raiz do projeto):
    python src/main.py
"""

from models import Tarefa
from utils import (
    normalizar_prioridade,
    validar_data_limite,
    validar_titulo,
)

LARGURA = 60

OPCOES_MENU = {
    "1": "Cadastrar nova tarefa",
    "2": "Visualizar tarefas cadastradas",
    "3": "Sair da aplicação",
}

tarefas = []


# ----------------------------------------------------------------------
# Funções auxiliares de exibição
# ----------------------------------------------------------------------
def exibir_cabecalho(titulo):
    print("\n" + "=" * LARGURA)
    print(titulo.center(LARGURA))
    print("=" * LARGURA)


def exibir_menu():
    exibir_cabecalho("TASKTRACKER - GERENCIADOR DE TAREFAS")
    for numero, descricao in OPCOES_MENU.items():
        print(f"  [{numero}] {descricao}")
    print("-" * LARGURA)


def exibir_tarefa(tarefa):
    """Exibe todas as propriedades de uma tarefa de forma legível."""
    print(f"  ID ..........: {tarefa.id}")
    print(f"  Título ......: {tarefa.titulo}")
    print(f"  Descrição ...: {tarefa.descricao or '(sem descrição)'}")
    print(f"  Prioridade ..: {tarefa.prioridade}")
    print(f"  Data limite .: {tarefa.data_limite}")
    print(f"  Status ......: {tarefa.status}")
    print("  " + "-" * (LARGURA - 2))


# ----------------------------------------------------------------------
# Funções de leitura e validação das entradas do usuário
# ----------------------------------------------------------------------
def ler_titulo():
    """Passos 2 e 3: solicita o título até que um valor não vazio seja informado."""
    while True:
        titulo = input("Título da tarefa: ")
        if validar_titulo(titulo):
            return titulo.strip()
        print("[ERRO] O título é obrigatório e não pode ficar em branco. Tente novamente.")


def ler_descricao():
    """Passo 4: solicita a descrição (campo opcional)."""
    return input("Descrição (opcional, pressione Enter para pular): ").strip()


def ler_prioridade():
    """Passos 5 e 6: solicita a prioridade até receber Alta, Média ou Baixa."""
    while True:
        prioridade = normalizar_prioridade(input("Prioridade (Alta / Média / Baixa): "))
        if prioridade is not None:
            return prioridade
        print("[ERRO] Prioridade inválida. Digite apenas Alta, Média (ou Media) ou Baixa.")


def ler_data_limite():
    """Passos 7 e 8: solicita a data limite até receber uma data válida e futura."""
    while True:
        data_limite = input("Data limite (DD/MM/AAAA): ").strip()
        valida, mensagem = validar_data_limite(data_limite)
        if valida:
            return data_limite
        print(f"[ERRO] {mensagem}")


# ----------------------------------------------------------------------
# Funcionalidades do menu
# ----------------------------------------------------------------------
def cadastrar_tarefa():
    """3.1 - Passo a passo do Cadastro de Tarefa."""
    exibir_cabecalho("CADASTRAR NOVA TAREFA")
    titulo = ler_titulo()
    descricao = ler_descricao()
    prioridade = ler_prioridade()
    data_limite = ler_data_limite()

    tarefa = Tarefa(len(tarefas) + 1, titulo, descricao, prioridade, data_limite)
    tarefas.append(tarefa)
    print(f"\n[OK] Tarefa \"{tarefa.titulo}\" cadastrada com sucesso! (ID {tarefa.id})")


def visualizar_tarefas():
    """3.2 - Passo a passo da Visualização de Tarefas."""
    exibir_cabecalho("TAREFAS CADASTRADAS")
    if not tarefas:
        print("Nenhuma tarefa cadastrada no momento.")
        return
    for tarefa in tarefas:
        exibir_tarefa(tarefa)
    print(f"Total de tarefas pendentes: {len(tarefas)}")


# ----------------------------------------------------------------------
# Loop principal
# ----------------------------------------------------------------------
def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_tarefa()
        elif opcao == "2":
            visualizar_tarefas()
        elif opcao == "3":
            print("\nObrigado por usar o TaskTracker. Até logo!")
            break
        else:
            print("[ERRO] Opção inválida. Escolha um número de 1 a 3.")
            continue

        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nAplicação encerrada pelo usuário. Até logo!")
