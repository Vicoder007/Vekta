#!/usr/bin/env python3
"""
Script de lancement pour Vekta
Démarre l'API FastAPI et l'interface Streamlit
"""

import subprocess
import sys
import time
import requests
import threading
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def check_api_health():
    """Vérifie si l'API est accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_api():
    """Démarre l'API FastAPI en arrière-plan"""
    console.print("🚀 Démarrage de l'API Vekta...", style="blue")
    
    # Démarrage de l'API
    api_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "vekta_api:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Attendre que l'API soit prête
    console.print("⏳ Attente du démarrage de l'API...", style="yellow")
    for i in range(30):  # Attendre jusqu'à 30 secondes
        if check_api_health():
            console.print("✅ API Vekta démarrée avec succès!", style="green")
            return api_process
        time.sleep(1)
    
    console.print("❌ Impossible de démarrer l'API", style="red")
    api_process.terminate()
    return None

def start_streamlit():
    """Démarre l'interface Streamlit"""
    console.print("🎨 Démarrage de l'interface Streamlit...", style="blue")
    
    streamlit_process = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", 
        "vekta_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--browser.gatherUsageStats", "false"
    ])
    
    return streamlit_process

def main():
    """Fonction principale"""
    console.print(Panel.fit(
        Text("🚴 VEKTA - AI-powered Session Generator", justify="center", style="bold blue"),
        border_style="blue"
    ))
    
    try:
        # Démarrage de l'API
        api_process = start_api()
        if not api_process:
            console.print("❌ Échec du démarrage de l'API", style="red")
            return
        
        # Démarrage de Streamlit
        streamlit_process = start_streamlit()
        
        console.print("\n" + "="*60, style="green")
        console.print("🎉 Vekta est maintenant accessible !", style="bold green")
        console.print("📱 Interface web: http://localhost:8501", style="cyan")
        console.print("🔧 API: http://localhost:8000", style="cyan")
        console.print("📚 Documentation API: http://localhost:8000/docs", style="cyan")
        console.print("="*60 + "\n", style="green")
        
        console.print("💡 Appuyez sur Ctrl+C pour arrêter les services", style="yellow")
        
        # Attendre l'interruption
        try:
            api_process.wait()
        except KeyboardInterrupt:
            console.print("\n🔄 Arrêt des services...", style="yellow")
            
            # Arrêt des processus
            try:
                streamlit_process.terminate()
                api_process.terminate()
                
                # Attendre l'arrêt propre
                streamlit_process.wait(timeout=5)
                api_process.wait(timeout=5)
                
                console.print("✅ Services arrêtés avec succès", style="green")
            except subprocess.TimeoutExpired:
                console.print("⚠️ Arrêt forcé des services", style="yellow")
                streamlit_process.kill()
                api_process.kill()
    
    except Exception as e:
        console.print(f"❌ Erreur: {e}", style="red")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 