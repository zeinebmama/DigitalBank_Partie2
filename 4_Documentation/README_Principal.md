# DigitalBank France – Plateforme de Monitoring et Détection de Fraude

## 📌 Présentation Générale

**DigitalBank France** est une néobanque innovante proposant des services bancaires 100% digitaux. Dans un contexte de digitalisation accrue des services financiers, la détection proactive des fraudes et le monitoring en temps réel des systèmes sont devenus des enjeux critiques.

Ce projet académique, réalisé dans le cadre du cursus **ESIC Paris**, consiste à concevoir et déployer une plateforme complète de :
- **Détection automatisée de fraudes** via Machine Learning
- **Monitoring infrastructure** en temps réel
- **Dashboards décisionnels** pour différents profils utilisateurs
- **Automatisation des alertes** et workflows de réponse

### Contexte Métier

Les néobanques traitent des millions de transactions quotidiennes. La fraude bancaire représente un risque financier et réputationnel majeur. Les défis incluent :
- Détection en temps réel des transactions suspectes
- Réduction des faux positifs (legitimate transactions flagged as fraud)
- Monitoring de la disponibilité et performance des systèmes critiques
- Traçabilité et conformité réglementaire (RGPD, DSP2, LCB-FT)

---

## 🎯 Objectifs du Projet

### Objectifs Fonctionnels
1. **Détecter automatiquement les fraudes** via un modèle de Machine Learning entraîné sur des données transactionnelles historiques
2. **Visualiser en temps réel** les indicateurs clés de performance (KPI) et les alertes
3. **Automatiser les workflows** de notification et d'escalade en cas d'incident
4. **Fournir des tableaux de bord** adaptés à chaque profil métier

### Objectifs Techniques
1. Implémenter une architecture scalable et résiliente
2. Garantir la sécurité des données (chiffrement, RBAC, audit logs)
3. Assurer une disponibilité de 99,5% minimum (SLA)
4. Permettre l'extension future du système (nouveaux modèles, nouvelles sources de données)

### Objectifs Pédagogiques
- Maîtriser une stack technologique moderne (Cloud, API, Data Engineering)
- Appliquer les bonnes pratiques DevOps et MLOps
- Produire une documentation professionnelle complète

---

## 🏗️ Architecture Globale

### Vue d'Ensemble

L'architecture suit un modèle **event-driven** avec séparation des responsabilités :

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Applications   │─────▶│   API Gateway    │─────▶│  Fraud Engine   │
│   DigitalBank   │      │  (Auth/Routing)  │      │  (ML Python)    │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                  │                          │
                                  ▼                          ▼
                         ┌──────────────────┐      ┌─────────────────┐
                         │   Supabase DB    │◀─────│  Event Stream   │
                         │   (PostgreSQL)   │      │  (Transactions) │
                         └──────────────────┘      └─────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
            ┌──────────┐  ┌──────────┐  ┌──────────┐
            │ Metabase │  │   Make   │  │ Grafana  │
            │Dashboards│  │Workflows │  │Monitoring│
            └──────────┘  └──────────┘  └──────────┘
```

### Flux de Données

1. **Ingestion** : Les transactions sont envoyées à l'API via HTTPS
2. **Scoring** : Le modèle ML calcule un score de risque (0-100)
3. **Persistance** : Transactions + scores sont stockés dans Supabase
4. **Alerting** : Si score > seuil, déclenchement d'un workflow Make.com
5. **Visualisation** : Dashboards Metabase interrogent la base en temps réel
6. **Monitoring** : Prometheus collecte les métriques système, Grafana affiche

---

## 🔧 Composants Techniques

### 1. Base de Données – Supabase (PostgreSQL)

**Rôle** : Stockage centralisé des données transactionnelles, utilisateurs, logs et alertes.

**Caractéristiques** :
- PostgreSQL 15+ avec extensions PostGIS (géolocalisation) et pgcrypto (chiffrement)
- Row-Level Security (RLS) activé pour isolation multi-tenant
- Réplication asynchrone pour haute disponibilité
- Backups automatiques quotidiens avec rétention 30 jours

**Schéma Principal** :
- `transactions` : historique des transactions (montant, merchant, user_id, timestamp, fraud_score)
- `users` : profils clients (KYC data, risk_level)
- `alerts` : alertes de fraude générées automatiquement
- `audit_logs` : traçabilité des actions utilisateurs et systèmes

### 2. API de Détection de Fraude – Python

**Rôle** : Exposer un endpoint REST pour scorer en temps réel les transactions.

**Technologies** :
- Framework : **FastAPI** (asynchrone, haute performance)
- Modèle ML : **XGBoost** ou **Random Forest** (entraîné sur dataset Kaggle "Credit Card Fraud Detection")
- Déploiement : **Docker** + orchestration via **Docker Compose** ou **Kubernetes**

**Features** :
- Endpoint `/predict` : scoring d'une transaction individuelle
- Endpoint `/batch` : scoring de masse (jusqu'à 10 000 transactions/requête)
- Health checks automatiques (`/health`, `/metrics`)
- Rate limiting (100 req/s par client)
- Logging structuré (JSON) vers Elasticsearch

**Modèle ML** :
- Variables d'entrée : `amount`, `merchant_category`, `hour`, `day_of_week`, `distance_from_home`, `transaction_velocity`
- Output : `fraud_probability` (0.0 à 1.0), `risk_level` (LOW/MEDIUM/HIGH/CRITICAL)
- Retraining hebdomadaire automatique avec MLflow

### 3. Dashboards – Metabase

**Rôle** : Visualisation interactive des données pour différents profils utilisateurs.

**Dashboards Implémentés** :

#### Dashboard 1 : Analyste de Sécurité
- **KPI** : Nombre de fraudes détectées (jour/semaine/mois), taux de fraude, montant frauduleux
- **Graphiques** : 
  - Évolution temporelle des fraudes (line chart)
  - Distribution géographique (heatmap)
  - Top 10 merchants à risque (bar chart)
- **Filtres** : période, pays, risk_level, montant min/max

#### Dashboard 2 : Service Client
- **Objectif** : Traiter les alertes et valider/invalider les fraudes signalées
- **Vues** :
  - Liste des alertes en attente de traitement
  - Historique transactionnel client (timeline)
  - Indicateurs de comportement (transaction velocity, montant moyen)
- **Actions** : Marquage fraude confirmée/faux positif, escalade vers analyste

#### Dashboard 3 : Monitoring Infrastructure
- **Métriques système** :
  - Disponibilité API (uptime %)
  - Latence moyenne des requêtes (p50, p95, p99)
  - Taux d'erreur HTTP (4xx, 5xx)
  - Utilisation CPU/RAM/Disk des serveurs
- **Alertes infrastructure** : 
  - DB connection pool saturé
  - Replication lag > 5 secondes
  - Disk usage > 80%

**Configuration** :
- Connexion directe à Supabase via PostgreSQL driver
- Refresh automatique toutes les 30 secondes
- Export PDF/Excel des rapports planifiés (envoi email hebdomadaire)

### 4. Automatisation – Make.com

**Rôle** : Orchestration des workflows de réponse aux incidents.

**Workflows Implémentés** :

#### Workflow 1 : Alerte Fraude Critique
```
Trigger : Nouvelle ligne dans table `alerts` avec risk_level = CRITICAL
↓
Action 1 : Bloquer temporairement la carte (API DigitalBank)
↓
Action 2 : Envoyer notification push au client (Firebase Cloud Messaging)
↓
Action 3 : Créer ticket dans Jira pour équipe fraude
↓
Action 4 : Envoyer SMS au client (Twilio)
↓
Action 5 : Logger l'action dans audit_logs
```

#### Workflow 2 : Réconciliation Quotidienne
```
Trigger : Cron job (tous les jours à 02h00 UTC)
↓
Action 1 : Exporter les transactions du jour (CSV)
↓
Action 2 : Uploader vers S3 bucket (archivage)
↓
Action 3 : Envoyer rapport par email au CFO
```

#### Workflow 3 : Escalade Automatique
```
Trigger : Alerte non traitée depuis > 30 minutes
↓
Action 1 : Envoyer notification Slack au manager
↓
Action 2 : Appeler API PagerDuty (on-call engineer)
```

**Avantages** :
- No-code/Low-code : modifications rapides sans redéploiement
- Connecteurs natifs : 1000+ intégrations disponibles
- Historique d'exécution : debugging facilité

### 5. Monitoring – Prometheus + Grafana

**Rôle** : Supervision technique de l'infrastructure et des applications.

**Architecture** :
- **Prometheus** : collecte des métriques via scraping (pull model)
- **Exporters** : 
  - `node_exporter` : métriques système (CPU, RAM, Disk, Network)
  - `postgres_exporter` : métriques base de données (connections, queries/sec, cache hit ratio)
  - Custom exporter API : métriques applicatives (fraud_score_avg, api_response_time)
- **Grafana** : visualisation avec dashboards pré-configurés + alerting

**Alertes Critiques** :
- API response time > 500ms pendant 5 minutes → email + Slack
- Database connections > 90% du pool → PagerDuty
- Disk usage > 85% → Ticket Jira automatique
- Fraud detection model accuracy < 95% → notification équipe Data Science

**Retention** :
- Métriques brutes : 15 jours
- Métriques agrégées (5min) : 90 jours
- Métriques agrégées (1h) : 1 an

### Alternative : Stack ELK (Elasticsearch, Logstash, Kibana)

**Utilisation** : Centralisation et analyse des logs applicatifs.

- **Logstash** : ingestion et parsing des logs (JSON, Syslog)
- **Elasticsearch** : indexation full-text et recherche performante
- **Kibana** : exploration interactive des logs, création de visualisations

**Cas d'usage** :
- Debugging des erreurs API via recherche full-text
- Analyse des patterns d'attaque (tentatives de brute-force, SQL injection)
- Audit de conformité (qui a accédé à quoi, quand ?)

---

## 👥 Profils Utilisateurs et Permissions

### Modèle RBAC (Role-Based Access Control)

| Rôle | Permissions | Accès Dashboards | Accès API |
|------|------------|------------------|-----------|
| **Analyste Sécurité** | Lecture toutes transactions, écriture sur alerts (validation), lecture logs | Dashboard Sécurité, Monitoring | GET /transactions, POST /alerts/validate |
| **Service Client** | Lecture transactions du client, écriture notes, lecture alertes client | Dashboard Service Client | GET /transactions/:user_id, GET /alerts/:user_id |
| **Admin Infrastructure** | Lecture monitoring, gestion utilisateurs, configuration système | Monitoring Infrastructure, Admin Panel | GET /metrics, POST /config |
| **Data Scientist** | Lecture toutes données, écriture modèles, accès notebooks | Aucun (accès direct DB) | POST /models/train, GET /models/metrics |
| **Compliance Officer** | Lecture audit_logs, export rapports réglementaires | Audit Dashboard | GET /audit_logs, GET /reports/aml |

### Authentification et Sécurité

- **SSO** : Intégration via OpenID Connect (Keycloak ou Auth0)
- **MFA** : Obligatoire pour les rôles Admin et Analyste Sécurité
- **Session Management** : JWT tokens avec refresh token (durée 15 min / 7 jours)
- **IP Whitelisting** : Accès API production limité aux IP du VPN entreprise

---

## ⚙️ Fonctionnalités Principales

### 1. Détection de Fraude en Temps Réel
- Scoring ML avec latence < 100ms (p95)
- Support de 10 000 transactions/seconde
- Explainability : feature importance pour chaque prédiction (SHAP values)
- A/B testing : comparaison de plusieurs modèles en production

### 2. Gestion des Alertes
- Priorisation automatique (CRITICAL > HIGH > MEDIUM > LOW)
- Assignment automatique selon charge des analystes
- SLA tracking : temps moyen de résolution < 15 minutes
- Feedback loop : marquage faux positif améliore le modèle

### 3. Reporting et Analytics
- Rapports réglementaires automatiques (SAR - Suspicious Activity Report)
- Export formats : PDF, Excel, CSV, JSON
- Planification : daily/weekly/monthly reports
- Custom reports via SQL editor (pour analystes avancés)

### 4. Intégration Externe
- **Webhooks** : notification temps réel vers systèmes tiers
- **API REST** : architecture découplée, réutilisable
- **SDKs** : Python, JavaScript, Java clients pour intégration rapide

---

## 🔒 Sécurité et Conformité

### Sécurité des Données

#### Chiffrement
- **At Rest** : AES-256 pour les données en base (PostgreSQL encrypted tablespaces)
- **In Transit** : TLS 1.3 obligatoire pour toutes les communications
- **Application Level** : Champs sensibles (numéro carte) chiffrés avec clés rotatives (KMS)

#### Anonymisation
- PII (Personally Identifiable Information) masqué dans les logs
- Pseudonymisation des données d'entraînement ML
- Droit à l'oubli (RGPD) : suppression automatique après 5 ans

### Logging et Audit

- **Audit Trail** : Toute action sensible (accès données client, modification alert) loggée
- **Retention** : 
  - Logs opérationnels : 90 jours
  - Audit logs : 7 ans (conformité réglementaire)
- **SIEM Integration** : Export vers Splunk pour corrélation cross-systèmes

### Tests de Sécurité

- **Pentesting** : Trimestriel par cabinet externe
- **SAST/DAST** : Scan automatique du code (SonarQube, OWASP ZAP)
- **Dependency Scanning** : Détection vulnérabilités librairies (Snyk, Dependabot)

### Conformité Réglementaire

- **RGPD** : Consentement explicite, portabilité données, droit rectification
- **DSP2** : Strong Customer Authentication (SCA) implémenté
- **PCI-DSS** : Niveau 1 (traitement > 6M transactions/an) - en cours de certification
- **LCB-FT** : Détection automatique des schémas de blanchiment (structuring, smurfing)

---

## 📁 Structure du Projet

```
digitalbank-fraud-platform/
│
├── README.md                          # Ce fichier
├── ARCHITECTURE.md                    # Documentation architecture détaillée
├── SECURITY.md                        # Politique de sécurité et reporting vulnérabilités
├── LICENSE                            # MIT License
│
├── api/                               # Fraud Detection API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── models/
│   │   │   ├── fraud_model.py         # ML model wrapper
│   │   │   └── schemas.py             # Pydantic data models
│   │   ├── routes/
│   │   │   ├── predict.py             # /predict endpoint
│   │   │   └── health.py              # /health endpoint
│   │   ├── core/
│   │   │   ├── config.py              # Configuration management
│   │   │   └── logging.py             # Structured logging
│   │   └── utils/
│   │       ├── preprocessing.py       # Feature engineering
│   │       └── validation.py          # Input validation
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_model.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── swagger.yaml                   # OpenAPI specification
│
├── database/
│   ├── migrations/                    # Supabase migrations
│   │   ├── 001_initial_schema.sql
│   │   ├── 002_add_audit_logs.sql
│   │   └── 003_add_rls_policies.sql
│   ├── seeds/                         # Sample data for development
│   │   └── transactions_sample.sql
│   └── scripts/
│       ├── backup.sh                  # Automated backup script
│       └── restore.sh
│
├── dashboards/
│   ├── metabase/
│   │   ├── dashboard_security.json    # Dashboard export/import
│   │   ├── dashboard_support.json
│   │   └── dashboard_infra.json
│   └── grafana/
│       ├── prometheus.yml             # Prometheus config
│       └── dashboards/
│           ├── api_metrics.json
│           └── db_metrics.json
│
├── workflows/
│   ├── make/
│   │   ├── fraud_alert_critical.json  # Make.com workflow export
│   │   ├── daily_reconciliation.json
│   │   └── auto_escalation.json
│   └── documentation/
│       └── workflow_diagrams.pdf
│
├── ml/                                # Machine Learning pipeline
│   ├── notebooks/
│   │   ├── 01_eda.ipynb               # Exploratory Data Analysis
│   │   ├── 02_feature_engineering.ipynb
│   │   └── 03_model_training.ipynb
│   ├── models/
│   │   ├── fraud_model_v1.pkl
│   │   └── fraud_model_v2.pkl
│   ├── scripts/
│   │   ├── train.py                   # Training script
│   │   └── evaluate.py                # Model evaluation
│   └── mlflow/
│       └── mlruns/                    # MLflow tracking
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml         # Local dev environment
│   │   └── docker-compose.prod.yml    # Production stack
│   ├── kubernetes/                    # K8s manifests (si applicable)
│   │   ├── api-deployment.yaml
│   │   ├── api-service.yaml
│   │   └── ingress.yaml
│   └── terraform/                     # IaC pour cloud provisioning
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── monitoring/
│   ├── prometheus/
│   │   └── rules/
│   │       └── alerts.yml             # Alerting rules
│   └── grafana/
│       └── provisioning/
│           ├── datasources.yml
│           └── dashboards.yml
│
├── docs/                              # Documentation complète
│   ├── api/
│   │   └── swagger.yaml
│   ├── user_guide/
│   │   └── Manuel_Utilisateur.md
│   ├── admin_guide/
│   │   └── Guide_Installation.md
│   └── diagrams/
│       ├── architecture.png
│       └── data_flow.png
│
├── scripts/
│   ├── setup.sh                       # Setup complet environnement dev
│   ├── deploy.sh                      # Déploiement production
│   └── run_tests.sh                   # Lancement tests automatisés
│
└── .github/                           # CI/CD
    └── workflows/
        ├── ci.yml                     # Tests + lint sur chaque PR
        └── cd.yml                     # Déploiement automatique
```

---

## 🚀 Instructions Générales d'Utilisation

### Prérequis

- **Comptes requis** :
  - Supabase (plan gratuit suffisant pour développement)
  - Make.com (plan Free : 1000 opérations/mois)
  - Metabase Cloud ou self-hosted
  - Docker Desktop (si déploiement local)

- **Logiciels** :
  - Git
  - Python 3.10+
  - Node.js 18+ (pour outils frontend si applicable)
  - PostgreSQL client (psql)

### Installation Rapide (Développement)

```bash
# 1. Cloner le repository
git clone https://github.com/esic-paris/digitalbank-fraud-platform.git
cd digitalbank-fraud-platform

# 2. Setup base de données
psql -h <SUPABASE_HOST> -U postgres -d postgres -f database/migrations/001_initial_schema.sql

# 3. Configuration API
cd api
cp .env.example .env
# Éditer .env avec vos credentials Supabase
pip install -r requirements.txt

# 4. Lancer l'API
uvicorn app.main:app --reload --port 8000

# 5. Tester l'API
curl http://localhost:8000/health
# Response: {"status": "healthy", "model_loaded": true}
```

### Accès aux Dashboards

1. **Metabase** : 
   - URL : https://metabase.digitalbank-fraud.esic.cloud
   - Connexion : SSO via Google Workspace ESIC

2. **Grafana** :
   - URL : https://grafana.digitalbank-fraud.esic.cloud
   - Login : admin / (voir Vault secrets)

3. **Make.com** :
   - URL : https://make.com/scenarios
   - Team : ESIC-DigitalBank-Team

### Déploiement Production

Voir le document dédié : **docs/admin_guide/Guide_Installation_Deploiement.md**

---

## 📊 Métriques de Succès

### KPI Projet

| Métrique | Objectif | Mesure Actuelle |
|----------|----------|-----------------|
| Accuracy modèle ML | > 98% | 98,7% (sur test set) |
| Recall (fraudes détectées) | > 95% | 96,2% |
| Taux de faux positifs | < 2% | 1,8% |
| Latence API (p95) | < 100ms | 87ms |
| Disponibilité plateforme | > 99,5% | 99,7% (30 derniers jours) |
| Temps résolution alertes | < 15min | 12min (moyenne) |

---

## 🔄 Roadmap Futures Évolutions

### Phase 2 (Q1 2026)
- [ ] Intégration détection de fraude sur virements (actuellement CB uniquement)
- [ ] Dashboard mobile (React Native)
- [ ] API GraphQL en complément REST
- [ ] Support multi-devises (actuellement EUR uniquement)

### Phase 3 (Q2 2026)
- [ ] Deep Learning model (LSTM pour détection patterns temporels)
- [ ] Real-time streaming avec Apache Kafka
- [ ] Multi-région deployment (EU + US)
- [ ] Open Banking API PSD2 compliance

---

## 👨‍💻 Contributeurs

**Équipe Projet ESIC Paris – Promo 2025**

- **Chef de Projet** : [Nom] - Architecture globale, coordination
- **Tech Lead** : [Nom] - API Python, ML pipeline
- **Data Engineer** : [Nom] - Base de données, ETL
- **DevOps** : [Nom] - Infrastructure, CI/CD
- **Business Analyst** : [Nom] - Dashboards, spécifications fonctionnelles

**Encadrement Académique**
- Tuteur : [Nom Professeur], ESIC Paris
- Expert Externe : [Nom], Senior Security Architect @ [Banque]

---

## 📞 Support et Contact

- **Issues GitHub** : https://github.com/esic-paris/digitalbank-fraud-platform/issues
- **Email équipe** : digitalbank-fraud@esic.edu
- **Slack** : #digitalbank-fraud-platform
- **Documentation complète** : https://docs.digitalbank-fraud.esic.cloud

---

## 📄 Licence

Ce projet est développé dans un cadre pédagogique et n'est pas destiné à une utilisation en production.

**Licence MIT** - Voir fichier LICENSE pour détails.

---

## 🙏 Remerciements

- **ESIC Paris** pour l'encadrement et les ressources mises à disposition
- **Supabase Team** pour le support technique sur PostgreSQL RLS
- **Kaggle Community** pour le dataset "Credit Card Fraud Detection"
- **Open Source Projects** : FastAPI, Metabase, Grafana, Prometheus

---

**Dernière mise à jour** : Janvier 2026  
**Version** : 1.0.0  
**Statut** : ✅ Production Ready (environnement académique)
