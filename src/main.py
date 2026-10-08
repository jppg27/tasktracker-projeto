"""
main.py - Ponto de entrada do TaskTracker (aplicação CLI).

Exibe o menu principal em loop contínuo e conduz a interação com o
usuário, seguindo a "receita lógica" definida no Planejamento Lógico
(Fase 1).

Execução (a partir da raiz do projeto):
    python src/main.py
"""

from models import Tarefa

LARGURA = 60

OPCOES_MENU = {
    "1": "Cadastrar nova tarefa",
    "2": "Visualizar tarefas cadastradas",
    "3": "Sair da aplicação",
}

tarefas = []


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


def cadastrar_tarefa():
    """3.1 - Cadastro de Tarefa (versão inicial, sem validações)."""
    exibir_cabecalho("CADASTRAR NOVA TAREFA")
    titulo = input("Título da tarefa: ").strip()
    descricao = input("Descrição (opcional, pressione Enter para pular): ").strip()
    prioridade = input("Prioridade (Alta / Média / Baixa): ").strip()
    data_limite = input("Data limite (DD/MM/AAAA): ").strip()

    tarefa = Tarefa(len(tarefas) + 1, titulo, descricao, prioridade, data_limite)
    tarefas.append(tarefa)
    print(f"\n[OK] Tarefa \"{tarefa.titulo}\" cadastrada com sucesso! (ID {tarefa.id})")


def visualizar_tarefas():
    """3.2 - Visualização de Tarefas."""
    exibir_cabecalho("TAREFAS CADASTRADAS")
    if not tarefas:
        print("Nenhuma tarefa cadastrada no momento.")
        return
    for tarefa in tarefas:
        exibir_tarefa(tarefa)
    print(f"Total de tarefas pendentes: {len(tarefas)}")


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
