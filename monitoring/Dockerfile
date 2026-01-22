FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY fraud_api_with_prometheus.py fraud_api.py
COPY fraud_detection_model.pkl .

# Exposer le port
EXPOSE 5000

# Lancer l'application
CMD ["python", "fraud_api.py"]
