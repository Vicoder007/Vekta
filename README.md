# 🚴‍♂️ Vekta V2 - Générateur d'Entraînements Intelligents pour Mac M3

## 🎯 **Qu'est-ce que Vekta V2 ?**

Vekta V2 est un générateur d'entraînements cyclistes intelligent spécialement optimisé pour **Mac M3**. Il utilise un modèle IA local (`llama3.2:3b`) pour comprendre vos demandes en langage naturel et générer des séances d'entraînement structurées.

## ⚡ **Démarrage Ultra-Rapide**

```bash
# Lancement automatique (tout-en-un)
python3 launch_vekta_v2.py
```

L'application va automatiquement :
- ✅ Installer Ollama si nécessaire  
- ✅ Télécharger le modèle optimisé Mac M3
- ✅ Lancer l'interface sur http://localhost:8502

## 🧠 **Intelligence Artificielle Locale**

- **Modèle** : `llama3.2:3b` (3 milliards de paramètres)
- **Optimisé** : Spécialement choisi pour Mac M3
- **Performance** : 4-15 secondes de génération
- **Mémoire** : ~2GB (respecte votre système)
- **Privé** : 100% local, aucune donnée externe

## 🚀 **Fonctionnalités**

### **Parser Intelligent**
- Comprend le **langage familier** français
- Gère les **structures complexes** (blocs, intervalles imbriqués)
- **Auto-correction** des fautes de frappe
- **Fallbacks robustes** en cas d'erreur

### **Exemples de Requêtes**
```
"10 min chofe, puis 3x(5min seuil + 2min récup), 10min retour calme"

"2 blocs: chaque bloc 4 répétitions de 30s à fond avec 30s pose"

"pyramide 1-2-3-4-3-2-1 min vo2max, 1min récup entre chaque"
```

### **Formats de Sortie**
- **Interface web** avec graphiques interactifs
- **Fichiers Zwift** (.zwo) exportables
- **Métriques détaillées** (TSS, puissance, zones)

## 📊 **Zones de Puissance Automatiques**

Le système calcule automatiquement vos zones basées sur votre Critical Power :

| Zone | Intensité | Description |
|------|-----------|-------------|
| Z1   | < 55%     | Récupération |
| Z2   | 55-75%    | Endurance |
| Z3   | 75-90%    | Tempo |
| Z4   | 90-105%   | Seuil |
| Z5   | > 105%    | VO2max |

## 🔧 **Configuration Requise**

- **macOS** (optimisé pour M3)
- **Python 3.8+**
- **4GB+ RAM** recommandés
- **Ollama** (installé automatiquement)

## 🧪 **Tests et Diagnostics**

```bash
# Test complet de la configuration
python3 test_mac_m3_setup.py

# Installation manuelle Ollama (si nécessaire)
./install_ollama_mac.sh
```

## 📁 **Structure du Projet**

```
Vekta/
├── launch_vekta_v2.py          # 🚀 Lanceur principal
├── components/
│   └── llm_parser_simple.py   # 🧠 Parser intelligent
├── frontend/
│   └── vekta_app_simple.py     # 🖥️ Interface Streamlit
├── install_ollama_mac.sh       # 🔧 Installation Mac M3
├── test_mac_m3_setup.py        # 🧪 Tests diagnostics
└── requirements.txt            # 📦 Dépendances essentielles
```

## 🎨 **Interface**

L'interface web propose :
- **Saisie naturelle** : Décrivez votre séance comme vous voulez
- **Monitoring temps réel** : État du modèle IA
- **Graphiques interactifs** : Visualisation de votre entraînement
- **Export Zwift** : Fichiers .zwo prêts à l'emploi

## 🔍 **Dépannage**

### Ollama ne démarre pas
```bash
brew install ollama
ollama serve
```

### Modèle lent (>30s)
- Fermez d'autres applications
- Redémarrez : `pkill ollama && ollama serve`

### Mémoire insuffisante
- Le modèle fonctionne avec 4GB+ de libre
- Redémarrez votre Mac si nécessaire

## 📈 **Performance Mac M3**

- **Génération simple** : 3-8 secondes
- **Structure complexe** : 8-15 secondes  
- **Utilisation mémoire** : 2-4GB
- **CPU** : 20-60% pendant génération

## 💡 **Conseils d'Utilisation**

1. **Soyez naturel** : "je veux faire du seuil" fonctionne parfaitement
2. **Précisez les durées** : "10 min échauffement, 3x5min seuil"
3. **Utilisez vos mots** : "à fond", "récup", "pose" sont compris
4. **Structures complexes** : Les blocs imbriqués sont supportés

---

🚴‍♂️ **Votre Mac M3 est maintenant un coach cycliste intelligent !**

*Générez des entraînements professionnels en langage naturel, localement et en privé.*
