# 🚴 Vekta V2 - Intelligence Architecture

**Post-Interview Branch** - Architecture intelligente avec LLM open source

## 🏗️ Architecture

```
Query → Extraction Entités Flexible → LLM Génération → Validation Stricte → RAG Correction
```

## 🧠 LLM Integration

- **API**: Hugging Face Inference API
- **Model**: Llama-3.1-8B-Instruct
- **Usage**: Extraction d'entités + génération structure

## 🚀 Quick Start

```bash
cd vekta
python launch_vekta.py
```

## 📊 Performance Target

- **Coverage**: 90%+ des queries Vekta
- **Precision**: Validation ultra-stricte
- **Flexibility**: Ordre libre des entités
