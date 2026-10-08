# TaskTracker — Gerenciador de Tarefas em Linha de Comando

Aplicação CLI (Interface de Linha de Comando) em **Python 3** para registrar, consultar e controlar tarefas do dia a dia de forma simples e organizada.

> **Bootcamp II — Desafio Cumulativo · Fase 2 (Entrega Intermediária)**
> Estruturação do repositório, versionamento com Git/GitHub, implementação da lógica em Python e validação das regras de negócio.

| | |
|---|---|
| **Autor** | João Pedro Pinheiro Ghesti |
| **Curso** | Ciência de Dados e Machine Learning |
| **Polo** | Asa Norte |
| **Vídeo de apresentação** | _[cole aqui o link do vídeo no YouTube]_ |

---

## Sumário

- [O problema](#o-problema)
- [Funcionalidades](#funcionalidades)
- [Regras de negócio](#regras-de-negócio)
- [Estrutura de dados da tarefa](#estrutura-de-dados-da-tarefa)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Instalação](#instalação)
- [Execução](#execução)
- [Exemplo de uso](#exemplo-de-uso)
- [Testes automatizados](#testes-automatizados)
- [Histórico de versionamento](#histórico-de-versionamento)
- [Próximos passos (Fase 3)](#próximos-passos-fase-3)

---

## O problema

Pessoas e pequenas equipes lidam com várias tarefas ao mesmo tempo — acadêmicas, profissionais e pessoais — que acabam espalhadas entre papéis, aplicativos de mensagens ou apenas na memória. Isso causa esquecimento de prazos, falta de clareza sobre o que é mais urgente e pouca visibilidade sobre o que já foi concluído.

O **TaskTracker** centraliza essas atividades em um único ponto de controle, com prioridades, prazos e acompanhamento do progresso.

O planejamento lógico completo (Fase 1) está em [`docs/planejamento_logico.pdf`](docs/planejamento_logico.pdf).

## Funcionalidades

Menu principal em loop contínuo:

```
============================================================
            TASKTRACKER - GERENCIADOR DE TAREFAS
============================================================
  [1] Cadastrar nova tarefa
  [2] Visualizar tarefas cadastradas
  [3] Concluir tarefa
  [4] Remover tarefa
  [5] Exibir resumo
  [6] Sair da aplicação
------------------------------------------------------------
```

| Opção | O que faz |
|---|---|
| **1. Cadastrar nova tarefa** | Solicita título, descrição, prioridade e data limite, validando cada campo. A tarefa recebe um ID automático e o status `Pendente`. |
| **2. Visualizar tarefas cadastradas** | Lista as tarefas pendentes ordenadas por prioridade (Alta > Média > Baixa) e data limite, exibindo todas as propriedades e o total de pendentes. Mostra também o histórico de concluídas. Se não houver registros, informa que não existem tarefas no momento. |
| **3. Concluir tarefa** | Move uma tarefa pendente (pelo ID) para o histórico de concluídas. |
| **4. Remover tarefa** | Exclui uma tarefa pendente (pelo ID), após confirmação do usuário. |
| **5. Exibir resumo** | Mostra o total de tarefas pendentes, concluídas e o total geral. |
| **6. Sair da aplicação** | Encerra o programa. |

As tarefas são gravadas em `data/tarefas.json`, portanto continuam disponíveis na próxima execução.

## Regras de negócio

Regras definidas no Planejamento Lógico (Fase 1) e aplicadas no código:

1. **Título obrigatório** — entradas vazias ou compostas apenas por espaços são rejeitadas, e o sistema solicita nova digitação até que um título válido seja informado.
2. **Prioridade estrita** — aceita exclusivamente `Alta`, `Média` (ou `Media`) e `Baixa` (sem diferenciar maiúsculas/minúsculas). Qualquer outro valor gera mensagem de erro e repete a pergunta.
3. **Data limite válida** — deve estar no formato `DD/MM/AAAA`, existir no calendário e não ser anterior à data atual.
4. **ID único e sequencial** — gerado automaticamente; IDs de tarefas removidas não são reutilizados.
5. **ID existente** — uma tarefa só pode ser concluída ou removida se o seu ID existir na lista de pendentes.
6. **Histórico separado** — tarefas concluídas ficam em uma lista própria, separada das pendentes.

## Estrutura de dados da tarefa

Cada tarefa é um objeto da classe `Tarefa` (`src/models.py`), convertido em dicionário ao ser salvo:

| Campo | Tipo | Regra |
|---|---|---|
| `id` | int | Gerado automaticamente (único e sequencial) |
| `titulo` | str | Obrigatório, não pode ser vazio |
| `descricao` | str | Livre / opcional |
| `prioridade` | str | `Alta`, `Média` ou `Baixa` |
| `data_limite` | str | `DD/MM/AAAA`, não anterior a hoje |
| `status` | str | `Pendente` no cadastro; `Concluída` após a conclusão |

Exemplo de `data/tarefas.json`:

```json
{
  "proximo_id": 2,
  "pendentes": [
    {
      "id": 1,
      "titulo": "Estudar Git",
      "descricao": "Ler capítulo sobre branches",
      "prioridade": "Média",
      "data_limite": "20/10/2026",
      "status": "Pendente"
    }
  ],
  "concluidas": []
}
```

## Tecnologias utilizadas

- **Python 3.8+** — somente biblioteca padrão (`dataclasses`, `datetime`, `json`, `pathlib`, `re`)
- **pytest** — testes automatizados
- **Git** e **GitHub** — versionamento e publicação do código

## Estrutura do repositório

```
tasktracker-projeto/
├── README.md               # Documentação principal e instruções de uso
├── .gitignore              # Ignora __pycache__/, *.pyc, .venv/ e outros temporários
├── requirements.txt        # Dependências do projeto (pytest para os testes)
├── docs/
│   └── planejamento_logico.pdf   # Planejamento lógico e arquitetural da Fase 1
├── src/
│   ├── main.py             # Ponto de entrada: menu, loop principal e leitura das entradas
│   ├── models.py           # Estrutura da tarefa (classe Tarefa)
│   ├── gerenciador.py      # Regras de cadastro, listagem, conclusão, remoção e resumo
│   └── utils.py            # Validações de título, prioridade e data
├── tests/
│   ├── test_gerenciador.py # Testes das regras de negócio
│   └── test_utils.py       # Testes das funções de validação
└── data/
    └── tarefas.json        # Armazenamento das tarefas em disco
```

Cada arquivo de `src/` tem uma responsabilidade única, conforme o mapeamento arquitetural da Fase 1.

## Instalação

Pré-requisitos: **Python 3.8 ou superior** e **Git**.

```bash
# 1. Clonar o repositório
git clone https://github.com/<seu-usuario>/tasktracker-projeto.git
cd tasktracker-projeto

# 2. (Opcional) Criar e ativar um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# 3. Instalar as dependências (necessárias apenas para os testes)
pip install -r requirements.txt
```

## Execução

A partir da raiz do projeto:

```bash
python src/main.py
```

> No Linux/macOS, use `python3` caso o comando `python` aponte para outra versão.

## Exemplo de uso

Tentativa de cadastro com dados inválidos, seguida de correção:

```
============================================================
                   CADASTRAR NOVA TAREFA
============================================================
Título da tarefa:
[ERRO] O título é obrigatório e não pode ficar em branco. Tente novamente.
Título da tarefa: Estudar Git
Descrição (opcional, pressione Enter para pular): Ler capítulo sobre branches
Prioridade (Alta / Média / Baixa): Urgente
[ERRO] Prioridade inválida. Digite apenas Alta, Média (ou Media) ou Baixa.
Prioridade (Alta / Média / Baixa): media
Data limite (DD/MM/AAAA): 01/01/2020
[ERRO] A data limite não pode ser anterior à data atual (08/10/2026).
Data limite (DD/MM/AAAA): 20/10/2026

[OK] Tarefa "Estudar Git" cadastrada com sucesso! (ID 1)
```

Visualização:

```
============================================================
                    TAREFAS CADASTRADAS
============================================================
TAREFAS PENDENTES (ordenadas por prioridade e data limite)

  ID ..........: 1
  Título ......: Estudar Git
  Descrição ...: Ler capítulo sobre branches
  Prioridade ..: Média
  Data limite .: 20/10/2026
  Status ......: Pendente
  ----------------------------------------------------------
Total de tarefas pendentes: 1
```

## Testes automatizados

```bash
python -m pytest -v
```

Os testes cobrem as validações de título, prioridade e data (`tests/test_utils.py`) e as regras de cadastro, ordenação, conclusão, remoção, resumo e persistência (`tests/test_gerenciador.py`). Eles usam arquivos temporários e não alteram `data/tarefas.json`.

## Histórico de versionamento

O desenvolvimento foi registrado em commits incrementais:

1. Commit inicial com `README.md`, `.gitignore` e o documento da Fase 1 (`docs/planejamento_logico.pdf`);
2. Estrutura principal em `src/main.py` (menu e loop principal) e modelo da tarefa;
3. Funções de validação de dados (título não vazio, prioridade e data limite);
4. Gerenciador de tarefas com ID sequencial, ordenação, conclusão, remoção e resumo;
5. Persistência das tarefas em `data/tarefas.json`;
6. Testes automatizados e `requirements.txt`;
7. Documentação final do README.

Para consultar: `git log --oneline`.

## Próximos passos (Fase 3)

- Empacotamento da aplicação;
- Containerização com **Docker** (`Dockerfile`);
- Ampliação dos testes automatizados;
- Deploy.
