#!/usr/bin/env python3
"""
Lanceur Vekta V2 - Intelligence Architecture avec Auto-Démarrage Ollama
Architecture LLM + Validation Stricte + Auto-Configuration Ollama
"""

import subprocess
import sys
import os
import time
import signal
import threading
import requests
from pathlib import Path

# Variables globales pour les processus
ollama_process = None
streamlit_process = None

def check_ollama_installed():
    """Vérifie si Ollama est installé"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama est installé")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama n'est pas installé")
    print("📥 Veuillez installer Ollama depuis : https://ollama.ai")
    return False

def check_ollama_running():
    """Vérifie si Ollama est déjà en cours d'exécution"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama est déjà en cours d'exécution")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print("🔄 Ollama n'est pas en cours d'exécution")
    return False

def start_ollama():
    """Démarre Ollama en arrière-plan"""
    global ollama_process
    
    print("🚀 Démarrage d'Ollama...")
    
    try:
        # Démarrer Ollama en arrière-plan avec optimisations Mac M3
        env = os.environ.copy()
        env['OLLAMA_MODELS'] = os.path.expanduser('~/.ollama/models')
        env['OLLAMA_HOST'] = 'localhost:11434'
        env['OLLAMA_KEEP_ALIVE'] = '5m'  # Garde le modèle en mémoire 5 minutes
        env['OLLAMA_NUM_PARALLEL'] = '1'  # Une seule requête à la fois pour économiser la mémoire
        
        ollama_process = subprocess.Popen(
            ['ollama', 'serve'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Attendre que Ollama soit prêt (max 30 secondes)
        for i in range(30):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    print("✅ Ollama démarré avec succès")
                    return True
            except requests.exceptions.RequestException:
                pass
            
            print(f"⏳ Attente d'Ollama... ({i+1}/30)")
            time.sleep(1)
        
        print("❌ Timeout: Ollama n'a pas pu démarrer")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage d'Ollama: {e}")
        return False

def pull_optimal_model():
    """Télécharge le modèle optimal pour Mac M3"""
    optimal_model = "llama3.2:3b"
    
    print(f"🧠 Vérification du modèle optimal: {optimal_model}")
    
    try:
        # Vérifier si le modèle est déjà disponible
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            if any(optimal_model in name for name in model_names):
                print(f"✅ Modèle {optimal_model} déjà disponible")
                return True
        
        # Télécharger le modèle
        print(f"📥 Téléchargement du modèle {optimal_model}...")
        print("💡 Ce modèle est optimisé pour Mac M3 (3B paramètres)")
        print("⏳ Téléchargement en cours... (peut prendre quelques minutes)")
        
        pull_result = subprocess.run(
            ['ollama', 'pull', optimal_model],
            capture_output=True,
            text=True,
            timeout=600  # 10 minutes max
        )
        
        if pull_result.returncode == 0:
            print(f"✅ Modèle {optimal_model} téléchargé avec succès")
            return True
        else:
            print(f"❌ Erreur lors du téléchargement: {pull_result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors du téléchargement")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def setup_ollama():
    """Configuration d'Ollama avec modèle optimal pour Mac M3"""
    print("🧠 === CONFIGURATION OLLAMA POUR MAC M3 ===")
    
    # 1. Vérifier l'installation
    if not check_ollama_installed():
        return False
    
    # 2. Vérifier si déjà en cours
    if not check_ollama_running():
        # 3. Démarrer Ollama
        if not start_ollama():
            return False
    
    # 4. Télécharger le modèle optimal
    if not pull_optimal_model():
        print("⚠️  Impossible de télécharger le modèle optimal")
        print("💡 L'application fonctionnera, mais le modèle sera téléchargé au premier usage")
    
    print("✅ Ollama configuré et prêt avec modèle Mac M3")
    return True

def check_dependencies():
    """Vérification des dépendances V2"""
    print("🔍 Vérification des dépendances Python...")
    
    required_packages = [
        'streamlit',
        'requests', 
        'plotly',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("📦 Installation avec: pip install -r requirements.txt")
        
        install = input("Installer maintenant? (y/N): ").lower().strip()
        if install == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        else:
            sys.exit(1)
    
    print("✅ Toutes les dépendances Python sont installées")

def launch_streamlit_v2():
    """Lance l'interface Streamlit V2"""
    global streamlit_process
    
    print("🚀 Lancement de l'interface Vekta V2...")
    
    # Vérifier que le fichier existe
    app_file = Path('frontend/vekta_app_simple.py')
    if not app_file.exists():
        print(f"❌ Fichier non trouvé: {app_file}")
        sys.exit(1)
    
    # Lancer Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        str(app_file),
        '--server.port', '8502',
        '--server.address', '127.0.0.1'
    ]
    
    try:
        print("🌐 Interface disponible sur: http://localhost:8502")
        streamlit_process = subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt de Vekta V2")

def cleanup_processes():
    """Nettoie les processus avant de quitter"""
    global ollama_process, streamlit_process
    
    print("\n🧹 Nettoyage des processus...")
    
    if streamlit_process and streamlit_process.poll() is None:
        print("⏹️  Arrêt de Streamlit...")
        streamlit_process.terminate()
    
    if ollama_process and ollama_process.poll() is None:
        print("⏹️  Arrêt d'Ollama...")
        ollama_process.terminate()
        try:
            ollama_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            ollama_process.kill()

def signal_handler(signum, frame):
    """Gestionnaire de signaux pour un arrêt propre"""
    cleanup_processes()
    sys.exit(0)

def check_system_resources():
    """Vérifie les ressources système pour Mac M3"""
    print("🖥️  Vérification des ressources système...")
    
    try:
        import psutil
        
        # Vérifier la mémoire disponible
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        
        print(f"   💾 Mémoire disponible: {available_gb:.1f} GB")
        
        if available_gb < 4:
            print("   ⚠️  Attention: Mémoire faible (<4GB). Le modèle pourrait être lent.")
        elif available_gb >= 8:
            print("   ✅ Mémoire suffisante pour une performance optimale")
        else:
            print("   ✅ Mémoire correcte pour le modèle llama3.2:3b")
            
        # Vérifier le processeur
        cpu_count = psutil.cpu_count()
        print(f"   🔢 Cœurs CPU: {cpu_count}")
        
        if cpu_count >= 8:
            print("   ✅ Processeur performant détecté (optimal pour M3)")
        
        return True
        
    except ImportError:
        print("   💡 Package psutil non disponible (optionnel)")
        return True
    except Exception as e:
        print(f"   ⚠️  Impossible de vérifier les ressources: {e}")
        return True

def main():
    """Point d'entrée principal"""
    print("🧠 VEKTA V2 - Intelligence Architecture pour Mac M3")
    print("=" * 60)
    
    # Configurer les gestionnaires de signaux
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Changer vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        # 1. Vérifier les ressources système
        check_system_resources()
        print()
        
        # 2. Vérifier les dépendances Python
        check_dependencies()
        print()
        
        # 3. Configurer Ollama (installation + démarrage)
        if not setup_ollama():
            print("❌ Impossible de configurer Ollama")
            sys.exit(1)
        print()
        
        # 4. Lancer Streamlit
        launch_streamlit_v2()
        
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
    finally:
        cleanup_processes()

if __name__ == "__main__":
    main()
