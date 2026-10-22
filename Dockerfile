# ----------------------------------------------------------------------
# Dockerfile - TaskTracker (Fase 3: Conteinerização)
#
# Empacota a aplicação CLI em uma imagem leve e autossuficiente.
#   Construir a imagem:  docker build -t tasktracker-app .
#   Executar:            docker run -it --rm tasktracker-app
# ----------------------------------------------------------------------

# Imagem base leve: Python 3.11 sobre Debian "slim" (sem pacotes desnecessários).
FROM python:3.11-slim

# PYTHONUNBUFFERED=1        -> envia a saída do print() imediatamente ao terminal (sem buffer).
# PYTHONDONTWRITEBYTECODE=1 -> evita gerar arquivos .pyc/__pycache__ dentro do container.
# PYTHONIOENCODING=utf-8    -> garante acentos corretos na entrada e saída (ex.: "Média").
# TZ="<-03>3"               -> fuso de Brasília (UTC-3) em formato POSIX, que não depende do
#                              pacote tzdata. Assim a regra "data limite não pode ser anterior
#                              a hoje" usa a data local, e não a data em UTC.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    TZ="<-03>3"

# Pasta central de operações dentro do container.
WORKDIR /app

# Usuário sem privilégios de administrador (boa prática de segurança).
RUN useradd --create-home --uid 1000 appuser

# Injeta o código-fonte e a pasta de dados no container.
# A aplicação usa apenas a biblioteca padrão do Python, então não há "pip install".
COPY --chown=appuser:appuser src/ /app/src/
COPY --chown=appuser:appuser data/ /app/data/

USER appuser

# Gatilho que dispara a execução da aplicação.
CMD ["python", "src/main.py"]
