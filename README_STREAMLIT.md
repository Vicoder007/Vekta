# 🚴 Vekta - Interface Streamlit

Interface web moderne pour le générateur de séances d'entraînement cycliste Vekta, alimenté par l'IA.

## 🌟 Fonctionnalités

### Interface Principale
- **Design moderne** reproduisant fidèlement l'interface Vekta originale
- **Saisie en langage naturel** avec correction orthographique automatique
- **Support du français familier** : "je doie faire dix minut de chaude, apres 3 set de 5 mn a fond"
- **Validation en temps réel** avec score de confiance
- **Génération automatique** de séances structurées

### Visualisations
- **Graphique de puissance** interactif avec zones colorées
- **Métriques détaillées** : durée, puissance moyenne, calories, training stimulus
- **Structure de séance** avec étapes détaillées
- **Zones de puissance** calculées automatiquement

### Fonctionnalités Avancées
- **Téléchargement .zwo** compatible Zwift
- **Configuration des zones** de puissance personnalisées
- **Paramètres avancés** dans l'onglet Options
- **Statistiques API** en temps réel
- **Test de connectivité** intégré

## 🚀 Démarrage Rapide

### Option 1: Script de lancement automatique
```bash
python start_vekta.py
```

### Option 2: Démarrage manuel
```bash
# Terminal 1: API
uvicorn vekta_api:app --reload

# Terminal 2: Interface
streamlit run vekta_app.py
```

### Accès
- **Interface web**: http://localhost:8501
- **API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## 📱 Utilisation

### 1. Configuration de Base
1. Ouvrez l'interface web
2. Saisissez votre requête en français naturel
3. Configurez l'auteur et la durée
4. Ajustez la puissance critique (Critical Power)

### 2. Génération de Séance
1. Cliquez sur "🚀 Générer la Séance"
2. Visualisez les métriques et le graphique
3. Consultez la structure détaillée
4. Téléchargez le fichier .zwo

### 3. Options Avancées
- Ajustez les seuils de confiance
- Configurez les paramètres de génération
- Consultez les statistiques API
- Testez la connectivité

## 🎯 Exemples de Requêtes

### Français Standard
```
10 minutes d'échauffement puis 3 séries de 5 minutes à fond avec 2 minutes de repos entre séries puis 10 minutes de retour au calme
```

### Français Familier
```
je doie faire dix minut de chaude, apres 3 set de 5 mn a fond et 2 min pose entre set. fini avk 10 min cool down facile
```

### Séances Complexes
```
15min échauffement progressif puis pyramide 1-2-3-4-3-2-1 minutes à 95% FTP avec 1min récup entre puis 10min retour calme
```

## 🎨 Design et UX

### Composants Visuels
- **Header gradient** bleu avec logo Vekta
- **Onglets stylisés** Main/Options
- **Cartes métriques** avec bordures colorées
- **Graphique interactif** Plotly avec zones de puissance
- **Étapes de séance** avec codes couleur par zone
- **Bouton de téléchargement** jaune signature

### Couleurs des Zones
- **Zone 1**: Gris (#6b7280) - Récupération active
- **Zone 2**: Bleu (#3b82f6) - Endurance
- **Zone 3**: Vert (#10b981) - Tempo
- **Zone 4**: Orange (#f59e0b) - Seuil
- **Zone 5**: Rouge (#ef4444) - VO2 Max
- **Zone 6**: Violet (#8b5cf6) - Capacité anaérobie
- **Zone 7**: Rose (#ec4899) - Puissance neuromusculaire

## ⚙️ Configuration

### Variables d'Environnement
```bash
# API Configuration
API_BASE_URL=http://localhost:8000

# Streamlit Configuration  
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Paramètres Streamlit
```toml
# .streamlit/config.toml
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false

[browser]
gatherUsageStats = false
```

## 🔧 Architecture Technique

### Stack Technologique
- **Frontend**: Streamlit 1.46.0
- **Graphiques**: Plotly 6.1.2
- **Backend**: FastAPI + RAG Pipeline
- **Styling**: CSS personnalisé + HTML

### Flux de Données
1. **Saisie utilisateur** → Validation frontend
2. **Appel API** `/validate` → Score de confiance
3. **Génération** `/generate-workout` → Données structurées
4. **Visualisation** → Graphiques + Métriques
5. **Export** → Fichier .zwo

### Gestion d'Erreurs
- **API indisponible**: Message d'erreur avec instructions
- **Timeout**: Retry automatique avec feedback
- **Validation échouée**: Suggestions d'amélioration
- **Génération échouée**: Détails techniques dans l'expandeur

## 🚨 Dépannage

### API Non Disponible
```bash
# Vérifier le statut
curl http://localhost:8000/health

# Redémarrer l'API
uvicorn vekta_api:app --reload --port 8000
```

### Interface Non Accessible
```bash
# Vérifier le port
lsof -i :8501

# Redémarrer Streamlit
streamlit run vekta_app.py --server.port 8501
```

### Problèmes de Performance
- Augmenter les timeouts API (actuellement 10s)
- Vérifier la charge système
- Consulter les logs dans `vekta_api.log`

## 📊 Métriques et Monitoring

### Métriques Affichées
- **Requêtes traitées**: Compteur total
- **Taux de succès**: Pourcentage de validations réussies
- **Temps de réponse**: Moyenne des appels API
- **Statut des composants**: Health check détaillé

### Logs Disponibles
- **API logs**: `vekta_api.log`
- **Streamlit logs**: Console de démarrage
- **Erreurs utilisateur**: Interface web

## 🔮 Roadmap

### Prochaines Fonctionnalités
- [ ] **Sauvegarde de séances** favorites
- [ ] **Historique** des générations
- [ ] **Templates** de séances prédéfinies
- [ ] **Export** vers autres formats (TrainerRoad, etc.)
- [ ] **Mode sombre** pour l'interface
- [ ] **Internationalisation** (EN, ES, IT)

### Améliorations UX
- [ ] **Autocomplete** pour les requêtes
- [ ] **Aperçu temps réel** pendant la saisie
- [ ] **Comparaison** de séances
- [ ] **Recommandations** basées sur l'historique

---

**Développé avec ❤️ pour la communauté cycliste** 