#!/bin/bash

# Script d'installation Ollama optimisé pour Mac M3
# Ce script installe Ollama et configure le modèle optimal pour votre Mac

echo "🚀 Installation Ollama pour Mac M3"
echo "=================================="

# Fonction pour vérifier si une commande existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Vérifier si Ollama est déjà installé
if command_exists ollama; then
    echo "✅ Ollama est déjà installé"
    ollama --version
else
    echo "📥 Installation d'Ollama..."
    
    # Installation via Homebrew (recommandé pour Mac)
    if command_exists brew; then
        echo "🍺 Installation via Homebrew..."
        brew install ollama
    else
        echo "🔧 Installation via script officiel..."
        curl -fsSL https://ollama.ai/install.sh | sh
    fi
    
    echo "✅ Ollama installé avec succès"
fi

echo ""
echo "🧠 Configuration du modèle optimal pour Mac M3..."

# Démarrer Ollama en arrière-plan si pas déjà en cours
if ! pgrep -f "ollama serve" > /dev/null; then
    echo "⚡ Démarrage d'Ollama..."
    ollama serve &
    OLLAMA_PID=$!
    echo "Ollama PID: $OLLAMA_PID"
    
    # Attendre que Ollama soit prêt
    echo "⏳ Attente du démarrage d'Ollama..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            echo "✅ Ollama est prêt"
            break
        fi
        sleep 1
        echo -n "."
    done
    echo ""
else
    echo "✅ Ollama est déjà en cours d'exécution"
fi

# Télécharger le modèle optimal pour Mac M3
echo "📥 Téléchargement du modèle llama3.2:3b (optimal pour Mac M3)..."
echo "💡 Ce modèle a 3 milliards de paramètres, parfait pour votre Mac M3"
echo "⏳ Téléchargement en cours... (peut prendre 5-10 minutes)"

ollama pull llama3.2:3b

if [ $? -eq 0 ]; then
    echo "✅ Modèle llama3.2:3b téléchargé avec succès"
else
    echo "❌ Erreur lors du téléchargement du modèle"
    exit 1
fi

echo ""
echo "🧪 Test du modèle..."
echo "Bonjour, peux-tu générer un entraînement cycliste simple?" | ollama run llama3.2:3b --verbose

echo ""
echo "🎉 Configuration terminée!"
echo "💡 Votre Mac M3 est maintenant configuré avec:"
echo "   - Ollama installé et configuré"
echo "   - Modèle llama3.2:3b (3B paramètres, optimal pour M3)"
echo "   - Prêt pour Vekta V2"

echo ""
echo "🚴‍♂️ Vous pouvez maintenant lancer Vekta avec:"
echo "   python3 launch_vekta_v2.py" 