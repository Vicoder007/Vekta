# 🚀 Vekta - Pipeline de Génération d'Entraînements Cyclistes

## 📋 Description
Pipeline intelligent de génération d'entraînements cyclistes transformant des descriptions textuelles en fichiers .zwo structurés avec validation de fidélité absolue.

## 🎯 Fonctionnalités Clés
- **Validation intelligente** avec seuils de confiance renforcés (≥0.95)
- **Génération XML réelle** de fichiers .zwo compatibles Zwift/TrainerRoad
- **Vérification de fidélité absolue** corpus → XML (100%)
- **Messages d'erreur précis** avec entités manquantes détaillées
- **Corpus complet** 150+ entraînements couvrant toutes les zones

## 📁 Structure du Projet
```
Vekta/
├── Demo_Pipeline_Ameliore.ipynb    # Démonstration live du pipeline
├── Tests_Pipeline_Vekta.ipynb      # Suite de tests automatisés
├── Core.ipynb                      # Notebook de base (historique)
├── Plan_Technique_Vekta.md         # Documentation technique
├── workouts_demo/                  # Fichiers .zwo générés
└── test_workouts/                  # Fichiers de test
```

## 🧪 Tests de Validation
- ✅ Confiance élevée (≥0.95): Génération directe
- ⚠️ Confiance modérée (≥0.75): Génération avec avertissement  
- ❌ Confiance faible (<0.75): Rejet avec suggestions

## 🚀 Utilisation
```python
# Exemple d'utilisation
demonstrate_enhanced_pipeline("3x 10 min tempo avec 5min récup")
# → Génère un fichier .zwo avec fidélité 100%
```

## 📊 Métriques de Performance
- **Précision**: 100% (générations validées)
- **Fidélité**: 100% (correspondance corpus → XML)
- **Couverture**: 10 zones d'entraînement complètes
- **Robustesse**: 120+ variations linguistiques

## 🔧 Développement
Voir les branches pour les différentes versions :
- `main`: Version stable
- `feature/enhanced-validation`: Améliorations en cours

---
*Développé pour l'entretien technique Vekta* 