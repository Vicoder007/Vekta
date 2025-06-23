# 🎯 Guide de Présentation - Entretien Vekta

## 📋 Présentation du Projet (5 min)

### Contexte
- **Problème** : Génération automatique de séances d'entraînement cycliste
- **Défi** : Traiter le langage naturel français familier avec fautes
- **Solution** : Pipeline RAG + Correction orthographique + Interface moderne

### Démonstration Live
1. **Notebook Simple** : `Demo-Interview.ipynb`
   - Correction orthographique spécialisée
   - Recherche sémantique dans corpus
   - Pipeline RAG complet
   - Génération de fichiers .zwo

2. **Application Complète** : `vekta/`
   - Interface Streamlit moderne
   - API FastAPI performante
   - Export Zwift compatible

## 🎯 Points Clés à Mettre en Avant

### 1. Innovation Technique
```python
# Exemple emblématique
Input:  "je doie faire dix minut de chaude, apres 3 set de 5 mn a fond"
→ 13 corrections automatiques
→ Séance validée (56% confiance)
→ Fichier .zwo généré
```

### 2. Performance
- **Temps de traitement** : < 10ms
- **Taux de succès** : 80% sur requêtes variées
- **Scores variables** : 56% (familier) à 100% (parfait)

### 3. Architecture Modulaire
- **Components** : Pipeline RAG réutilisable
- **API** : FastAPI avec documentation automatique
- **Frontend** : Interface utilisateur intuitive
- **Tests** : Suite de tests automatisés

## 🚀 Démonstration Recommandée

### Étape 1 : Notebook (3 min)
```bash
jupyter notebook Demo-Interview.ipynb
```
- Montrer la correction orthographique
- Expliquer la recherche sémantique
- Démontrer le pipeline complet

### Étape 2 : Application (2 min)
```bash
cd vekta
python start_vekta.py
```
- Interface sur http://localhost:8501
- Saisir une requête familière
- Montrer les visualisations
- Télécharger le fichier .zwo

## 🧠 Questions Techniques Anticipées

### Q: "Comment gérez-vous les fautes d'orthographe ?"
**R:** Correcteur spécialisé cyclisme avec :
- Dictionnaire familier → technique
- Expressions composées ("cool down" → "retour au calme")
- Corrections contextuelles

### Q: "Comment assurez-vous la qualité des résultats ?"
**R:** Scores de confiance hybrides :
- Similarité sémantique (Jaccard)
- Bonus correction orthographique
- Bonus structure complète
- Seuils de validation (65% minimum)

### Q: "Scalabilité de la solution ?"
**R:** Architecture modulaire :
- API REST stateless
- Components découplés
- Docker ready
- Tests automatisés

## 📊 Métriques à Présenter

| Métrique | Valeur | Impact |
|----------|--------|--------|
| **Corrections automatiques** | 13 types | Traite langage familier |
| **Temps de réponse** | < 10ms | Temps réel |
| **Taux de succès** | 80% | Fiabilité élevée |
| **Formats export** | .zwo | Compatibilité Zwift |

## 🎨 Points Différenciants

### 1. Spécialisation Cyclisme
- Vocabulaire technique spécialisé
- Zones de puissance (7 zones)
- Compatibilité Zwift native

### 2. Robustesse Linguistique
- Langage familier accepté
- Fautes d'orthographe corrigées
- Expressions composées gérées

### 3. Interface Moderne
- Visualisations Plotly interactives
- Métriques temps réel
- Export direct fichiers

## 🔧 Structure de Code

```
Vekta/
├── 📓 Demo-Interview.ipynb     # Démo simple pour entretien
├── 🚀 vekta/                   # Projet complet production
│   ├── api/                    # Backend FastAPI
│   ├── frontend/               # Interface Streamlit  
│   ├── components/             # Pipeline RAG
│   └── docs/                   # Documentation
├── 🧪 examples/                # Tests et exemples
└── 📊 research/                # Notebooks recherche
```

## 💡 Messages Clés

1. **"Pipeline RAG spécialisé"** - Pas juste de la génération de texte
2. **"Correction orthographique contextuelle"** - Comprend le domaine
3. **"Scores de confiance variables"** - Pas de réponse binaire
4. **"Architecture production-ready"** - API + Tests + Docker
5. **"Interface utilisateur moderne"** - Pas juste un script

## ⏰ Timing Recommandé

- **0-2 min** : Contexte et problématique
- **2-5 min** : Démonstration notebook
- **5-7 min** : Application complète
- **7-10 min** : Questions techniques

## 🎯 Objectif Final

Montrer une solution **complète** et **professionnelle** qui :
- Résout un problème réel
- Utilise des techniques IA appropriées
- Fournit une expérience utilisateur moderne
- Est prête pour la production 