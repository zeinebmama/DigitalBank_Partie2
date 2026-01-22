# Guide d'Installation et Déploiement
## Plateforme DigitalBank Fraud Detection

**Version** : 1.0  
**Date** : Janvier 2026  
**Public cible** : Équipe technique, DevOps, Administrateurs système

---

## 📋 Table des Matières

1. [Prérequis Techniques](#prerequis)
2. [Architecture de Déploiement](#architecture)
3. [Installation de la Base de Données (Supabase)](#database)
4. [Déploiement de l'API de Détection de Fraude](#api)
5. [Configuration des Dashboards Metabase](#metabase)
6. [Mise en Place des Workflows Make.com](#workflows)
7. [Configuration du Monitoring (Prometheus + Grafana)](#monitoring)
8. [Variables d'Environnement](#env-vars)
9. [Lancement et Vérification](#launch)
10. [Dépannage et Erreurs Courantes](#troubleshooting)
11. [Maintenance et Mise à Jour](#maintenance)

---

## 1. Prérequis Techniques {#prerequis}

### 🖥️ Infrastructure Requise

#### Environnement de Développement (Local)

| Composant | Spécification Minimum | Recommandé |
|-----------|----------------------|------------|
| **OS** | Linux (Ubuntu 20.04+), macOS 11+, Windows 10+ avec WSL2 | Ubuntu 22.04 LTS |
| **CPU** | 4 cores | 8 cores |
| **RAM** | 8 GB | 16 GB |
| **Disque** | 50 GB disponible | 100 GB SSD |
| **Réseau** | 10 Mbps | 100 Mbps |

#### Environnement de Production

| Service | Configuration | Coût Estimé |
|---------|--------------|-------------|
| **Serveur API** | 4 vCPU, 8 GB RAM, 100 GB SSD | ~80€/mois |
| **Base de Données** | Managed PostgreSQL 15, 2 vCPU, 4 GB RAM, réplication activée | ~120€/mois |
| **Monitoring** | 2 vCPU, 4 GB RAM, 50 GB SSD | ~40€/mois |
| **Bande passante** | 1 TB/mois | ~15€/mois |
| **Total** | | **~255€/mois** |

**💡 Note** : Coûts basés sur cloud providers (DigitalOcean, AWS, GCP). Pour projet académique, utilisation tier gratuit possible.

### 📦 Logiciels et Outils

#### Obligatoires

```bash
# Vérifier les versions installées
git --version          # >= 2.30
docker --version       # >= 20.10
docker-compose --version # >= 2.0
python --version       # >= 3.10
node --version         # >= 18.0
npm --version          # >= 9.0
psql --version         # >= 14.0 (client PostgreSQL)
```

#### Installation des Dépendances (Ubuntu/Debian)

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des paquets de base
sudo apt install -y \
    git \
    curl \
    wget \
    vim \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3.10 \
    python3.10-venv \
    python3-pip \
    postgresql-client-14

# Installation Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Installation Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Installation Node.js (via nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
```

#### Optionnels (Recommandés)

- **kubectl** : Orchestration Kubernetes (si déploiement K8s)
- **helm** : Package manager Kubernetes
- **terraform** : Infrastructure as Code
- **httpie** : Client HTTP en CLI (alternative à curl)
- **jq** : Parser JSON en CLI

```bash
# Installation kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Installation helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Installation terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Installation httpie et jq
sudo apt install -y httpie jq
```

### 🔑 Comptes et Accès Requis

#### Services Cloud

1. **Supabase** (Base de Données)
   - URL : https://supabase.com
   - Plan : Free (2 projets) ou Pro ($25/mois)
   - Créer un compte avec email professionnel
   - Activer 2FA

2. **Make.com** (Automatisation)
   - URL : https://make.com
   - Plan : Free (1000 opérations/mois) ou Core ($9/mois)
   - Vérifier email après inscription

3. **Metabase Cloud** (optionnel, alternative self-hosted disponible)
   - URL : https://www.metabase.com/start/hosted
   - Plan : Pro ($85/mois) - Essai gratuit 14 jours
   - Ou utiliser version open-source gratuite

#### Accès GitHub (si repository privé)

```bash
# Configuration Git
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@esic.edu"

# Génération clé SSH
ssh-keygen -t ed25519 -C "votre.email@esic.edu"
cat ~/.ssh/id_ed25519.pub
# Copier la clé et l'ajouter sur GitHub : Settings → SSH Keys
```

---

## 2. Architecture de Déploiement {#architecture}

### 📐 Schéma d'Infrastructure

```
┌─────────────────────────────────────────────────────┐
│                 INTERNET                            │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────▼────────┐
         │  Load Balancer │ (NGINX / Cloudflare)
         │   (SSL/TLS)    │
         └───────┬────────┘
                 │
     ┌───────────┼────────────┐
     │           │            │
┌────▼────┐ ┌───▼────┐ ┌─────▼────┐
│ API-1   │ │ API-2  │ │  API-3   │ (Autoscaling)
│ (Docker)│ │(Docker)│ │ (Docker) │
└────┬────┘ └───┬────┘ └─────┬────┘
     │          │            │
     └──────────┼────────────┘
                │
         ┌──────▼──────────┐
         │  Supabase DB    │ (PostgreSQL 15)
         │  (Primary)      │
         └─────────────────┘
                │
         ┌──────▼──────────┐
         │  Replica DB     │ (Read-only)
         └─────────────────┘

┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Metabase      │───▶│  Supabase    │◀───│  Make.com   │
│  (Dashboards)   │    │  (Database)  │    │ (Workflows) │
└─────────────────┘    └──────────────┘    └─────────────┘

┌─────────────────┐    ┌──────────────┐
│   Prometheus    │───▶│   Grafana    │
│  (Metrics)      │    │ (Monitoring) │
└─────────────────┘    └──────────────┘
```

### 🌐 Stratégies de Déploiement

#### Option 1 : Docker Compose (Développement / Small Scale)

**Avantages** :
- ✅ Simple à mettre en place
- ✅ Faible coût (1 serveur VPS suffit)
- ✅ Idéal pour POC et environnement académique

**Limites** :
- ❌ Scalabilité limitée
- ❌ Pas de haute disponibilité native
- ❌ Maintenance manuelle

**Recommandé pour** : Projet ESIC, MVP, tests

#### Option 2 : Kubernetes (Production / Enterprise)

**Avantages** :
- ✅ Autoscaling automatique
- ✅ Haute disponibilité (self-healing)
- ✅ Rolling updates sans downtime
- ✅ Gestion multi-environnements (dev/staging/prod)

**Limites** :
- ❌ Complexité accrue
- ❌ Coût infrastructure plus élevé
- ❌ Expertise K8s requise

**Recommandé pour** : Production avec trafic élevé, SLA strict

---

## 3. Installation de la Base de Données (Supabase) {#database}

### 🗄️ Création du Projet Supabase

#### Étape 1 : Création du Projet

1. Connectez-vous à https://app.supabase.com
2. Cliquez sur **"New Project"**
3. Remplissez les informations :
   - **Name** : `digitalbank-fraud-production`
   - **Database Password** : Générer un mot de passe fort (32 caractères)
   - **Region** : `Europe (Frankfurt)` ou le plus proche de vos utilisateurs
   - **Pricing Plan** : Free (dev) ou Pro (production)
4. Cliquez sur **"Create new project"**
5. ⏳ Attendre ~2 minutes (provisioning database)

#### Étape 2 : Récupération des Credentials

Dans l'interface Supabase, allez dans **Settings → Database** :

```bash
# Notez ces informations (à mettre dans .env plus tard)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (CONFIDENTIEL)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

⚠️ **Sécurité** : NE JAMAIS commiter le `SERVICE_ROLE_KEY` dans Git.

### 📊 Création du Schéma de Base de Données

#### Méthode 1 : Via l'Interface Supabase SQL Editor

1. Dans Supabase Dashboard, allez dans **SQL Editor**
2. Cliquez sur **"New Query"**
3. Collez le script SQL ci-dessous
4. Cliquez sur **"Run"**

#### Méthode 2 : Via psql (CLI)

```bash
# Connexion à la base
psql "postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres"

# Exécuter le fichier de migration
\i database/migrations/001_initial_schema.sql
```

#### Script SQL : Schéma Initial

```sql
-- =========================================
-- Schema Initial - DigitalBank Fraud Detection
-- Version: 1.0
-- Date: 2026-01-22
-- =========================================

-- Extension pour UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Extension pour chiffrement
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Extension pour géolocalisation
CREATE EXTENSION IF NOT EXISTS "postgis";

-- =========================================
-- TABLE : users
-- Description : Profils clients
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    country_code CHAR(2), -- ISO 3166-1 alpha-2
    date_of_birth DATE,
    account_created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    risk_level VARCHAR(20) DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH
    kyc_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP WITH TIME ZONE,
    metadata JSONB, -- Données supplémentaires flexibles
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour performances
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_risk_level ON users(risk_level);
CREATE INDEX idx_users_country ON users(country_code);

-- =========================================
-- TABLE : transactions
-- Description : Historique transactionnel
-- =========================================
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    amount DECIMAL(12, 2) NOT NULL,
    currency CHAR(3) DEFAULT 'EUR',
    merchant_name VARCHAR(255),
    merchant_category VARCHAR(4), -- MCC code
    merchant_country CHAR(2),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    device_id VARCHAR(255),
    ip_address INET,
    user_location GEOGRAPHY(POINT),
    merchant_location GEOGRAPHY(POINT),
    card_present BOOLEAN DEFAULT FALSE,
    transaction_type VARCHAR(50), -- PURCHASE, WITHDRAWAL, REFUND, etc.
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, APPROVED, DECLINED, FLAGGED
    fraud_score DECIMAL(5, 4), -- 0.0000 to 1.0000
    risk_level VARCHAR(20), -- LOW, MEDIUM, HIGH, CRITICAL
    model_version VARCHAR(50),
    processing_time_ms INTEGER,
    additional_context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index critiques pour performances
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC);
CREATE INDEX idx_transactions_fraud_score ON transactions(fraud_score DESC);
CREATE INDEX idx_transactions_risk_level ON transactions(risk_level);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_transactions_merchant_country ON transactions(merchant_country);

-- Index composite pour requêtes fréquentes
CREATE INDEX idx_transactions_user_timestamp ON transactions(user_id, timestamp DESC);
CREATE INDEX idx_transactions_risk_timestamp ON transactions(risk_level, timestamp DESC);

-- =========================================
-- TABLE : alerts
-- Description : Alertes de fraude
-- =========================================
CREATE TABLE IF NOT EXISTS alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id UUID REFERENCES transactions(transaction_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    risk_level VARCHAR(20) NOT NULL, -- MEDIUM, HIGH, CRITICAL
    fraud_score DECIMAL(5, 4),
    alert_type VARCHAR(50), -- AUTO_GENERATED, MANUAL, ESCALATED
    status VARCHAR(20) DEFAULT 'NEW', -- NEW, ASSIGNED, IN_PROGRESS, RESOLVED, ESCALATED
    priority INTEGER DEFAULT 3, -- 1=Urgent, 2=High, 3=Normal, 4=Low
    assigned_to VARCHAR(255), -- Analyst email or ID
    resolution VARCHAR(50), -- FRAUD_CONFIRMED, FALSE_POSITIVE, PENDING
    resolution_notes TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by VARCHAR(255),
    sla_deadline TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour dashboard analystes
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_priority ON alerts(priority);
CREATE INDEX idx_alerts_assigned ON alerts(assigned_to);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);
CREATE INDEX idx_alerts_sla ON alerts(sla_deadline) WHERE status != 'RESOLVED';

-- =========================================
-- TABLE : audit_logs
-- Description : Logs d'audit pour conformité
-- =========================================
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL, -- LOGIN, VIEW_TRANSACTION, UPDATE_ALERT, etc.
    resource_type VARCHAR(50), -- TRANSACTION, ALERT, USER, CONFIG
    resource_id UUID,
    actor VARCHAR(255), -- Email ou ID de l'utilisateur effectuant l'action
    actor_ip INET,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour requêtes audit
CREATE INDEX idx_audit_actor ON audit_logs(actor);
CREATE INDEX idx_audit_action ON audit_logs(action);
CREATE INDEX idx_audit_created ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_resource ON audit_logs(resource_type, resource_id);

-- =========================================
-- TABLE : ml_models
-- Description : Versioning des modèles ML
-- =========================================
CREATE TABLE IF NOT EXISTS ml_models (
    model_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version VARCHAR(50) UNIQUE NOT NULL,
    algorithm VARCHAR(100),
    trained_date TIMESTAMP WITH TIME ZONE,
    deployed_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT FALSE,
    performance_metrics JSONB, -- accuracy, precision, recall, etc.
    training_dataset_info JSONB,
    features_count INTEGER,
    model_file_path TEXT, -- Chemin S3 ou local
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Un seul modèle actif à la fois
CREATE UNIQUE INDEX idx_ml_models_active ON ml_models(is_active) WHERE is_active = TRUE;

-- =========================================
-- VIEWS : Vues matérialisées pour dashboards
-- =========================================

-- Vue : Statistiques quotidiennes fraudes
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_fraud_stats AS
SELECT
    DATE(timestamp) as date,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as fraud_count,
    SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN amount ELSE 0 END) as fraud_amount,
    AVG(fraud_score) as avg_fraud_score,
    AVG(processing_time_ms) as avg_processing_time
FROM transactions
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Index sur la vue matérialisée
CREATE UNIQUE INDEX idx_daily_fraud_stats_date ON daily_fraud_stats(date);

-- Refresh automatique (à scheduler via cron ou pg_cron)
-- SELECT cron.schedule('refresh_daily_stats', '0 1 * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY daily_fraud_stats');

-- Vue : Top merchants à risque
CREATE MATERIALIZED VIEW IF NOT EXISTS top_risky_merchants AS
SELECT
    merchant_name,
    merchant_category,
    merchant_country,
    COUNT(*) as transaction_count,
    SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END) as fraud_count,
    (SUM(CASE WHEN risk_level IN ('HIGH', 'CRITICAL') THEN 1 ELSE 0 END)::FLOAT / COUNT(*)) as fraud_rate,
    SUM(amount) as total_amount
FROM transactions
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY merchant_name, merchant_category, merchant_country
HAVING COUNT(*) > 10 -- Minimum 10 transactions pour statistiques fiables
ORDER BY fraud_count DESC
LIMIT 100;

-- =========================================
-- FUNCTIONS : Fonctions utilitaires
-- =========================================

-- Fonction : Calcul distance entre 2 points (km)
CREATE OR REPLACE FUNCTION calculate_distance(
    lat1 FLOAT, lon1 FLOAT,
    lat2 FLOAT, lon2 FLOAT
) RETURNS FLOAT AS $$
BEGIN
    RETURN ST_Distance(
        ST_MakePoint(lon1, lat1)::geography,
        ST_MakePoint(lon2, lat2)::geography
    ) / 1000; -- Conversion en km
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Fonction : Trigger pour update timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Application du trigger sur les tables nécessaires
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_transactions_updated_at
    BEFORE UPDATE ON transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alerts_updated_at
    BEFORE UPDATE ON alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =========================================
-- ROW LEVEL SECURITY (RLS)
-- =========================================

-- Activation RLS sur les tables sensibles
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- Politique : Analyste peut voir toutes les transactions
CREATE POLICY analyst_read_all_transactions ON transactions
    FOR SELECT
    USING (auth.jwt() ->> 'role' = 'analyst');

-- Politique : Service client peut voir uniquement transactions du client contacté
CREATE POLICY support_read_user_transactions ON transactions
    FOR SELECT
    USING (
        auth.jwt() ->> 'role' = 'support' AND
        user_id = (auth.jwt() ->> 'user_id')::UUID
    );

-- Politique : Admin full access
CREATE POLICY admin_all_access ON transactions
    FOR ALL
    USING (auth.jwt() ->> 'role' = 'admin');

-- =========================================
-- DONNÉES DE TEST (optionnel pour dev)
-- =========================================

-- Insertion utilisateur test
INSERT INTO users (user_id, email, first_name, last_name, phone, country_code, risk_level, kyc_verified)
VALUES
    ('00000000-0000-0000-0000-000000000001', 'test.user1@digitalbank.fr', 'Jean', 'Dupont', '+33612345678', 'FR', 'LOW', TRUE),
    ('00000000-0000-0000-0000-000000000002', 'test.user2@digitalbank.fr', 'Marie', 'Martin', '+33698765432', 'FR', 'MEDIUM', TRUE);

-- Insertion transaction test légitime
INSERT INTO transactions (transaction_id, user_id, amount, merchant_name, merchant_category, merchant_country, fraud_score, risk_level, status)
VALUES
    (uuid_generate_v4(), '00000000-0000-0000-0000-000000000001', 45.30, 'Carrefour Paris', '5411', 'FR', 0.05, 'LOW', 'APPROVED');

-- Insertion transaction test suspecte
INSERT INTO transactions (transaction_id, user_id, amount, merchant_name, merchant_category, merchant_country, fraud_score, risk_level, status)
VALUES
    (uuid_generate_v4(), '00000000-0000-0000-0000-000000000001', 2850.00, 'Electronics Store Bangkok', '5732', 'TH', 0.92, 'CRITICAL', 'FLAGGED');

-- =========================================
-- VERIFICATION
-- =========================================

-- Lister toutes les tables
\dt

-- Compter les enregistrements
SELECT 'users' as table_name, COUNT(*) FROM users
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'alerts', COUNT(*) FROM alerts;

-- Afficher le schéma d'une table
\d transactions

COMMIT;
```

### ✅ Vérification de l'Installation

```bash
# Test connexion
psql "$DATABASE_URL" -c "SELECT version();"

# Vérifier les tables créées
psql "$DATABASE_URL" -c "\dt"

# Compter les utilisateurs de test
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM users;"
# Résultat attendu : 2

# Vérifier les extensions
psql "$DATABASE_URL" -c "SELECT * FROM pg_extension WHERE extname IN ('uuid-ossp', 'pgcrypto', 'postgis');"
```

### 🔄 Backups Automatiques

#### Configuration Backup Quotidien

```bash
# Créer script de backup
cat > /usr/local/bin/backup-supabase.sh <<'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/supabase"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/digitalbank_$DATE.sql.gz"

mkdir -p $BACKUP_DIR

# Backup avec compression
pg_dump "$DATABASE_URL" | gzip > $BACKUP_FILE

# Garder seulement les 30 derniers backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete

# Upload vers S3 (optionnel)
# aws s3 cp $BACKUP_FILE s3://digitalbank-backups/

echo "Backup completed: $BACKUP_FILE"
EOF

chmod +x /usr/local/bin/backup-supabase.sh

# Ajouter au crontab (tous les jours à 2h du matin)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-supabase.sh >> /var/log/supabase-backup.log 2>&1") | crontab -
```

---

## 4. Déploiement de l'API de Détection de Fraude {#api}

### 🐍 Préparation de l'Environnement Python

#### Structure du Projet API

```bash
cd ~/projects
git clone https://github.com/esic-paris/digitalbank-fraud-platform.git
cd digitalbank-fraud-platform/api
```

Si le repository n'existe pas encore, créez la structure :

```bash
mkdir -p api/{app/{models,routes,core,utils},tests}
cd api
```

#### Installation des Dépendances Python

```bash
# Créer environnement virtuel
python3.10 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Installation des dépendances
cat > requirements.txt <<EOF
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Machine Learning
scikit-learn==1.3.2
xgboost==2.0.2
numpy==1.26.2
pandas==2.1.3
joblib==1.3.2

# Database
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
asyncpg==0.29.0

# Monitoring & Logging
prometheus-client==0.19.0
python-json-logger==2.0.7

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
python-multipart==0.0.6

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
EOF

pip install -r requirements.txt
```

### 📝 Code de l'API

#### Fichier : `app/main.py` (Point d'Entrée)

```python
"""
DigitalBank Fraud Detection API
Main application entry point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import time
import logging

from app.routes import predict, health
from app.core.config import settings
from app.core.logging import setup_logging

# Configuration du logging
setup_logging()
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="DigitalBank Fraud Detection API",
    description="API de détection de fraude en temps réel",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour logging des requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms"
    )
    
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Routes
app.include_router(predict.router, prefix="/v1", tags=["Fraud Detection"])
app.include_router(health.router, prefix="/v1", tags=["Health"])

# Métriques Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Endpoint racine
@app.get("/")
async def root():
    return {
        "service": "DigitalBank Fraud Detection API",
        "version": "1.2.0",
        "status": "operational",
        "docs": "/docs"
    }

# Handler d'erreurs globales
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "request_id": request.headers.get("X-Request-ID", "unknown")
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
```

#### Fichier : `app/routes/predict.py` (Endpoint de Prédiction)

```python
"""
Fraud prediction endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import logging

from app.models.fraud_model import FraudModel
from app.models.schemas import TransactionInput, PredictionResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Instance du modèle (singleton)
fraud_model = FraudModel()

@router.post("/predict", response_model=PredictionResponse)
async def predict_fraud(transaction: TransactionInput):
    """
    Score une transaction et retourne la probabilité de fraude
    """
    try:
        # Prédiction
        result = fraud_model.predict(transaction.dict())
        
        # Log pour audit
        logger.info(
            f"Prediction for {transaction.transaction_id}: "
            f"score={result['fraud_score']:.4f}, "
            f"risk={result['risk_level']}"
        )
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

@router.post("/predict/batch")
async def predict_batch(
    transactions: List[TransactionInput],
    background_tasks: BackgroundTasks
):
    """
    Score un batch de transactions (async)
    """
    if len(transactions) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10000 transactions per batch"
        )
    
    batch_id = f"batch_{int(datetime.utcnow().timestamp())}"
    
    # Traitement asynchrone en background
    background_tasks.add_task(
        process_batch,
        batch_id,
        transactions
    )
    
    return {
        "batch_id": batch_id,
        "status": "QUEUED",
        "transactions_count": len(transactions)
    }

async def process_batch(batch_id: str, transactions: List[TransactionInput]):
    """
    Traitement batch en arrière-plan
    """
    results = []
    for txn in transactions:
        try:
            result = fraud_model.predict(txn.dict())
            results.append(result)
        except Exception as e:
            logger.error(f"Error processing {txn.transaction_id}: {e}")
    
    # Sauvegarder les résultats (DB ou S3)
    logger.info(f"Batch {batch_id} completed: {len(results)} predictions")
```

#### Fichier : `app/models/fraud_model.py` (Logique ML)

```python
"""
Fraud detection ML model wrapper
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FraudModel:
    def __init__(self):
        self.model = None
        self.model_version = "v2.3.1"
        self.load_model()
    
    def load_model(self):
        """Charge le modèle ML depuis le disque"""
        model_path = Path(__file__).parent.parent.parent / "ml/models/fraud_model_v2.pkl"
        
        if not model_path.exists():
            logger.warning(f"Model file not found: {model_path}. Using dummy model.")
            self.model = None
            return
        
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded successfully: {self.model_version}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None
    
    def preprocess(self, transaction: Dict[str, Any]) -> np.ndarray:
        """Feature engineering et preprocessing"""
        features = []
        
        # Feature 1: Amount
        features.append(transaction.get('amount', 0))
        
        # Feature 2: Merchant category risk score
        high_risk_categories = ['7995', '5732', '6211']  # Gaming, Electronics, Securities
        features.append(1 if transaction.get('merchant_category') in high_risk_categories else 0)
        
        # Feature 3: International transaction
        features.append(0 if transaction.get('merchant_country') == 'FR' else 1)
        
        # Feature 4: Card not present
        features.append(0 if transaction.get('card_present', False) else 1)
        
        # Feature 5: Transaction velocity (si disponible)
        velocity = transaction.get('additional_context', {}).get('transaction_velocity_1h', 0)
        features.append(velocity)
        
        # Feature 6-10: Autres features (à adapter selon votre modèle réel)
        # ...
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Prédiction de fraude"""
        
        # Si pas de modèle chargé, utiliser scoring basique (règles)
        if self.model is None:
            return self._rule_based_scoring(transaction)
        
        # Preprocessing
        X = self.preprocess(transaction)
        
        # Prédiction
        fraud_probability = float(self.model.predict_proba(X)[0][1])
        
        # Détermination du niveau de risque
        if fraud_probability < 0.3:
            risk_level = "LOW"
            recommendation = "APPROVE"
        elif fraud_probability < 0.6:
            risk_level = "MEDIUM"
            recommendation = "REVIEW"
        elif fraud_probability < 0.85:
            risk_level = "HIGH"
            recommendation = "CHALLENGE"
        else:
            risk_level = "CRITICAL"
            recommendation = "BLOCK"
        
        return {
            "transaction_id": transaction['transaction_id'],
            "fraud_score": round(fraud_probability, 4),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "model_version": self.model_version,
            "processing_time_ms": 65,  # À mesurer réellement
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _rule_based_scoring(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Scoring basique par règles (fallback si pas de modèle ML)"""
        score = 0.0
        
        # Règle 1: Montant élevé
        if transaction.get('amount', 0) > 1000:
            score += 0.3
        
        # Règle 2: Pays à risque
        if transaction.get('merchant_country') not in ['FR', 'BE', 'ES', 'IT', 'DE']:
            score += 0.2
        
        # Règle 3: Catégorie à risque
        if transaction.get('merchant_category') in ['7995', '5732']:
            score += 0.25
        
        # Règle 4: Vélocité
        velocity = transaction.get('additional_context', {}).get('transaction_velocity_1h', 0)
        if velocity > 5:
            score += 0.15
        
        # Règle 5: Device inconnu
        if not transaction.get('device_id'):
            score += 0.1
        
        score = min(score, 1.0)
        
        if score < 0.3:
            risk_level, recommendation = "LOW", "APPROVE"
        elif score < 0.6:
            risk_level, recommendation = "MEDIUM", "REVIEW"
        elif score < 0.85:
            risk_level, recommendation = "HIGH", "CHALLENGE"
        else:
            risk_level, recommendation = "CRITICAL", "BLOCK"
        
        return {
            "transaction_id": transaction['transaction_id'],
            "fraud_score": round(score, 4),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "model_version": "rule-based",
            "processing_time_ms": 10,
            "timestamp": datetime.utcnow().isoformat()
        }
```

#### Fichier : `.env` (Configuration)

```bash
# Application
APP_NAME=DigitalBank Fraud API
DEBUG=False
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Security
SECRET_KEY=your-secret-key-min-32-chars-CHANGE-ME
CORS_ORIGINS=["http://localhost:3000", "https://digitalbank.fr"]

# ML Model
MODEL_PATH=ml/models/fraud_model_v2.pkl
MODEL_VERSION=v2.3.1

# Monitoring
ENABLE_METRICS=True
```

⚠️ **NE JAMAIS commiter ce fichier dans Git. Ajouter `.env` au `.gitignore`.**

### 🐳 Dockerisation de l'API

#### Fichier : `Dockerfile`

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY ./app ./app
COPY ./ml ./ml

# Création utilisateur non-root (sécurité)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposition du port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/v1/health')"

# Lancement de l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Construction et Lancement

```bash
# Build de l'image Docker
docker build -t digitalbank-fraud-api:latest .

# Test en local
docker run -d \
    --name fraud-api \
    -p 8000:8000 \
    --env-file .env \
    digitalbank-fraud-api:latest

# Vérification
curl http://localhost:8000/v1/health
```

### ✅ Tests de l'API

```bash
# Test endpoint health
curl http://localhost:8000/v1/health

# Test prédiction
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "test_001",
    "user_id": "user_123",
    "amount": 45.30,
    "merchant_category": "5411",
    "merchant_country": "FR",
    "timestamp": "2026-01-22T14:30:00Z",
    "card_present": true
  }'

# Résultat attendu :
# {
#   "transaction_id": "test_001",
#   "fraud_score": 0.05,
#   "risk_level": "LOW",
#   "recommendation": "APPROVE",
#   ...
# }
```

---

**(Suite du document dans le prochain message en raison de la limite de longueur...)**

Voulez-vous que je continue avec :
- 📊 Configuration Metabase
- 🔄 Workflows Make.com
- 📈 Monitoring Prometheus/Grafana
- 🔧 Dépannage

Ou préférez-vous que je génère directement les fichiers PDF/Word finaux de ces 4 documents ?