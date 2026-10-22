# TaskTracker — Gerenciador de Tarefas em Linha de Comando

Aplicação CLI (Interface de Linha de Comando) em **Python 3** para registrar, consultar e controlar tarefas do dia a dia, empacotada com **Docker** para rodar de forma idêntica em qualquer ambiente.

> **Bootcamp II — Desafio Cumulativo · Fase 3 (Entrega Final)**
> Conteinerização, orquestração e deploy do TaskTracker.

| | |
|---|---|
| **Autor** | João Pedro Pinheiro Ghesti |
| **Curso** | Ciência de Dados e Machine Learning |
| **Polo** | Asa Norte |
| **Vídeo de apresentação — Fase 3** | _[cole aqui o link do vídeo no YouTube]_ |

---

## Sumário

- [Execução com Docker (início rápido)](#execução-com-docker-início-rápido)
- [Como a conteinerização funciona](#como-a-conteinerização-funciona)
- [O problema](#o-problema)
- [Funcionalidades](#funcionalidades)
- [Regras de negócio](#regras-de-negócio)
- [Estrutura de dados da tarefa](#estrutura-de-dados-da-tarefa)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Execução local (sem Docker)](#execução-local-sem-docker)
- [Exemplo de uso](#exemplo-de-uso)
- [Testes automatizados](#testes-automatizados)
- [Histórico de versionamento](#histórico-de-versionamento)
- [Evolução do projeto](#evolução-do-projeto)

---

## Execução com Docker (início rápido)

**Pré-requisito:** [Docker](https://docs.docker.com/get-docker/) instalado (Docker Desktop no Windows/macOS ou Docker Engine + plugin Compose no Linux). Não é necessário ter Python instalado na máquina.

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/<seu-usuario>/tasktracker-projeto.git
cd tasktracker-projeto
```

### 1. Como construir a imagem

```bash
docker build -t tasktracker-app .
```

### 2. Como rodar o container em modo isolado

```bash
docker run -it --rm tasktracker-app
```

- `-i` mantém a entrada de dados aberta para o `input()` da aplicação;
- `-t` aloca um terminal virtual, simulando o console;
- `--rm` remove o container ao sair do programa.

> Neste modo as tarefas ficam apenas dentro do container e são descartadas ao sair. Para guardá-las, use a orquestração (abaixo) ou acrescente um volume: `docker run -it --rm -v tasktracker-dados:/app/data tasktracker-app`.

### 3. Como rodar via orquestração (recomendado)

```bash
docker compose run --rm tasktracker-app
```

O `docker-compose.yml` já define o build, o modo interativo (`stdin_open` e `tty`) e um volume que **mantém as tarefas salvas entre execuções**. Na primeira vez, o Compose constrói a imagem automaticamente; para reconstruí-la após alterar o código, use `docker compose build`.

> Use `docker compose run`, e não `docker compose up`: o `up` não conecta o teclado ao menu da aplicação.

### Comandos úteis

| Objetivo | Comando |
|---|---|
| Listar a imagem criada | `docker images tasktracker-app` |
| Reconstruir a imagem pelo Compose | `docker compose build` |
| Apagar as tarefas salvas no volume | `docker compose down -v` |

## Como a conteinerização funciona

| | `Dockerfile` (a receita) | `docker-compose.yml` (o maestro) |
|---|---|---|
| **Papel** | Empacota a aplicação e suas dependências | Orquestra a execução interativa da CLI |
| **Saída** | Gera a imagem `tasktracker-app` | Roda o container com os parâmetros definidos |
| **Comando-chave** | `docker build` | `docker compose run` |

### Decisões do `Dockerfile`

| Instrução | Por quê |
|---|---|
| `FROM python:3.11-slim` | Base leve e oficial com Python 3.11, sem pacotes desnecessários. |
| `ENV PYTHONUNBUFFERED=1` | Envia a saída do `print()` imediatamente ao terminal, sem buffer. |
| `ENV PYTHONDONTWRITEBYTECODE=1` | Evita criar `__pycache__/` e `.pyc` dentro do container. |
| `ENV PYTHONIOENCODING=utf-8` | Garante acentuação correta na entrada e na saída (ex.: `Média`). |
| `ENV TZ="<-03>3"` | Fuso de Brasília (UTC-3), para que a regra "data limite não pode ser anterior a hoje" use a data local. |
| `WORKDIR /app` | Define a pasta central de operações. |
| `RUN useradd ... appuser` + `USER appuser` | Executa a aplicação sem privilégios de administrador (boa prática de segurança). |
| `COPY src/ /app/src/` e `COPY data/ /app/data/` | Injeta o código-fonte e a pasta de dados no container. |
| `CMD ["python", "src/main.py"]` | Gatilho que dispara a execução da aplicação. |

A aplicação usa apenas a biblioteca padrão do Python, então a imagem não precisa de `pip install`. O arquivo `.dockerignore` deixa de fora do build o que não é necessário para rodar (testes, documentação, `.git`, caches), deixando o build mais rápido e a imagem mais leve.

### Orquestração e interatividade

A CLI usa `input()`, e um container isolado não recebe dados do teclado por padrão. O `docker-compose.yml` cria esse canal:

```yaml
services:
  tasktracker-app:
    build: { context: ., dockerfile: Dockerfile }
    image: tasktracker-app
    stdin_open: true   # mantém a entrada de dados aberta (equivale a -i)
    tty: true          # aloca um terminal virtual (equivale a -t)
    volumes:
      - tasktracker-dados:/app/data   # persiste data/tarefas.json

volumes:
  tasktracker-dados:
```

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

As tarefas são gravadas em `data/tarefas.json`, portanto continuam disponíveis na próxima execução (no Docker, dentro do volume `tasktracker-dados`).

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

- **Python 3** (3.11 na imagem Docker; 3.8+ para execução local) — somente biblioteca padrão (`dataclasses`, `datetime`, `json`, `pathlib`, `re`)
- **Docker** e **Docker Compose** — empacotamento e orquestração
- **pytest** — testes automatizados
- **Git** e **GitHub** — versionamento e publicação do código

## Estrutura do repositório

```
tasktracker-projeto/
├── .gitignore              # Ignora __pycache__/, *.pyc, .venv/ e outros temporários
├── .dockerignore           # Arquivos que ficam fora do build da imagem
├── Dockerfile              # Receita da imagem Docker (Fase 3)
├── docker-compose.yml      # Orquestração da execução interativa (Fase 3)
├── README.md               # Documentação principal e instruções de uso
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

## Execução local (sem Docker)

Alternativa para desenvolvimento. Pré-requisitos: **Python 3.8 ou superior** e **Git**.

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

Para executar, a partir da raiz do projeto:

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
[ERRO] A data limite não pode ser anterior à data atual (22/10/2026).
Data limite (DD/MM/AAAA): 30/10/2026

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
  Data limite .: 30/10/2026
  Status ......: Pendente
  ----------------------------------------------------------
Total de tarefas pendentes: 1
```

## Testes automatizados

Localmente:

```bash
python -m pytest -v
```

Os testes cobrem as validações de título, prioridade e data (`tests/test_utils.py`) e as regras de cadastro, ordenação, conclusão, remoção, resumo e persistência (`tests/test_gerenciador.py`). Eles usam arquivos temporários e não alteram `data/tarefas.json`.

## Histórico de versionamento

O desenvolvimento foi registrado em commits incrementais, mantidos desde a Fase 2:

**Fase 2 — Desenvolvimento**

1. Commit inicial com `README.md`, `.gitignore` e o documento da Fase 1 (`docs/planejamento_logico.pdf`);
2. Estrutura principal em `src/main.py` (menu e loop principal) e modelo da tarefa;
3. Funções de validação de dados (título não vazio, prioridade e data limite);
4. Gerenciador de tarefas com ID sequencial, ordenação, conclusão, remoção e resumo;
5. Persistência das tarefas em `data/tarefas.json`;
6. Testes automatizados e `requirements.txt`;
7. Documentação do README.

**Fase 3 — Conteinerização e orquestração**

8. `Dockerfile` e `.dockerignore` para empacotar a aplicação;
9. `docker-compose.yml` para a execução interativa da CLI com volume de dados;
10. README atualizado com o guia Docker.

Para consultar: `git log --oneline`.

## Evolução do projeto

| Fase | Papel | Entrega |
|---|---|---|
| **Fase 1** | Arquiteto(a) de Software | Planejamento lógico, decomposição do problema e algoritmo em português ([`docs/planejamento_logico.pdf`](docs/planejamento_logico.pdf)) |
| **Fase 2** | Desenvolvedor(a) | Código Python versionado com menu CLI e regras de negócio (`src/`) |
| **Fase 3** | Engenheiro(a) DevOps | Imagem Docker e orquestração com Docker Compose (`Dockerfile`, `docker-compose.yml`) |

O projeto saiu de um planejamento em papel, virou código que funciona na máquina do desenvolvedor e agora roda de forma idêntica em qualquer ambiente com Docker.
