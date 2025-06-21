# 🚀 Vekta - Projet Complet

Application complète de génération intelligente de séances d'entraînement cycliste.

## 🏗️ Architecture

```
vekta/
├── api/                    # Backend FastAPI
│   └── vekta_api.py       # API REST + Pipeline RAG
├── frontend/              # Interface utilisateur
│   └── vekta_app.py      # Application Streamlit
├── components/            # Composants IA
│   └── vekta_components.py # Pipeline RAG + Correcteur
├── config/                # Configuration
│   └── .streamlit/       # Config interface
├── docs/                  # Documentation
├── start_vekta.py        # Script de lancement
├── requirements.txt      # Dépendances Python
├── docker-compose.yml    # Déploiement Docker
└── Dockerfile           # Image Docker
```

## 🚀 Installation et Lancement

### Méthode 1 : Lancement Automatique (Recommandé)
```bash
# Installation des dépendances
pip install -r requirements.txt

# Lancement automatique (API + Interface)
python start_vekta.py
```

### Méthode 2 : Lancement Manuel
```bash
# Terminal 1 - API
cd api
uvicorn vekta_api:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Interface
cd frontend
streamlit run vekta_app.py --server.port 8501
```

### Méthode 3 : Docker
```bash
# Construction et lancement
docker-compose up -d

# Arrêt
docker-compose down
```

## 🌐 Accès aux Services

| Service | URL | Description |
|---------|-----|-------------|
| **Interface Web** | http://localhost:8501 | Interface utilisateur Streamlit |
| **API REST** | http://localhost:8000 | API FastAPI |
| **Documentation API** | http://localhost:8000/docs | Swagger UI |
| **Métriques** | http://localhost:8000/metrics | Statistiques de performance |

## 🔧 Configuration

### Variables d'Environnement
```bash
# API
API_HOST=127.0.0.1
API_PORT=8000

# Interface
STREAMLIT_PORT=8501
STREAMLIT_HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
```

### Configuration Streamlit
Voir `config/.streamlit/config.toml` pour la configuration de l'interface.

## 📊 Utilisation

### 1. Interface Web
1. Ouvrir http://localhost:8501
2. Saisir une description d'entraînement
3. Configurer la puissance critique
4. Cliquer sur "Générer la Séance"
5. Télécharger le fichier .zwo

### 2. API REST
```python
import requests

# Validation d'une requête
response = requests.post("http://localhost:8000/validate", json={
    "query": "10min échauffement puis 3 séries de 5min à fond"
})

# Génération complète
response = requests.post("http://localhost:8000/generate-workout", json={
    "query": "10min échauffement puis 3 séries de 5min à fond",
    "critical_power": 250,
    "author": "Mon Nom"
})
```

## 🧪 Tests

```bash
# Tests de l'API
cd ../examples
python test_api_client.py

# Tests de l'interface
python test_streamlit_interface.py
```

## 📈 Monitoring

### Métriques Disponibles
- Nombre de requêtes par endpoint
- Temps de réponse moyen
- Taux de succès
- Uptime du service

### Logs
```bash
# Consultation des logs
tail -f vekta_api.log

# Logs en temps réel
docker-compose logs -f vekta-api
```

## 🔧 Développement

### Structure du Code
- **API** : FastAPI avec endpoints REST
- **Components** : Pipeline RAG modulaire
- **Frontend** : Streamlit avec visualisations Plotly
- **Config** : Configuration centralisée

### Ajout de Fonctionnalités
1. **Nouveau composant** : Ajouter dans `components/`
2. **Nouvel endpoint** : Modifier `api/vekta_api.py`
3. **Nouvelle interface** : Modifier `frontend/vekta_app.py`

## 🚀 Déploiement

### Production
```bash
# Variables d'environnement
export API_HOST=0.0.0.0
export API_PORT=8000

# Lancement production
gunicorn api.vekta_api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Production
```bash
# Build
docker build -t vekta:latest .

# Run
docker run -p 8000:8000 -p 8501:8501 vekta:latest
```

## 📚 Documentation

- **[Guide Utilisateur](docs/GUIDE_UTILISATEUR.md)** : Mode d'emploi détaillé
- **[Documentation API](docs/README_STREAMLIT.md)** : Référence technique
- **[Status du Projet](docs/STATUS_FINAL.md)** : Bilan complet

## 🐛 Dépannage

### Problèmes Courants

**Port déjà utilisé**
```bash
# Trouver le processus
lsof -i :8501
# Tuer le processus
kill -9 <PID>
```

**Erreur de dépendances**
```bash
pip install --upgrade -r requirements.txt
```

**Problème de configuration Streamlit**
```bash
streamlit config show
```

## 📞 Support

Pour toute question technique, consulter :
1. La documentation dans `docs/`
2. Les exemples dans `../examples/`
3. Les notebooks de recherche dans `../research/` 