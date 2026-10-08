"""
main.py - Ponto de entrada do TaskTracker (aplicação CLI).

Exibe o menu principal em loop contínuo e conduz a interação com o
usuário, seguindo a "receita lógica" definida no Planejamento Lógico
(Fase 1). As regras de negócio ficam em gerenciador.py e as validações
em utils.py.

Execução (a partir da raiz do projeto):
    python src/main.py
"""

from gerenciador import GerenciadorTarefas, TarefaNaoEncontradaError
from utils import (
    normalizar_prioridade,
    validar_data_limite,
    validar_titulo,
)

LARGURA = 60

OPCOES_MENU = {
    "1": "Cadastrar nova tarefa",
    "2": "Visualizar tarefas cadastradas",
    "3": "Concluir tarefa",
    "4": "Remover tarefa",
    "5": "Exibir resumo",
    "6": "Sair da aplicação",
}


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


def exibir_lista_resumida(tarefas):
    """Exibe as tarefas pendentes em formato de tabela compacta (ID e dados)."""
    print(f"  {'ID':<5}{'TÍTULO':<28}{'PRIORIDADE':<12}{'PRAZO':<10}")
    for tarefa in tarefas:
        titulo = tarefa.titulo if len(tarefa.titulo) <= 26 else tarefa.titulo[:23] + "..."
        print(f"  {tarefa.id:<5}{titulo:<28}{tarefa.prioridade:<12}{tarefa.data_limite:<10}")
    print()


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


def ler_id(mensagem):
    """Solicita um ID numérico. Retorna None se o usuário digitar 0 (cancelar)."""
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            numero = int(valor)
            return None if numero == 0 else numero
        print("[ERRO] Digite um número de ID válido (ou 0 para cancelar).")


def confirmar(mensagem):
    """Solicita confirmação do tipo S/N e retorna True para 'S'."""
    while True:
        resposta = input(f"{mensagem} (S/N): ").strip().upper()
        if resposta in ("S", "SIM"):
            return True
        if resposta in ("N", "NAO", "NÃO"):
            return False
        print("[ERRO] Responda apenas com S ou N.")


# ----------------------------------------------------------------------
# Funcionalidades do menu
# ----------------------------------------------------------------------
def cadastrar_tarefa(gerenciador):
    """3.1 - Passo a passo do Cadastro de Tarefa."""
    exibir_cabecalho("CADASTRAR NOVA TAREFA")
    titulo = ler_titulo()
    descricao = ler_descricao()
    prioridade = ler_prioridade()
    data_limite = ler_data_limite()

    # Passos 9 e 10: o gerenciador gera o ID e salva como "Pendente".
    tarefa = gerenciador.cadastrar(titulo, descricao, prioridade, data_limite)

    # Passo 11: mensagem de sucesso.
    print(f"\n[OK] Tarefa \"{tarefa.titulo}\" cadastrada com sucesso! (ID {tarefa.id})")


def visualizar_tarefas(gerenciador):
    """3.2 - Passo a passo da Visualização de Tarefas."""
    exibir_cabecalho("TAREFAS CADASTRADAS")
    pendentes = gerenciador.listar_pendentes()
    concluidas = gerenciador.listar_concluidas()

    if not pendentes and not concluidas:
        print("Nenhuma tarefa cadastrada no momento.")
        return

    print("TAREFAS PENDENTES (ordenadas por prioridade e data limite)\n")
    if pendentes:
        for tarefa in pendentes:
            exibir_tarefa(tarefa)
    else:
        print("  Não há tarefas pendentes no momento.\n")
    print(f"Total de tarefas pendentes: {len(pendentes)}")

    if concluidas:
        print("\nHISTÓRICO DE TAREFAS CONCLUÍDAS\n")
        for tarefa in concluidas:
            exibir_tarefa(tarefa)
        print(f"Total de tarefas concluídas: {len(concluidas)}")


def concluir_tarefa(gerenciador):
    """3.3 - Passo a passo para Marcar Tarefa como Concluída."""
    exibir_cabecalho("CONCLUIR TAREFA")
    pendentes = gerenciador.listar_pendentes()
    if not pendentes:
        print("Não há tarefas pendentes para concluir.")
        return

    exibir_lista_resumida(pendentes)
    while True:
        id_tarefa = ler_id("ID da tarefa a concluir (0 para cancelar): ")
        if id_tarefa is None:
            print("Operação cancelada.")
            return
        try:
            tarefa = gerenciador.concluir(id_tarefa)
            break
        except TarefaNaoEncontradaError as erro:
            print(f"[ERRO] {erro} Tente novamente.")

    print(f"\n[OK] Tarefa \"{tarefa.titulo}\" concluída e movida para o histórico.")


def remover_tarefa(gerenciador):
    """3.4 - Passo a passo para Remoção de Tarefa."""
    exibir_cabecalho("REMOVER TAREFA")
    pendentes = gerenciador.listar_pendentes()
    if not pendentes:
        print("Não há tarefas pendentes para remover.")
        return

    exibir_lista_resumida(pendentes)
    id_tarefa = ler_id("ID da tarefa a remover (0 para cancelar): ")
    if id_tarefa is None:
        print("Operação cancelada.")
        return

    tarefa = gerenciador.buscar_pendente(id_tarefa)
    if tarefa is None:
        print(f"[ERRO] Não existe tarefa pendente com o ID {id_tarefa}.")
        return

    if not confirmar(f"Confirma a remoção da tarefa \"{tarefa.titulo}\"?"):
        print("Remoção cancelada.")
        return

    gerenciador.remover(id_tarefa)
    print(f"\n[OK] Tarefa \"{tarefa.titulo}\" removida com sucesso.")


def exibir_resumo(gerenciador):
    """Resumo com o total de tarefas pendentes e concluídas."""
    exibir_cabecalho("RESUMO DO PROGRESSO")
    resumo = gerenciador.resumo()
    print(f"  Tarefas pendentes ..: {resumo['pendentes']}")
    print(f"  Tarefas concluídas .: {resumo['concluidas']}")
    print(f"  Total de tarefas ...: {resumo['total']}")


# ----------------------------------------------------------------------
# Loop principal
# ----------------------------------------------------------------------
def main():
    gerenciador = GerenciadorTarefas()

    acoes = {
        "1": cadastrar_tarefa,
        "2": visualizar_tarefas,
        "3": concluir_tarefa,
        "4": remover_tarefa,
        "5": exibir_resumo,
    }

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "6":
            print("\nObrigado por usar o TaskTracker. Até logo!")
            break

        acao = acoes.get(opcao)
        if acao is None:
            print("[ERRO] Opção inválida. Escolha um número de 1 a 6.")
            continue

        acao(gerenciador)
        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nAplicação encerrada pelo usuário. Até logo!")
