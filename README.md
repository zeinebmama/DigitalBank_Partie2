# DigitalBank_Partie2
Projet DigitalBank - Plateforme low-code ESIC/CPDIA
Plateforme de Monitoring, Sécurité et Automatisation – DigitalBank France
📌 Présentation générale

Ce dossier contient l’ensemble des livrables du projet de groupe – Partie 2, réalisé dans le cadre du module Systèmes d’Information, Sécurité et Data.

L’objectif du projet est de concevoir une plateforme complète intégrant :

la visualisation des données,

la détection de fraude,

l’automatisation des alertes,

le monitoring de l’infrastructure,

et la sécurisation des accès.

📂 Index des dossiers et fichiers
📁 1_Specifications/

Contient les documents de cadrage fonctionnel du projet.

Document_Specifications.pdf
→ Description des besoins fonctionnels et non fonctionnels, périmètre du projet.

User_Stories.xlsx
→ Liste des user stories organisées par profils utilisateurs.

📁 2_Architecture/

Contient les documents d’architecture technique et de conception.

Schema_Architecture_Technique.png / .pdf
→ Schéma global de l’architecture du système.

Modele_Donnees_ERD.png
→ Modèle conceptuel et logique des données (ERD).

Document_Conception_Technique.pdf
→ Détails techniques de la solution (composants, flux, sécurité).

Justification_Choix_Technologiques.pdf
→ Justification des outils et technologies utilisés.

📁 3_Code_Source/

Contient l’ensemble du code et des configurations techniques.

README.md
→ Instructions générales liées au code source.

🔹 supabase_config/ (ou hasura_config/)

schema.sql → Schéma de la base de données.

policies.sql → Règles de sécurité (RBAC, Row Level Security).

config_files/ → Fichiers de configuration.

🔹 fraud_detection_api/

app.py → API Python de détection de fraude.

requirements.txt → Dépendances Python.

fraud_model.pkl → Modèle Machine Learning entraîné.

Dockerfile (optionnel) → Conteneurisation de l’API.

🔹 dashboards/

metabase_exports/ ou retool_exports/ → Exports des dashboards.

grafana_dashboards/ → Dashboards de monitoring.

screenshots/ → Captures d’écran des dashboards.

🔹 workflows/

n8n_workflows.json ou make_scenarios/ → Automatisations.

screenshots/ → Captures des workflows.

🔹 monitoring/

docker-compose.yml → Stack ELK ou Prometheus + Grafana.

config_files/ → Fichiers de configuration.

📁 4_Documentation/

Contient la documentation complète du projet.

README_Principal.md
→ Présentation générale et synthèse du projet.

Documentation_API.pdf / swagger.yaml
→ Documentation technique de l’API de détection de fraude.

Manuel_Utilisateur.pdf
→ Guide d’utilisation des dashboards et fonctionnalités.

Guide_Installation_Deploiement.pdf
→ Instructions d’installation et de déploiement.

📁 5_Securite/

Contient les éléments liés à la sécurité du système.

Documentation_Roles_Permissions.pdf
→ Gestion des rôles et des droits.

Audit_Logs_Trigger.sql
→ Triggers SQL pour la journalisation des actions.

Rapport_Tests_Securite.pdf
→ Résultats des tests de sécurité.

screenshots/
→ Preuves visuelles.

📁 6_Tests/

Contient les tests fonctionnels et de sécurité.

Postman_Collection.json
→ Tests automatisés de l’API.

Resultats_Tests_Securite.pdf
→ Synthèse des résultats de tests.

screenshots/
→ Captures d’exécution.

📁 7_Gestion_Projet/

Contient les éléments de gestion de projet.

Tableau_Repartition_Contributions.xlsx
→ Répartition des tâches par membre du groupe.

Planning_Projet_Gantt.pdf / .xlsx
→ Planning du projet.

Comptes_Rendus_Reunions.pdf
→ Comptes rendus des réunions.

Declaration_Integrite.pdf
→ Déclaration d’intégrité signée.

📁 8_Presentation/

Contient les supports de soutenance.

Video_Demonstration.mp4 / lien YouTube
→ Vidéo de démonstration du projet.

Slides_Presentation.pdf
→ Slides de soutenance.

Scripts_Demo/ (optionnel)
→ Scripts utilisés lors de la démonstration.

✅ Fin du document

Ce fichier sert de point d’entrée principal pour comprendre l’organisation et le contenu du projet.
