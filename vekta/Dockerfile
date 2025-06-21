FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Vekta Team"
LABEL description="API REST pour la génération intelligente de séances d'entraînement cyclistes"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV PORT=8000

# Création du répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p /app/generated_workouts /app/chroma_db /app/logs

# Permissions
RUN chmod +x vekta_api.py

# Exposition du port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/health || exit 1

# Commande par défaut
CMD ["python", "-m", "uvicorn", "vekta_api:app", "--host", "0.0.0.0", "--port", "8000"] 