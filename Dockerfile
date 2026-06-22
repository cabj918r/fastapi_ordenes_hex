# ==========================================
# ETAPA 1: Builder (Compilación y pruebas)
# ==========================================
FROM python:3.14-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar ciertas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry de forma oficial
ENV POETRY_VERSION=2.0.1
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copiar archivos de configuración de dependencias
COPY pyproject.toml poetry.lock ./

# Configurar Poetry para que cree el entorno virtual dentro de la carpeta del proyecto
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# Copiar el código de la aplicación
COPY app/ ./app

# ==========================================
# ETAPA 2: Runner (Imagen final de producción)
# ==========================================
FROM python:3.14-slim AS runner

WORKDIR /app

# Instalar solo la librería de Postgres para tiempo de ejecución
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar el entorno virtual con las librerías ya compiladas desde el builder
COPY --from=builder /app/.venv /app/.venv
COPY app/ ./app

# Variables de entorno para asegurar que Python no use caché y use el venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Comando para levantar la API con Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
