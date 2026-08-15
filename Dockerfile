# Usa uma imagem oficial do Python em versão estável
FROM python:3.12-slim-bookworm

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Variáveis do Python para não gerar bytecodes e logs imediatos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências nativas para o PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos
COPY requirements.txt /app/

# Atualiza pip e instala as dependências
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn psycopg2-binary django-environ whitenoise

# Copia todo o projeto para o diretório app
COPY . /app/
