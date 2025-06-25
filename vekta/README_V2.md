# 🧠 Vekta V2 - Intelligence Architecture

## 🎯 Objectif

Architecture révolutionnaire combinant **LLM open source** + **validation stricte** + **correction RAG** pour une compréhension flexible et une génération précise d'entraînements cyclistes.

## 🏗️ Pipeline Intelligent

```
Query Libre → LLM Entity Extraction → Smart Generation → Ultra-Strict Validation → RAG Correction
```

### 1️⃣ LLM Entity Extraction (Hugging Face)

- **Model**: Llama-3.1-8B-Instruct
- **Capability**: Ordre libre des entités
- **Examples**:
  - `"5 minutes tempo"` = `"tempo 5 minutes"` = même résultat
  - `"2x3x5 minutes tempo"` → structure nested automatique

### 2️⃣ Smart Generation

- **Structures complexes**: 2x3x5 = 2 blocs × (3 séries × 5min)
- **Séances simples**: parsing direct
- **Phases auto**: échauffement/cooldown détectés
- **Intensités intelligentes**: mapping type → zone → %

### 3️⃣ Ultra-Strict Validation

- **Durées exactes**: 55min demandées = 55min générées
- **Intensités précises**: ±5% tolérance maximum
- **Structures conformes**: validation logique complète
- **Types préservés**: tous les workout_types dans l'output

### 4️⃣ RAG Correction

- **Corpus intelligent**: base de séances validées
- **Correction automatique**: si validation échoue
- **Apprentissage continu**: amélioration progressive

## 🚀 Installation & Usage

### Quick Start

```bash
cd vekta
python launch_vekta_v2.py
```

### Configuration Hugging Face

1. **Créer compte**: https://huggingface.co/
2. **Générer token**: https://huggingface.co/settings/tokens
3. **Configuration**:
   ```bash
   cp .env.example .env
   # Éditer .env avec votre token
   ```

### Mode Fallback

Sans token HF, mode fallback regex automatique activé.

## 📊 Formats Supportés

### ✅ Séances Simples
- `"5 minutes tempo"`
- `"tempo 5 minutes"`
- `"aerobic 10min"`

### ✅ Structures Répétitives
- `"5x3min à 95%"`
- `"4 fois 5 minutes seuil"`
- `"8x30sec vo2max"`

### ✅ Structures Imbriquées
- `"2x3x5 minutes tempo"` → 2 blocs de (3×5min)
- `"3x(4x2min) à 95%"` → 3 blocs de (4×2min)

### ✅ Séances Complètes
- `"10min échauffement puis 5x5min seuil puis 10min retour"`
- `"2min aerobic warmup then 2x3x5min tempo"`

## 🎯 Performance Targets

- **Coverage**: 90%+ des queries Vekta
- **Precision**: <5% erreur sur métriques
- **Speed**: <2s LLM + génération
- **Flexibility**: Ordre libre total

## 🔧 Architecture Technique

### LLM Integration
```python
from llm_parser import IntelligentWorkoutParser

parser = IntelligentWorkoutParser(hf_token="your_token")
entities = parser.extract_entities("5 minutes tempo")
workout = parser.generate_workout_structure(entities)
```

### Validation Pipeline
```python
is_valid, errors = parser.validate_structure_strict(
    workout_steps, entities, original_query
)
```

### Frontend Intelligent
- **Interface épurée**: focus sur le parsing
- **Visualisation intelligente**: graphiques adaptatifs
- **Métriques temps réel**: extraction + génération + validation

## 🌟 Avantages V2

1. **Flexibilité maximale**: ordre libre complet
2. **Précision garantie**: validation ultra-stricte
3. **Performance optimale**: LLM externe rapide
4. **Évolutivité**: RAG correction continue
5. **Simplicité**: une seule interface propre

## 🚧 Roadmap

- [ ] **RAG Corpus**: base de 1000+ séances validées
- [ ] **Multi-langues**: français + anglais + espagnol
- [ ] **API REST**: endpoints pour intégration
- [ ] **Batch processing**: traitement massif
- [ ] **Learning loop**: amélioration auto des prompts

## 💡 Exemples d'Usage

### Query Simple
```
Input:  "55 minutes tempo"
Output: 1 étape × 55min @ 82% FTP (Zone 3)
```

### Query Complexe
```
Input:  "2 minutes échauffement aerobic puis 2x3x5 minutes tempo"
Output: 
- Échauffement 2min @ 70% (Zone 2)
- Bloc 1: 3×5min @ 82% + récup 2min
- Bloc 2: 3×5min @ 82% + récup 2min
```

### Query avec Intensité
```
Input:  "5x3min à 95% avec 2min récup"
Output: 5×(3min @ 95% + 2min @ 50%)
```

---

🧠 **Vekta V2** - L'intelligence au service de la performance cycliste
