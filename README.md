# 🚴‍♂️ Vekta - Pipeline de Génération d'Entraînements Cyclistes

## 📋 Description

Pipeline intelligent de génération d'entraînements cyclistes qui transforme des descriptions textuelles en fichiers .zwo structurés et compatibles avec Zwift/TrainerRoad.

## 🎯 Fonctionnalités Clés

- **Validation intelligente** avec seuils de confiance renforcés (≥0.95)
- **Génération XML réelle** de fichiers .zwo utilisables
- **Vérification de fidélité absolue** corpus → XML
- **Messages d'erreur précis** avec entités manquantes
- **Corpus complet** de 150+ entraînements cyclistes

## 📚 Structure du Projet

```
Vekta/
├── Demo_Pipeline_Ameliore.ipynb     # Notebook de démonstration principal
├── Tests_Pipeline_Vekta.ipynb       # Suite de tests automatisés
├── Plan_Technique_Vekta.md          # Documentation technique
├── workouts_demo/                   # Fichiers .zwo générés
└── README.md                        # Ce fichier
```

## 🚀 Utilisation Rapide

```python
# Chargement du pipeline
from Demo_Pipeline_Ameliore import demonstrate_enhanced_pipeline

# Test d'une requête
demonstrate_enhanced_pipeline("3x 10 min tempo avec 5min récup")
```

## 🎯 Seuils de Confiance

- **≥0.95** : Génération directe (excellence requise)
- **≥0.75** : Génération avec avertissement
- **<0.75** : Rejet complet avec suggestions

## 📊 Performance

- **Fidélité** : 100% corpus → XML
- **Précision** : 100% sur requêtes validées
- **Couverture** : 10 zones d'entraînement complètes
- **Robustesse** : 150+ variations linguistiques

## 🔧 Développement

### Prérequis
- Python 3.8+
- Jupyter Notebook
- pandas, xml.etree.ElementTree

### Installation
```bash
git clone https://github.com/victorabsil/vekta.git
cd vekta
pip install -r requirements.txt
```

## 📈 Versions

- **v1.0** : Pipeline de base avec corpus simple
- **v2.0** : Corpus étendu + seuils renforcés
- **v2.1** : Améliorations messages d'erreur (en cours)

## 🤝 Contribution

Ce projet est développé dans le cadre d'un entretien technique pour Vekta.

## 📄 License

Propriétaire - Vekta Training Systems 