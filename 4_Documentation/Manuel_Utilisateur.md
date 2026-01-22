# Manuel Utilisateur – Plateforme DigitalBank Fraud Detection

**Version** : 1.0  
**Date** : Janvier 2026  
**Public cible** : Utilisateurs non techniques (Analystes, Service Client, Managers)

---

## 📖 Table des Matières

1. [Introduction](#introduction)
2. [Premiers Pas](#premiers-pas)
3. [Dashboard Analyste de Sécurité](#dashboard-analyste-de-sécurité)
4. [Dashboard Service Client](#dashboard-service-client)
5. [Dashboard Monitoring Infrastructure](#dashboard-monitoring-infrastructure)
6. [Filtres et Recherches](#filtres-et-recherches)
7. [Gestion des Alertes](#gestion-des-alertes)
8. [Bonnes Pratiques](#bonnes-pratiques)
9. [FAQ](#faq)

---

## 1. Introduction {#introduction}

### 🎯 Objectif de la Plateforme

La plateforme **DigitalBank Fraud Detection** vous permet de :
- **Détecter les fraudes** en temps réel grâce à l'intelligence artificielle
- **Visualiser les indicateurs clés** via des tableaux de bord interactifs
- **Traiter les alertes** rapidement pour protéger nos clients
- **Monitorer la santé** de nos systèmes informatiques

### 👥 Qui Utilise Quoi ?

| Profil | Dashboard Principal | Objectif |
|--------|---------------------|----------|
| **Analyste de Sécurité** | Dashboard Sécurité | Identifier et analyser les fraudes |
| **Conseiller Client** | Dashboard Service Client | Traiter les alertes clients et historique |
| **Manager Infrastructure** | Dashboard Monitoring | Superviser la disponibilité des systèmes |

### 🔐 Sécurité et Confidentialité

⚠️ **Important** :
- Ne partagez jamais vos identifiants de connexion
- Déconnectez-vous toujours après utilisation (surtout sur poste partagé)
- Les données affichées sont **confidentielles** : ne les communiquez pas en dehors de l'équipe
- Toute action est tracée pour audit (conformité RGPD)

---

## 2. Premiers Pas {#premiers-pas}

### 🔑 Connexion à la Plateforme

#### Étape 1 : Accéder à l'URL
- Ouvrez votre navigateur (Chrome, Firefox, Safari recommandés)
- URL : **https://metabase.digitalbank-fraud.esic.cloud**

#### Étape 2 : Authentification
- Cliquez sur **"Se connecter avec Google"**
- Utilisez votre compte **@esic.edu** ou **@digitalbank.fr**
- Si demandé, validez la double authentification (code SMS ou app Authenticator)

#### Étape 3 : Vérification
✅ Après connexion, vous devez voir :
- Votre nom en haut à droite
- La liste des dashboards auxquels vous avez accès
- Un bandeau vert indiquant "Connecté"

#### 🚨 Problème de Connexion ?
- **Erreur "Accès refusé"** → Contactez votre manager pour vérification des permissions
- **Erreur "Email non reconnu"** → Vérifiez que vous utilisez bien votre email professionnel
- **Page blanche** → Videz le cache du navigateur (Ctrl+F5)

### 📱 Interface Générale

L'interface se compose de 4 zones principales :

```
┌─────────────────────────────────────────────────────┐
│  [Logo] DigitalBank Fraud Detection    👤 Mon Compte│ ← Barre de navigation
├─────────────────────────────────────────────────────┤
│ 📊 Dashboards  |  🔔 Alertes (3)  |  ⚙️ Paramètres │ ← Menu principal
├─────────────────────────────────────────────────────┤
│                                                     │
│            [Contenu du Dashboard]                   │ ← Zone de visualisation
│                                                     │
├─────────────────────────────────────────────────────┤
│  🔄 Dernière mise à jour : il y a 30s              │ ← Barre de statut
└─────────────────────────────────────────────────────┘
```

### 🔔 Notifications

En haut à droite, l'icône 🔔 affiche le nombre d'alertes nécessitant votre attention :
- **Chiffre vert** (1-5) : Alertes de routine
- **Chiffre orange** (6-20) : Activité inhabituelle
- **Chiffre rouge** (>20) : Pic d'activité frauduleuse, prioriser le traitement

---

## 3. Dashboard Analyste de Sécurité {#dashboard-analyste-de-sécurité}

**Public** : Équipe Fraude et Sécurité  
**Objectif** : Vision globale des fraudes détectées et analyse approfondie

### 📊 Vue d'Ensemble

Le dashboard est organisé en 4 sections :

#### Section 1 : KPI Principaux (en haut)

```
┌────────────────┬────────────────┬────────────────┬────────────────┐
│ 🔴 Fraudes      │ 💰 Montant      │ 📈 Taux         │ ⏱️ Temps Moyen  │
│   Détectées     │   Bloqué        │   de Fraude     │   Résolution    │
│                │                │                │                │
│     247        │   182 450 €     │    0.34%       │   12 min       │
│   ↑ +12%      │  ↑ +8 350 €    │   ↓ -0.02%    │   ↓ -2 min     │
└────────────────┴────────────────┴────────────────┴────────────────┘
```

**Interprétation** :
- **Flèche verte ↓** : amélioration (ex: temps de résolution qui baisse)
- **Flèche rouge ↑** : dégradation (ex: nombre de fraudes qui augmente)
- Les pourcentages indiquent l'évolution par rapport à la période précédente

#### Section 2 : Graphique Temporel

**Graphique en ligne** : Évolution des fraudes sur 30 jours

**Utilisation** :
- **Pics visibles** → Identifier les périodes à risque (ex: Black Friday, fin de mois)
- **Tendance générale** → Évaluer l'efficacité du modèle de détection
- **Clic sur un point** → Accéder aux détails de cette journée

**Exemple d'Analyse** :
> "Le 15 janvier, on observe un pic à 89 fraudes. En creusant, on découvre une campagne de phishing ciblant nos clients. Action : alerte généralisée + renforcement authentification."

#### Section 3 : Répartition Géographique

**Carte thermique** : Intensité des fraudes par pays

**Codes couleur** :
- 🟢 **Vert** : < 5 fraudes/jour (risque faible)
- 🟡 **Jaune** : 5-20 fraudes/jour (surveillance)
- 🟠 **Orange** : 20-50 fraudes/jour (risque élevé)
- 🔴 **Rouge** : > 50 fraudes/jour (risque critique)

**Actions Possibles** :
- **Clic sur un pays** → Liste des transactions suspectes dans ce pays
- **Hover (survol)** → Affichage du nombre exact de fraudes
- **Export** → Télécharger les données au format Excel pour rapport

#### Section 4 : Top Merchants à Risque

**Tableau** : 10 commerçants avec le plus de fraudes

| Rang | Commerçant | Catégorie | Pays | Fraudes | Montant |
|------|-----------|-----------|------|---------|---------|
| 1 | ElectronicsWorld.com | Électronique | CY | 34 | 45 678 € |
| 2 | CryptoGaming Ltd | Jeux en ligne | MT | 28 | 38 921 € |
| ... | ... | ... | ... | ... | ... |

**Utilisation** :
- **Merchant suspect récurrent** → Envisager blocage préventif ou authentification renforcée
- **Catégorie à risque** → Ajuster les seuils de détection pour cette catégorie
- **Export vers Jira** → Créer un ticket d'investigation

### 🔍 Analyse d'une Transaction Suspecte

#### Étape 1 : Accéder aux Détails
- Dans la section "Alertes Récentes" (en bas du dashboard)
- Cliquer sur la ligne de la transaction

#### Étape 2 : Panneau de Détails

```
┌─────────────────────────────────────────────────────┐
│  Transaction ID : txn_2026012219456ghi              │
│  Date : 22/01/2026 18:20 UTC                        │
│  Montant : 999,99 €                                 │
│  Merchant : Online Gaming CRYPTO (Chypre)           │
│  Client : usr_54321 (Jean Dupont)                   │
│                                                     │
│  🎯 Score de Fraude : 92% (CRITIQUE)                │
│                                                     │
│  📌 Raisons Principales :                           │
│   1. Catégorie à haut risque (jeux/crypto)  +35%   │
│   2. Device non reconnu                      +28%   │
│   3. IP suspecte (nœud TOR)                  +18%   │
│   4. Vélocité : 8 transactions en 1h         +11%   │
│                                                     │
│  📊 Historique Client :                             │
│   - Compte créé : 18/07/2023                        │
│   - Dernière transaction : 15/07/2025 (6 mois)     │
│   - Montant moyen : 45 €                            │
│   - Aucune fraude antérieure                        │
│                                                     │
│  [✅ Confirmer Fraude]  [❌ Faux Positif]           │
└─────────────────────────────────────────────────────┘
```

#### Étape 3 : Prise de Décision

**Options disponibles** :

1. **✅ Confirmer Fraude**
   - La carte est automatiquement bloquée
   - Le client reçoit une notification (SMS + push)
   - Un ticket est créé pour contact client
   - L'information enrichit le modèle ML (retraining)

2. **❌ Faux Positif**
   - La transaction est autorisée rétroactivement
   - Le client est informé que tout est normal
   - Le modèle ML apprend à éviter ce type d'erreur

3. **⏸️ Demander Plus d'Infos**
   - Escalade vers un analyste senior
   - Appel téléphonique au client pour confirmation
   - Transaction en attente (timeout 4 heures)

**💡 Conseil** : En cas de doute, **toujours privilégier la sécurité** (confirmer fraude) puis contacter le client. Mieux vaut un faux positif qu'une vraie fraude non détectée.

### 📈 Rapports Personnalisés

#### Créer un Rapport

1. Cliquez sur **"Nouveau Rapport"** en haut à droite
2. Sélectionnez la période : Aujourd'hui / 7 jours / 30 jours / Personnalisé
3. Choisissez les métriques à inclure :
   - ☑️ Nombre de fraudes par catégorie
   - ☑️ Évolution temporelle
   - ☑️ Top 10 merchants
   - ☑️ Répartition géographique
4. Format d'export : PDF / Excel / PowerPoint
5. Cliquez sur **"Générer"**

#### Planifier un Rapport Automatique

**Cas d'usage** : Recevoir chaque lundi matin un rapport hebdomadaire

1. Dans le menu, cliquez sur **"Planification"**
2. Créez une nouvelle tâche :
   - **Nom** : Rapport Hebdo Fraudes
   - **Fréquence** : Tous les lundis à 8h00
   - **Destinataires** : manager@digitalbank.fr, equipe-fraude@digitalbank.fr
   - **Format** : PDF
3. Sauvegardez

➡️ Le rapport sera automatiquement envoyé par email chaque semaine.

---

## 4. Dashboard Service Client {#dashboard-service-client}

**Public** : Équipe Support Client  
**Objectif** : Traiter les alertes clients et consulter l'historique transactionnel

### 🎯 Vue Principale

Le dashboard Service Client est centré sur **les alertes nécessitant une action immédiate**.

#### Section 1 : Alertes en Attente

**Liste priorisée** :

| Priorité | Client | Transaction | Montant | Heure | Statut | Action |
|----------|--------|-------------|---------|-------|--------|--------|
| 🔴 URGENT | Marie L. | Achat en ligne TH | 2 850 € | 16:45 | En attente | [Traiter] |
| 🟠 HAUTE | Pierre D. | Retrait ATM ES | 500 € | 15:30 | En attente | [Traiter] |
| 🟡 MOYENNE | Sophie M. | Paiement UK | 120 € | 14:20 | En attente | [Traiter] |

**Signification des Priorités** :
- **🔴 URGENT** : Montant > 2000 € ou score > 90% → Traiter sous 15 minutes
- **🟠 HAUTE** : Montant 500-2000 € ou score 70-90% → Traiter sous 1 heure
- **🟡 MOYENNE** : Montant < 500 € ou score 50-70% → Traiter sous 4 heures

#### Section 2 : Traitement d'une Alerte

**Clic sur [Traiter]** → Ouverture du panneau de traitement

```
┌─────────────────────────────────────────────────────┐
│  🔴 ALERTE URGENTE                                  │
│                                                     │
│  Cliente : Marie Lefebvre (marie.l@email.com)       │
│  Téléphone : +33 6 12 34 56 78                      │
│                                                     │
│  Transaction Suspecte :                             │
│  ├─ Montant : 2 850,00 €                            │
│  ├─ Merchant : Electronics Store Bangkok            │
│  ├─ Date/Heure : 22/01/2026 16:45 UTC              │
│  └─ Score Fraude : 87% (HAUTE)                      │
│                                                     │
│  Raisons :                                          │
│  • Pays inhabituel (Thaïlande, jamais utilisé)     │
│  • Montant 5x supérieur à la moyenne                │
│  • Device non reconnu                               │
│                                                     │
│  Historique Récent :                                │
│  • 22/01 14:30 - Carrefour Paris - 45€ ✅          │
│  • 21/01 19:12 - Restaurant Lyon - 68€ ✅          │
│  • 20/01 10:05 - SNCF - 120€ ✅                    │
│                                                     │
│  ⚠️ Incohérence : Transaction Paris 14h30,         │
│                   puis Bangkok 16h45 (2h15)         │
│                   → Déplacement physiquement        │
│                      impossible                      │
│                                                     │
│  📞 Actions Disponibles :                           │
│  [📱 Appeler Cliente]  [✉️ Envoyer Email]          │
│  [💳 Bloquer Carte]    [✅ Valider Transaction]    │
└─────────────────────────────────────────────────────┘
```

#### Procédure de Contact Client

**Option 1 : Appel Téléphonique (recommandé pour urgence)**

1. Cliquez sur **[📱 Appeler Cliente]**
2. Le système compose automatiquement le numéro via le softphone
3. Script de conversation :

> "Bonjour Mme Lefebvre, je suis [Votre Nom] du service sécurité DigitalBank. Je vous appelle car nous avons détecté une transaction inhabituelle sur votre compte. Avez-vous effectué un achat de 2 850 € en Thaïlande il y a quelques minutes ?"

**Réponse OUI** → Transaction légitime (rare mais possible : achat en ligne pour un cadeau)
- Cliquez sur **[✅ Valider Transaction]**
- Notez la raison : "Client confirme achat cadeau pour un proche"
- Proposez d'augmenter temporairement le plafond si nécessaire

**Réponse NON** → Fraude confirmée
- Cliquez sur **[💳 Bloquer Carte]** immédiatement
- Informez le client : "Ne vous inquiétez pas, la transaction est annulée et votre carte est bloquée par sécurité. Vous recevrez une nouvelle carte sous 3 jours ouvrés."
- Envoyez un email de confirmation avec les étapes suivantes

**Option 2 : Email (pour priorités moyennes)**

1. Cliquez sur **[✉️ Envoyer Email]**
2. Un modèle pré-rempli s'affiche :

```
Objet : Alerte Sécurité - Transaction à Valider

Bonjour Marie,

Nous avons détecté une transaction inhabituelle sur votre compte :
- Montant : 2 850,00 €
- Commerçant : Electronics Store Bangkok
- Date : 22/01/2026 à 16:45

Si vous êtes à l'origine de cette transaction, aucune action n'est requise.

Dans le cas contraire, veuillez nous contacter immédiatement au 
+33 1 23 45 67 89 ou répondre à cet email.

Par sécurité, nous avons temporairement suspendu votre carte.

Cordialement,
L'équipe Sécurité DigitalBank
```

3. Personnalisez si besoin, puis cliquez sur **"Envoyer"**

#### Section 3 : Historique Client

**Onglet "Historique"** → Vision complète des 90 derniers jours

**Timeline Interactive** :

```
┌─────────────────────────────────────────────────────┐
│  Janvier 2026                                       │
│  ────────────────────────────────────────────────   │
│   22 ●──────●──────●──────●  (4 transactions)      │
│   21 ●──────●─────────────   (2 transactions)      │
│   20 ●────────────────────   (1 transaction)       │
│   19 ──────────────────────  (0 transaction)       │
│   18 ●──────●──────●──────   (3 transactions)      │
│                                                     │
│  Légende : ● Transaction normale  🔴 Fraude         │
│                                                     │
│  [Filtrer par Merchant]  [Filtrer par Montant]      │
└─────────────────────────────────────────────────────┘
```

**Utilisation** :
- **Clic sur un point** → Détails de la transaction
- **Pattern inhabituel** → Alerter l'analyste de sécurité (ex: 15 transactions en 1 journée)

### 📝 Notes et Commentaires

Pour chaque alerte traitée, vous devez **obligatoirement** ajouter une note :

**Champ "Commentaire"** :
```
┌─────────────────────────────────────────────────────┐
│  Résumé du traitement :                             │
│  ┌─────────────────────────────────────────────┐   │
│  │ Contact téléphonique avec cliente à 17h05.  │   │
│  │ Transaction confirmée : achat cadeau pour   │   │
│  │ son fils expatrié en Thaïlande.             │   │
│  │ Cliente a apprécié la réactivité.           │   │
│  │ Transaction validée manuellement.           │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  [Sauvegarder Note]                                 │
└─────────────────────────────────────────────────────┘
```

💡 **Bonnes pratiques** :
- Notez l'heure du contact
- Résumez la réponse du client
- Indiquez l'action prise
- Soyez factuel et concis

---

## 5. Dashboard Monitoring Infrastructure {#dashboard-monitoring-infrastructure}

**Public** : Équipe Infrastructure / DevOps  
**Objectif** : Surveiller la disponibilité et les performances des systèmes

### 🖥️ Vue d'Ensemble

Le dashboard Monitoring affiche en temps réel l'état de santé de la plateforme.

#### Section 1 : Status Global

```
┌─────────────────────────────────────────────────────┐
│  🟢 Tous les systèmes sont opérationnels            │
│  Dernière mise à jour : il y a 10 secondes          │
└─────────────────────────────────────────────────────┘
```

**Codes couleur** :
- 🟢 **Vert** : Tout fonctionne normalement
- 🟡 **Jaune** : Dégradation de performance (latence élevée)
- 🔴 **Rouge** : Incident en cours (service indisponible)

#### Section 2 : État des Services

| Service | Statut | Uptime | Latence | Dernière Vérification |
|---------|--------|--------|---------|----------------------|
| API Fraud Detection | 🟢 UP | 99.97% | 67ms | Il y a 5s |
| Base de Données | 🟢 UP | 99.99% | 12ms | Il y a 10s |
| Dashboards Metabase | 🟢 UP | 99.85% | 234ms | Il y a 15s |
| Workflows Make | 🟢 UP | 99.91% | - | Il y a 30s |
| Monitoring Grafana | 🟢 UP | 100% | 45ms | Il y a 5s |

**Interprétation** :
- **Uptime** : % de disponibilité sur les 30 derniers jours (objectif > 99,5%)
- **Latence** : temps de réponse moyen (objectif < 100ms pour API)

#### Section 3 : Métriques Temps Réel

**Graphiques en Direct** (refresh toutes les 30 secondes) :

**Graphique 1 : Requêtes API par Minute**
```
Req/min
  400 │         ╭╮
  300 │      ╭──╯╰╮
  200 │   ╭──╯    ╰─╮
  100 │╭──╯         ╰─╮
    0 └─────────────────────> temps
       10:00  10:15  10:30
```
- **Normal** : 100-300 req/min
- **Pic** : > 400 req/min (heure de pointe, campagne promo)
- **Creux** : < 50 req/min (nuit)

**Graphique 2 : Utilisation CPU Serveurs**
```
CPU %
  100│
   80│              ╭───
   60│         ╭────╯
   40│    ╭────╯
   20│────╯
    0└─────────────────────> temps
```
⚠️ **Alerte** si CPU > 80% pendant plus de 5 minutes

**Graphique 3 : Erreurs HTTP**
```
Erreurs/min
   50│
   40│
   30│
   20│           🔴 Pic d'erreurs
   10│──────────────•───────
    0└─────────────────────> temps
```
🔴 **Incident** si > 20 erreurs/min

#### Section 4 : Alertes Infrastructure

**Liste des Alertes Actives** :

| Gravité | Service | Message | Durée | Action |
|---------|---------|---------|-------|--------|
| 🟡 WARNING | Database | Connections > 80% du pool | 12 min | [Voir Détails] |
| 🟢 RESOLVED | API | Latence élevée (résolu) | - | [Historique] |

**Actions Possibles** :
- **[Voir Détails]** → Graphiques approfondis et logs
- **[Acquitter]** → Marquer l'alerte comme prise en compte
- **[Créer Ticket Jira]** → Escalader vers l'équipe DevOps

### 🔧 Diagnostic d'un Incident

#### Scenario : Alerte "API Latence Élevée"

**Étape 1 : Identifier la Cause**

1. Cliquez sur l'alerte dans la liste
2. Panneau de diagnostic s'ouvre :

```
┌─────────────────────────────────────────────────────┐
│  🔴 ALERTE : API Response Time > 500ms              │
│                                                     │
│  Début : 22/01/2026 15:45 UTC                       │
│  Durée : 8 minutes                                  │
│                                                     │
│  Métriques Actuelles :                              │
│  ├─ Latence P50 : 456ms (normal: 65ms) 📈 +601%   │
│  ├─ Latence P95 : 1.2s (normal: 87ms) 📈 +1279%   │
│  └─ Taux d'erreur : 5.2% (normal: 0.1%)           │
│                                                     │
│  Causes Probables :                                 │
│  1️⃣ Pic de trafic : 890 req/min (vs. 250 habituel) │
│  2️⃣ Database slow queries : 3 requêtes > 5s        │
│  3️⃣ CPU élevé sur serveur API-2 : 92%              │
│                                                     │
│  [Logs Détaillés]  [Métriques Avancées]            │
└─────────────────────────────────────────────────────┘
```

**Étape 2 : Actions Correctives**

**Si Pic de Trafic** :
- ✅ L'autoscaling Kubernetes va provisionner automatiquement des serveurs supplémentaires (délai : 2-3 minutes)
- Action manuelle : Aucune (sauf si l'autoscaling échoue)

**Si Database Slow Queries** :
- ⚠️ Alerter le DBA (Database Administrator)
- Vérifier les requêtes lentes dans l'onglet "Logs Détaillés"
- Potentiellement : tuer les requêtes bloquantes (nécessite privilèges admin)

**Si CPU Élevé** :
- Redémarrer le conteneur problématique (bouton "Restart API-2")
- Investiguer après résolution (memory leak ? code inefficace ?)

### 📊 Rapports de Disponibilité

**Rapport Mensuel Automatique** (envoyé le 1er de chaque mois) :

```
┌─────────────────────────────────────────────────────┐
│  Rapport Disponibilité - Janvier 2026               │
│                                                     │
│  📈 SLA Global : 99,87% (Objectif: 99,5%) ✅        │
│                                                     │
│  Incidents Majeurs : 2                              │
│  ├─ 08/01 14:30-15:12 : Panne Base de Données      │
│  │  (Durée: 42 min, Impact: Dashboards indispos.)  │
│  └─ 23/01 03:00-03:15 : Maintenance Serveur        │
│     (Durée: 15 min, Impact: Aucun - fenêtre maint.)│
│                                                     │
│  Incidents Mineurs : 8                              │
│  (Latence élevée, résolu en < 10 min)              │
│                                                     │
│  Améliorations Ce Mois :                            │
│  • Mise à niveau PostgreSQL 15.3 → 15.4            │
│  • Optimisation cache Redis (+30% hit rate)        │
│  • Ajout monitoring proactif database connections  │
└─────────────────────────────────────────────────────┘
```

---

## 6. Filtres et Recherches {#filtres-et-recherches}

### 🔍 Barre de Recherche Globale

En haut de chaque dashboard, une barre de recherche permet de trouver rapidement une transaction ou un client.

**Recherche par** :
- **Transaction ID** : `txn_2026012215487abc`
- **User ID** : `usr_98765`
- **Email client** : `marie.l@email.com`
- **Numéro de carte** (4 derniers chiffres) : `**** **** **** 1234`

**Exemple** :
```
┌─────────────────────────────────────────────────────┐
│  🔍 Rechercher... [txn_2026012215487abc        ]    │
└─────────────────────────────────────────────────────┘
```
➡️ Appuyez sur **Entrée** ou cliquez sur la loupe

**Résultat** : Affichage instantané de la fiche transaction

### 🎛️ Filtres Avancés

Chaque dashboard dispose de filtres pour affiner les données affichées.

#### Filtres Communs

**Période** :
- Aujourd'hui
- 7 derniers jours
- 30 derniers jours
- Personnalisé (sélection calendrier)

**Niveau de Risque** :
- ☐ LOW (afficher les risques faibles)
- ☑ MEDIUM
- ☑ HIGH
- ☑ CRITICAL

💡 **Astuce** : Décochez "LOW" pour ne voir que les transactions nécessitant une attention.

**Pays** :
- Liste déroulante des codes ISO (FR, GB, US, etc.)
- Multi-sélection possible (Ctrl+clic)

**Montant** :
- Min : _____ €
- Max : _____ €

**Exemple** : Pour voir uniquement les fraudes > 1000 € en France cette semaine :
1. Période : **7 derniers jours**
2. Niveau de Risque : **HIGH + CRITICAL uniquement**
3. Pays : **FR**
4. Montant Min : **1000**
5. Cliquez sur **"Appliquer Filtres"**

#### Sauvegarde de Filtres

**Fonctionnalité** : Enregistrer une combinaison de filtres pour réutilisation rapide

1. Configurez vos filtres
2. Cliquez sur **"💾 Sauvegarder ce filtre"**
3. Nommez-le : ex. "Fraudes France > 1000€"
4. Prochaine fois : sélectionnez-le dans le menu déroulant "Filtres Sauvegardés"

### 📥 Export de Données

**Formats disponibles** :
- **Excel (.xlsx)** : Pour analyse dans Excel / Google Sheets
- **CSV (.csv)** : Pour import dans d'autres outils
- **PDF** : Pour rapports imprimables / partage email
- **JSON** : Pour intégration technique

**Procédure** :
1. Appliquez les filtres souhaités
2. Cliquez sur **"⬇️ Exporter"** en haut à droite
3. Choisissez le format
4. Le fichier se télécharge dans votre dossier "Téléchargements"

⚠️ **Limite** : Export maximum 50 000 lignes (pour éviter les fichiers trop lourds). Si besoin de plus, contactez l'équipe Data.

---

## 7. Gestion des Alertes {#gestion-des-alertes}

### 🔔 Types d'Alertes

La plateforme génère automatiquement des alertes selon plusieurs critères :

#### Alertes Fraude

**Déclenchement** : Score de fraude > seuil défini

| Niveau | Seuil | Action Automatique | Délai Traitement |
|--------|-------|-------------------|------------------|
| 🟡 MEDIUM | 30-60% | Email analyste | 4 heures |
| 🟠 HIGH | 60-85% | Notification push | 1 heure |
| 🔴 CRITICAL | > 85% | Blocage carte + SMS client | 15 minutes |

#### Alertes Infrastructure

**Déclenchement** : Métriques hors limites

- **API Downtime** : Service non disponible > 1 minute
- **High Latency** : Temps réponse > 500ms pendant 5 minutes
- **Database Issues** : Connection pool > 90% ou replication lag > 10s
- **Disk Space** : Espace disque > 85%

### 📨 Canaux de Notification

**Selon la gravité** :

**Niveau MEDIUM** :
- ✉️ Email (groupé toutes les heures)
- 📊 Dashboard uniquement

**Niveau HIGH** :
- ✉️ Email (immédiat)
- 📱 Notification push (app mobile)
- 💬 Message Slack (#fraud-alerts)

**Niveau CRITICAL** :
- ✉️ Email (immédiat)
- 📱 Notification push
- 💬 Slack (mention @here)
- 📞 Appel PagerDuty (astreinte)

### 🔄 Workflow de Traitement

#### Cycle de Vie d'une Alerte

```
┌─────────┐      ┌──────────┐      ┌─────────┐      ┌────────┐
│ NOUVEAU │─────▶│ ASSIGNÉ  │─────▶│ EN COURS│─────▶│ RÉSOLU │
└─────────┘      └──────────┘      └─────────┘      └────────┘
                                         │
                                         ▼
                                   ┌──────────┐
                                   │ ESCALADÉ │
                                   └──────────┘
```

**NOUVEAU** :
- Alerte vient d'être créée
- Visible dans la liste "Alertes en Attente"
- Assignment automatique selon règles de routing (charge équipe, compétences)

**ASSIGNÉ** :
- Un analyste a été assigné (automatiquement ou manuellement)
- Notification envoyée à l'analyste
- Timer SLA démarre

**EN COURS** :
- Analyste a cliqué sur "Traiter"
- Investigation en cours
- Possibilité d'ajouter des notes

**ESCALADÉ** :
- Cas complexe nécessitant expertise senior
- Re-assignment automatique vers manager ou analyste L2
- SLA prolongé

**RÉSOLU** :
- Décision prise (fraude confirmée ou faux positif)
- Client contacté si nécessaire
- Archivage de l'alerte avec notes

#### Règles d'Escalade Automatique

**Escalade vers Manager** si :
- Alerte non traitée dans le délai SLA
- Montant > 10 000 €
- Client VIP (statut premium)
- Plus de 3 faux positifs sur ce client (nécessite revue)

**Notification Manager** :
> "⚠️ Alerte #2026012245 escaladée : transaction 15 000 € client VIP non traitée depuis 20 minutes. Analyste initial : Pierre D."

### 📊 Suivi de Performance

**Dashboard Équipe** (visible pour managers) :

```
┌─────────────────────────────────────────────────────┐
│  Performance Équipe - Janvier 2026                  │
│                                                     │
│  Alertes Traitées : 1 847                           │
│  Temps Moyen Résolution : 12 min (Objectif: 15min) │
│  SLA Respecté : 96,3% (Objectif: 95%) ✅            │
│                                                     │
│  Top Performers :                                   │
│  🥇 Sophie M.  : 247 alertes, 8 min avg            │
│  🥈 Pierre D.  : 198 alertes, 11 min avg           │
│  🥉 Marie L.   : 176 alertes, 13 min avg           │
│                                                     │
│  Alertes en Attente : 12 (🟡 Normal)                │
│  Backlog : < 1 heure                                │
└─────────────────────────────────────────────────────┘
```

**Indicateurs Individuels** (visible dans votre profil) :

- Nombre d'alertes traitées ce mois
- Temps moyen de résolution
- Taux de faux positifs (objectif < 5%)
- Feedback clients (satisfaction)

---

## 8. Bonnes Pratiques {#bonnes-pratiques}

### ✅ Do's (À Faire)

**Sécurité** :
- ✅ **Déconnectez-vous** toujours après utilisation
- ✅ **Verrouillez votre session** quand vous vous absentez (Windows+L)
- ✅ **Utilisez un mot de passe fort** (12+ caractères, lettres+chiffres+symboles)
- ✅ **Activez la double authentification** (2FA) dans vos paramètres
- ✅ **Signalez immédiatement** toute activité suspecte sur votre compte

**Traitement des Alertes** :
- ✅ **Priorisez** les alertes CRITICAL et HIGH en premier
- ✅ **Ajoutez toujours une note** après traitement (obligation de conformité)
- ✅ **Contactez le client** en cas de doute (mieux vaut un appel de trop)
- ✅ **Respectez les scripts** de conversation (formulation claire, professionnelle)
- ✅ **Documentez les cas atypiques** pour amélioration du modèle ML

**Utilisation de la Plateforme** :
- ✅ **Rafraîchissez régulièrement** les dashboards (F5 ou bouton refresh)
- ✅ **Utilisez les filtres** pour affiner vos recherches
- ✅ **Sauvegardez vos filtres récurrents** (gain de temps)
- ✅ **Exportez les rapports** pour vos comptes-rendus hebdomadaires

**Communication** :
- ✅ **Partagez les insights** intéressants avec l'équipe (Slack #fraud-insights)
- ✅ **Remontez les bugs** via le bouton "Signaler un problème"
- ✅ **Participez aux formations** trimestrielles (mise à jour des procédures)

### ❌ Don'ts (À Éviter)

**Sécurité** :
- ❌ **NE partagez JAMAIS** vos identifiants (même avec un collègue)
- ❌ **NE notez PAS** vos mots de passe sur papier ou fichier non chiffré
- ❌ **N'accédez PAS** à la plateforme depuis un réseau WiFi public non sécurisé
- ❌ **NE prenez PAS** de captures d'écran incluant des données clients (RGPD)

**Traitement des Alertes** :
- ❌ **NE validez PAS** une transaction suspecte sans investigation
- ❌ **N'ignorez PAS** une alerte même si elle semble être un faux positif
- ❌ **NE bloquez PAS** une carte sans avoir tenté de contacter le client d'abord (sauf CRITICAL)
- ❌ **N'escaladez PAS** systématiquement : vous êtes formés pour gérer la majorité des cas

**Communication Client** :
- ❌ **NE promettez PAS** de remboursement avant validation par le manager
- ❌ **N'utilisez PAS** de termes techniques incompréhensibles pour le client
- ❌ **NE culpabilisez PAS** le client ("Vous auriez dû faire attention...")
- ❌ **NE divulguez PAS** de détails sur notre système de détection

**Utilisation de la Plateforme** :
- ❌ **N'ouvrez PAS** plusieurs onglets de la même page (risque de conflits)
- ❌ **NE forcez PAS** le rechargement incessant (charge serveur inutile)
- ❌ **N'exportez PAS** plus de données que nécessaire (RGPD : minimisation)

### 🎯 Conseils d'Efficacité

**Gagner du Temps** :
- 🚀 **Raccourcis clavier** :
  - `Ctrl+K` : Ouvrir la barre de recherche
  - `Ctrl+F` : Filtrer la page actuelle
  - `Ctrl+E` : Exporter la vue actuelle
  - `Esc` : Fermer un panneau/modal

- 🚀 **Filtres intelligents** :
  - Créez un filtre "Mes alertes du jour" pour votre routine matinale
  - Utilisez "Fraudes confirmées semaine" pour votre reporting hebdo

- 🚀 **Modèles de notes** :
  - Créez des templates pour situations récurrentes (ex: "Client injoignable", "Transaction validée par téléphone")

**Améliorer Votre Performance** :
- 📊 **Consultez vos stats** chaque semaine (menu "Mon Profil" → "Performance")
- 📊 **Identifiez vos points faibles** (ex: temps résolution trop long sur alertes HIGH)
- 📊 **Fixez-vous des objectifs** (ex: "Descendre sous 10 min de moyenne ce mois")

**Apprendre en Continu** :
- 📚 **Lisez les post-mortems** d'incidents (Slack #fraud-incidents-analysis)
- 📚 **Participez aux ateliers** mensuels "Cas d'école" (analyse de fraudes complexes)
- 📚 **Consultez la FAQ** régulièrement (mise à jour avec nouveaux cas)

---

## 9. FAQ {#faq}

### 🔐 Connexion et Accès

**Q : J'ai oublié mon mot de passe, que faire ?**
> R : Cliquez sur "Mot de passe oublié" sur la page de connexion. Un email de réinitialisation sera envoyé à votre adresse professionnelle. Si vous ne le recevez pas sous 5 minutes, vérifiez vos spams ou contactez le support IT.

**Q : Pourquoi mon compte est-il bloqué ?**
> R : Votre compte se bloque automatiquement après 5 tentatives de connexion échouées (sécurité). Contactez votre manager ou le support IT (+33 1 23 45 67 89) pour déblocage.

**Q : Puis-je accéder à la plateforme depuis mon téléphone ?**
> R : Oui, la plateforme est responsive (compatible mobile). Utilisez le navigateur de votre smartphone professionnel. L'app mobile dédiée est en cours de développement (sortie prévue Q2 2026).

### 📊 Dashboards et Données

**Q : Les chiffres affichés ne correspondent pas à mon export Excel, pourquoi ?**
> R : Les dashboards se rafraîchissent toutes les 30 secondes. Si vous exportez puis consultez le dashboard 5 minutes après, de nouvelles données sont apparues. Astuce : exportez immédiatement après avoir appliqué vos filtres.

**Q : Puis-je créer mon propre dashboard personnalisé ?**
> R : Oui, fonction disponible pour les utilisateurs avancés. Menu "Dashboards" → "Créer un nouveau dashboard". Tutoriel vidéo disponible dans l'aide en ligne.

**Q : Combien de temps les données historiques sont-elles conservées ?**
> R : 
> - **Transactions et alertes** : 5 ans (conformité réglementaire)
> - **Métriques monitoring** : 1 an (agrégations), 15 jours (métriques brutes)
> - **Logs** : 90 jours (opérationnel), 7 ans (audit)

### 🚨 Alertes et Fraudes

**Q : Comment savoir si une alerte est vraiment une fraude ?**
> R : Indices de fraude avérée :
> - Transaction dans un pays jamais visité par le client
> - Device inconnu + IP suspecte
> - Montant très supérieur à l'habitude
> - Vélocité élevée (plusieurs transactions rapprochées)
> - Combinaison de plusieurs facteurs de risque
> 
> En cas de doute, **toujours contacter le client**.

**Q : Que faire si le client ne répond ni au téléphone ni à l'email ?**
> R : 
> 1. Tentez un second appel 15 minutes après
> 2. Si toujours injoignable et score > 85% : bloquez par sécurité
> 3. Laissez un message vocal explicatif
> 4. Notez "Client injoignable - décision préventive" dans le commentaire
> 5. Réessayez dans 2 heures

**Q : Un client se plaint d'un faux positif récurrent, comment gérer ?**
> R : 
> 1. Excusez-vous pour le désagrément
> 2. Expliquez que c'est pour sa sécurité
> 3. Escaladez vers un analyste senior pour ajustement du profil de risque client
> 4. Proposez une augmentation temporaire de plafond si justifié
> 5. Notez le cas dans le CRM pour suivi

### 🔧 Problèmes Techniques

**Q : Le dashboard ne se charge pas / page blanche**
> R : 
> 1. Vérifiez votre connexion internet
> 2. Videz le cache navigateur (Ctrl+Shift+Suppr)
> 3. Essayez en navigation privée
> 4. Si le problème persiste, vérifiez la page statut : https://status.digitalbank.fr
> 5. Contactez le support IT si incident généralisé

**Q : J'ai cliqué sur "Bloquer Carte" par erreur, puis-je annuler ?**
> R : ⚠️ **Non, cette action est irréversible** (pour des raisons de sécurité). La carte est immédiatement désactivée. Seule solution : contacter le client, lui expliquer l'erreur, et commander une nouvelle carte en express (délai 24h au lieu de 3 jours).

**Q : L'export Excel échoue avec un message "Timeout"**
> R : Vous essayez probablement d'exporter trop de données (> 50 000 lignes). Affinez vos filtres (par exemple, limitez la période à 7 jours au lieu de 30 jours) et réessayez.

### 📞 Support et Formation

**Q : Où trouver de l'aide supplémentaire ?**
> R : 
> - **Documentation complète** : https://docs.digitalbank-fraud.esic.cloud
> - **Vidéos tutoriels** : Onglet "Formation" dans le menu
> - **Support IT** : +33 1 23 45 67 89 (lun-ven 9h-18h)
> - **Email support** : support-fraud@digitalbank.fr
> - **Slack** : #fraud-platform-help

**Q : Existe-t-il des formations pour maîtriser la plateforme ?**
> R : Oui, formations disponibles :
> - **Onboarding nouveaux arrivants** : 2h (obligatoire)
> - **Formation avancée dashboards** : 4h (optionnelle)
> - **Certification Analyste Fraude** : 2 jours (requis pour promotion)
> 
> Inscriptions via RH ou votre manager.

**Q : Comment proposer une amélioration de la plateforme ?**
> R : Nous adorons vos retours ! 💡
> - **Bouton "Suggérer une amélioration"** (en bas de chaque page)
> - **Email** : product-feedback@digitalbank.fr
> - **Slack** : #fraud-platform-feedback
> 
> Les meilleures suggestions sont récompensées (prime trimestrielle "Innovation Award").

---

## 📞 Contacts Utiles

| Service | Contact | Disponibilité |
|---------|---------|---------------|
| **Support Technique** | +33 1 23 45 67 89 | Lun-Ven 9h-18h |
| **Support IT (urgent)** | +33 1 23 45 67 00 | 24/7 |
| **Manager Équipe Fraude** | manager-fraude@digitalbank.fr | Lun-Ven 9h-19h |
| **DPO (RGPD)** | dpo@digitalbank.fr | Sur RDV |
| **Hotline Clients** | +33 1 23 45 67 99 | 24/7 |

---

## 📄 Informations Document

**Dernière mise à jour** : Janvier 2026  
**Version** : 1.0  
**Auteur** : Équipe Projet DigitalBank - ESIC Paris  
**Prochaine révision** : Avril 2026

---

**© 2026 DigitalBank France - Document Confidentiel - Usage Interne Uniquement**
