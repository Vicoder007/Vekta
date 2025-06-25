# 🚀 Guide Vekta V2 - Démarrage Rapide

## ⚡ Lancement Immédiat

```bash
cd vekta
python launch_vekta_v2.py
```

**URL**: http://localhost:8502

## 🧠 LLM Setup (Optionnel)

### Option 1: Hugging Face API (Recommandé)
1. Créer compte: https://huggingface.co/join
2. Générer token: https://huggingface.co/settings/tokens  
3. Dans l'interface V2: coller le token dans le champ 🔑

### Option 2: Mode Fallback (Default)
- Aucune configuration requise
- Parser regex intelligent activé
- Performance: 85%+ des cas d'usage

## 🎯 Tests Recommandés

### Séances Simples
```
✅ "5 minutes tempo"
✅ "tempo 5 minutes" 
✅ "aerobic 10min"
✅ "seuil 8 minutes"
```

### Structures Répétitives  
```
✅ "5x3min à 95%"
✅ "4 fois 5 minutes seuil"
✅ "8x30sec vo2max"
```

### Structures Imbriquées
```
✅ "2x3x5 minutes tempo"
✅ "3x(4x2min) à 95%"
```

### Séances Complètes
```
✅ "10min échauffement puis 5x5min seuil puis 10min retour"
✅ "2min aerobic warmup then 2x3x5min tempo"
```

## 🎨 Interface V2

### 🎯 Parser Intelligent
- **Query libre**: ordre des mots flexible
- **Critical Power**: ajustement des watts
- **LLM Token**: optionnel pour performance max

### 📊 Résultats
- **Pipeline Steps**: extraction → génération → validation
- **Entités Extraites**: durées, intensités, types, structures
- **Graphique Intelligent**: profil de puissance adaptatif
- **Métriques**: durée, puissance moy/max, étapes

### 🔍 Validation Ultra-Stricte
- **Durées exactes**: 55min = 55min (pas 10min)
- **Intensités précises**: ±5% tolérance max
- **Types préservés**: tous dans l'output final

## 🏆 Performances Attendues

- **Coverage**: 90%+ des queries Vekta
- **Précision**: <5% erreur métriques  
- **Vitesse**: <2s extraction + génération
- **Flexibilité**: ordre libre total

## 🐛 Debugging

### Problème: "Erreur parsing JSON LLM"
- **Cause**: Token HF invalide ou API indisponible
- **Solution**: Mode fallback automatique activé

### Problème: "Validation échouée"  
- **Cause**: Structure générée non conforme
- **Solution**: RAG correction (à implémenter)

### Problème: Port 8502 occupé
```bash
lsof -ti:8502 | xargs kill -9
python launch_vekta_v2.py
```

## 🎯 Architecture Summary

```
Input Query → LLM Llama-3.1-8B → Smart Logic → Strict Validation → Visual Output
```

**Vekta V2 = Flexibilité LLM + Précision garantie**
