# 🚴 Guide Utilisateur Vekta

**Générateur de séances d'entraînement cycliste alimenté par l'IA**

## 🚀 Démarrage en 3 étapes

### 1. Installation
```bash
# Cloner le projet
git clone <votre-repo>
cd Vekta

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement
```bash
# Démarrage automatique (recommandé)
python start_vekta.py

# OU démarrage manuel
# Terminal 1: uvicorn vekta_api:app --reload
# Terminal 2: streamlit run vekta_app.py
```

### 3. Utilisation
1. **Ouvrez votre navigateur** : http://localhost:8501
2. **Décrivez votre séance** en français naturel
3. **Cliquez sur "Générer"** et téléchargez votre fichier .zwo

---

## 💬 Comment décrire votre séance

### ✅ Exemples qui fonctionnent parfaitement

**Français standard :**
```
10 minutes d'échauffement puis 3 séries de 5 minutes à fond avec 2 minutes de repos entre séries puis 10 minutes de retour au calme
```

**Français familier :**
```
je doie faire dix minut de chaude, apres 3 set de 5 mn a fond et 2 min pose entre set. fini avk 10 min cool down facile
```

**Séances complexes :**
```
15min échauffement progressif puis pyramide 1-2-3-4-3-2-1 minutes à 95% FTP avec 1min récup entre puis 10min retour calme
```

### 🎯 Mots-clés reconnus

| Type | Mots-clés |
|------|-----------|
| **Échauffement** | échauffement, chaude, warm up |
| **Intensité** | à fond, max, seuil, tempo, endurance |
| **Récupération** | repos, récup, pause, pose |
| **Retour au calme** | retour au calme, cool down, facile |
| **Séries** | séries, set, répétitions, fois |
| **Structures** | pyramide, over-under, intervals |

---

## 🎨 Interface Vekta

### Onglet Principal (Main)
- **Zone de saisie** : Décrivez votre séance
- **Configuration** : Auteur, durée, puissance critique
- **Zones de puissance** : Calcul automatique des 7 zones
- **Bouton de génération** : Lance la création de votre séance

### Résultats après génération
- **Métriques** : Durée, puissance moyenne, calories, training stimulus
- **Graphique** : Profil de puissance avec zones colorées
- **Structure** : Étapes détaillées de votre séance
- **Téléchargement** : Fichier .zwo compatible Zwift

### Onglet Options
- **Paramètres avancés** : Seuils de confiance, corrections
- **Statistiques API** : Performances du système
- **Test de connectivité** : Vérification du bon fonctionnement

---

## 🔧 Personnalisation

### Zones de Puissance
1. **Ajustez votre Critical Power** (puissance critique)
2. **Les 7 zones se calculent automatiquement** :
   - Zone 1 : < 55% (Récupération)
   - Zone 2 : 55-75% (Endurance)
   - Zone 3 : 75-90% (Tempo)
   - Zone 4 : 90-105% (Seuil)
   - Zone 5 : 105-120% (VO2 Max)
   - Zone 6 : 120-150% (Anaérobie)
   - Zone 7 : > 150% (Neuromusculaire)

### Paramètres Avancés
- **Seuil de confiance** : Ajustez la sensibilité de validation
- **Correction orthographique** : Activez/désactivez la correction automatique
- **Durée par défaut** : Configurez la durée standard de vos séances

---

## 📱 Utilisation Mobile

L'interface Vekta est **responsive** et fonctionne parfaitement sur :
- 📱 **Smartphones** : Interface adaptée tactile
- 📲 **Tablettes** : Expérience optimisée
- 💻 **Ordinateurs** : Interface complète

---

## 🎯 Cas d'Usage Typiques

### 🏃‍♂️ Entraînement Débutant
```
20 minutes facile puis 5 fois 2 minutes un peu plus fort avec 1 minute de repos puis 10 minutes facile
```

### 🚴‍♀️ Séance Seuil
```
15min échauffement puis 2x20min à 95% FTP avec 5min récup puis 10min retour calme
```

### 🏋️‍♂️ Travail de Force
```
échauffement 15min puis 6x30sec à 120% FTP avec 2min30 récup puis retour calme 15min
```

### 🎪 Séance Ludique
```
10min chaude puis pyramide 1-2-3-4-5-4-3-2-1 minutes à fond avec 1min pose entre puis cool down
```

---

## ❓ Dépannage Rapide

### Interface ne s'ouvre pas
```bash
# Vérifier que les services tournent
curl http://localhost:8501
curl http://localhost:8000/health

# Redémarrer si nécessaire
python start_vekta.py
```

### Erreur "API non disponible"
```bash
# Vérifier l'API
curl http://localhost:8000/health

# Redémarrer l'API
uvicorn vekta_api:app --reload
```

### Séance non générée
1. **Vérifiez la confiance** : Score > 70% recommandé
2. **Reformulez votre requête** : Utilisez les mots-clés reconnus
3. **Consultez les suggestions** : Affichées en cas d'échec

---

## 🏆 Conseils d'Expert

### ✨ Pour de meilleurs résultats
- **Soyez précis** sur les durées et intensités
- **Mentionnez l'échauffement et le retour au calme**
- **Utilisez des termes cyclistes** : FTP, seuil, tempo, etc.
- **Structurez votre demande** : échauffement → travail → récupération

### 🎨 Personnalisation avancée
- **Ajustez votre FTP** pour des zones précises
- **Modifiez les seuils** selon votre niveau
- **Sauvegardez vos séances** favorites (fichiers .zwo)

### 📊 Suivi de progression
- **Consultez les métriques** : TSS, calories, durée
- **Analysez le profil** : Répartition des zones
- **Exportez vers Zwift** : Entraînement structuré

---

## 🚀 Prêt à rouler ?

1. **Lancez Vekta** : `python start_vekta.py`
2. **Ouvrez votre navigateur** : http://localhost:8501
3. **Décrivez votre séance** en français naturel
4. **Pédalez avec votre séance générée** ! 🚴‍♂️

---

*Développé avec ❤️ pour la communauté cycliste française* 