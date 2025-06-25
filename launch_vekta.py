#!/usr/bin/env python3
"""
🚀 Lanceur Vekta - Application de Génération de Séances Cyclistes
Reproduction Fidèle du Pipeline Production

Usage:
    python launch_vekta.py
    
L'application sera disponible sur:
- API: http://localhost:8000
- Interface: http://localhost:8501
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_requirements():
    """Vérifie que les dépendances sont installées"""
    try:
        import fastapi
        import streamlit
        import uvicorn
        print("✅ Dépendances vérifiées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Installez avec: pip install -r requirements.txt")
        return False

def start_api():
    """Démarre l'API FastAPI"""
    print("🚀 Démarrage de l'API Vekta...")
    
    # Définir PYTHONPATH pour les imports
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).parent)
    
    # Lancer uvicorn
    api_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "api.vekta_api:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--reload"
    ], env=env)
    
    return api_process

def start_streamlit():
    """Démarre l'interface Streamlit"""
    print("🎨 Démarrage de l'interface Streamlit...")
    
    # Définir PYTHONPATH pour les imports
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).parent)
    
    # Lancer streamlit
    streamlit_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run",
        "frontend/vekta_app.py",
        "--server.port", "8501",
        "--server.address", "127.0.0.1"
    ], env=env)
    
    return streamlit_process

def main():
    """Fonction principale de lancement"""
    print("🚴 VEKTA - AI-powered Session Generator")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_requirements():
        sys.exit(1)
    
    try:
        # Démarrage des services
        api_process = start_api()
        time.sleep(3)  # Attendre que l'API démarre
        
        streamlit_process = start_streamlit()
        time.sleep(2)  # Attendre que Streamlit démarre
        
        print("\n🎉 APPLICATION DÉMARRÉE !")
        print("-" * 30)
        print("📡 API FastAPI:     http://localhost:8000")
        print("🌐 Interface:       http://localhost:8501")
        print("📚 Documentation:   http://localhost:8000/docs")
        print("-" * 30)
        print("\n⏹️  Appuyez sur Ctrl+C pour arrêter")
        
        # Attendre l'interruption
        try:
            api_process.wait()
        except KeyboardInterrupt:
            print("\n🔄 Arrêt en cours...")
            
            # Arrêt propre des processus
            api_process.terminate()
            streamlit_process.terminate()
            
            # Attendre la fermeture
            api_process.wait(timeout=5)
            streamlit_process.wait(timeout=5)
            
            print("✅ Application arrêtée proprement")
            
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 