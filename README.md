# 🚴 Vekta - reproduction

**Pipeline de génération de séances d'entraînement cycliste avec architecture hybride strict**

## 🎯 Description

Projet démontrant deux implémentations du pipeline Vekta :
- **📚 Pipeline de Démonstration** : Notebook interactif explicatif (8 sections)
- **🚀 Pipeline Production** : Application complète avec API REST + Interface web

**Principe architectural commun** : AUCUNE estimation automatique, OpenDuration explicite, génération Zwift native.

---

## 📁 Structure Globale du Projet

```
Vekta/
├── 📚 Demo_Pipeline_Vekta_Interview.ipynb    # 🎯 PIPELINE DÉMO
│                                             # Notebook pédagogique interactif
│                                             # Démonstration architecture stricte
│                                             # Tests validation + export Zwift
│
├── 🚀 vekta/                                 # 🎯 PIPELINE PRODUCTION
│   ├── components/vekta_components.py        # Core: parsing + validation + corpus
│   ├── api/vekta_api.py                      # API REST FastAPI
│   ├── frontend/vekta_app.py                 # Interface Streamlit
│   ├── docker-compose.yml                   # Déploiement containerisé
│   └── launch_vekta.py                       # Lanceur automatique
│
├── 📁 generated_workouts/                    # Fichiers .zwo générés (partagé)
├── 📄 README.md                              # Documentation architecturale globale
└── 📄 .gitignore                             # Configuration Git
```

---

## 🎯 Comparaison des Deux Pipelines

### 📚 **Pipeline de Démonstration** (Notebook)

**Objectif** : Explication pédagogique de l'architecture stricte

| Aspect | Implémentation Démo |
|--------|-------------------|
| **🎯 But** | Démonstration interactive + tests validation |
| **📋 Format** | Jupyter Notebook (8 sections séquentielles) |
| **🔧 Architecture** | Classes autonomes avec documentation inline |
| **📊 Validation** | 4 cas d'usage types avec métriques détaillées |
| **⚡ Performance** | Optimisé pour clarté (benchmark <1ms) |
| **🚴 Export Zwift** | Génération directe dans `generated_workouts/` |
| **📈 Monitoring** | Affichage temps réel avec `display(Markdown())` |

**Structure des 8 Sections :**
1. **🧩 Parseur Structurel** - Extraction regex haute précision
2. **📊 Tests Précision** - Validation sur requêtes réelles Vekta
3. **🚫 Générateur STRICT** - Logique OpenDuration sans estimation
4. **🔄 Pipeline Hybride** - 90% parsing + 10% enrichissement corpus
5. **✅ Validation Démo** - Cas d'usage avec scoring gradué
6. **⚡ Analyse Performance** - Benchmark objectif <100ms
7. **📋 Architecture Technique** - Documentation formatée complète
8. **🚴 Génération Zwift** - Export .zwo avec métadonnées

### 🚀 **Pipeline Complet Reproduction** 

**Objectif** : Déploiement industriel avec monitoring

| Aspect | Implémentation Production |
|--------|-------------------------|
| **🎯 But** | Application web complète + API REST |
| **📋 Format** | FastAPI + Streamlit + Docker |
| **🔧 Architecture** | Modules séparés + configuration centralisée |
| **📊 Validation** | Endpoints spécialisés + validation Pydantic |
| **⚡ Performance** | Optimisé pour throughput (cache + async) |
| **🚴 Export Zwift** | Téléchargement direct + stockage persistant |
| **📈 Monitoring** | Métriques Prometheus + logs structurés |

**Composants Architecture :**
- **`components/`** : Pipeline core (parsing + validation + corpus)
- **`api/`** : Endpoints REST avec documentation Swagger
- **`frontend/`** : Interface utilisateur avec graphiques Plotly
- **`Docker`** : Containerisation pour déploiement multi-environnement

---

## 🔧 Architecture Commune : Pipeline Hybride Strict

### 🚫 **Philosophie "Pas d'Estimation"**

**Principe fondamental** partagé par les deux implémentations :

```python
# ❌ ANCIEN : Estimation automatique
def _calculate_recovery_duration(intensity):
    return intensity * 0.5  # Calcul physiologique

# ✅ NOUVEAU : OpenDuration explicite
def handle_missing_duration(workout_step):
    return "OpenDuration"  # Utilisateur spécifie
```

### ⚡ **Pipeline Hybride (90% + 10%)**

**Architecture partagée** optimisée pour précision :

1. **90% Parsing Structurel** : Extraction regex directe
   - Durées, intensités, structures répétitives
   - Latence : <5ms
   - Précision : 95% cas d'usage cyclisme

2. **10% Enrichissement Corpus** : Complétion sémantique
   - Similarité vectorielle uniquement si parsing insuffisant
   - Latence : <95ms
   - Couverture : Cas non prévus par patterns

### 🎯 **Validation Graduée (3 Niveaux)**

**Scoring commun** aux deux pipelines :

| Score | Traitement | Confiance | Méthode |
|-------|------------|-----------|---------|
| **≥ 0.8** | Génération directe | 90% | Parsing seul |
| **0.4-0.8** | Enrichissement corpus | 50-75% | Parsing + corpus |
| **< 0.4** | Erreur avec guidance | 0% | Informations manquantes |

### 🚴 **Export Zwift Standard**

**Format compatible** identique :

```xml
<workout_file>
  <author>Vekta Pipeline</author>
  <name>Vekta: [Requête originale]</name>
  <description>
    Généré par Vekta Pipeline
    Requête: [texte_original]
    Confiance: [score]%
    Méthode: [parsing|parsing_plus_corpus]
  </description>
  <workout>
    <!-- Steps automatiquement convertis -->
    <SteadyState Duration="X" PowerLow="Y" PowerHigh="Y"/>
  </workout>
</workout_file>
```

---

## 🚀 Lancement Rapide

### 📚 **Pipeline Démo** (Notebook)
```bash
# Démonstration interactive complète
jupyter notebook Demo_Pipeline_Vekta_Interview.ipynb

# Section par section:
# 1-2: Architecture parsing (5 min)
# 3-4: Pipeline strict + hybride (5 min)  
# 5-6: Validation + performance (5 min)
# 7-8: Documentation + export Zwift (5 min)
```

### 🚀 **Pipeline Production** (Application)
```bash
# Lancement automatique
cd vekta/
python launch_vekta.py

# Accès services:
# Interface: http://localhost:8501
# API: http://localhost:8000
# Documentation: http://localhost:8000/docs
```

### 🐳 **Déploiement Docker**
```bash
cd vekta/
docker-compose up --build

# Services containerisés:
# - API FastAPI (port 8000)
# - Interface Streamlit (port 8501)
# - Volume partagé generated_workouts/
```

---

## 📊 Validation Comparative

### 🧪 **Tests Communs**

**Jeu de données identique** pour les deux pipelines :

```python
# Cas 1: Auto-génération (Score 1.0)
"5x8min à 92%FTP avec 3min récup"
# → Démo: 9 steps, notebook cell output
# → Prod: API response + .zwo download

# Cas 2: OpenDuration (Score 0.5)  
"séance tempo de 45min"
# → Démo: Markdown display avec métriques
# → Prod: Interface web + graphique zones

# Cas 3: Mode Coach (Score 0.9 forcé)
"6 heures à 130%FTP sans pause"
# → Démo: Validation bypass démonstration
# → Prod: Mode expert avec avertissement

# Cas 4: Erreur (Score 0.0)
"faire du vélo"
# → Démo: Cellule erreur avec suggestions
# → Prod: HTTP 400 + guidance structurée
```

## 📚 Technologies Principales

### **Core Pipeline** (Commun)
- **Regex** : Parsing structurel haute précision
- **Sentence Transformers** : Enrichissement corpus (optionnel)
- **XML ElementTree** : Génération fichiers .zwo natifs

### **Pipeline Démo**
- **Jupyter** : Notebook interactif avec cellules markdown
- **IPython.display** : Rendu temps réel avec tableaux
- **Pandas** : Manipulation données validation

### **Pipeline Production**  
- **FastAPI** : API REST avec validation Pydantic
- **Streamlit** : Interface web avec graphiques Plotly
- **Docker** : Containerisation multi-services
- **Uvicorn** : Serveur ASGI haute performance

---

## 🎯 Objectifs Architecturaux Atteints

### ✅ **Architecture Stricte**
- **Démo** : Démonstration pédagogique suppression estimations
- **Prod** : Implémentation industrielle OpenDuration

### ✅ **Performance <100ms**
- **Démo** : Benchmark optimisé clarté (<1ms)
- **Prod** : Throughput optimisé scalabilité (<100ms)

### ✅ **Export Zwift Native**
- **Démo** : Génération directe avec aperçu XML
- **Prod** : Téléchargement + stockage persistant

### ✅ **Validation Graduée**
- **Démo** : Scoring explicite avec métriques
- **Prod** : Endpoints spécialisés + monitoring
