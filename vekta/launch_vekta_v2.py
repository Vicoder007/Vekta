#!/usr/bin/env python3
"""
Lanceur Vekta V2 - Intelligence Architecture
Architecture LLM + Validation Stricte + RAG
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Vérification des dépendances V2"""
    print("🔍 Vérification des dépendances V2...")
    
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
        print("📦 Installation avec: pip install -r requirements_v2.txt")
        
        install = input("Installer maintenant? (y/N): ").lower().strip()
        if install == 'y':
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_v2.txt'])
        else:
            sys.exit(1)
    
    print("✅ Toutes les dépendances sont installées")

def launch_streamlit_v2():
    """Lance l'interface Streamlit V2"""
    print("🚀 Lancement de Vekta V2 Intelligence...")
    
    # Vérifier que le fichier existe
    app_file = Path('frontend/vekta_app_intelligent.py')
    if not app_file.exists():
        print(f"❌ Fichier non trouvé: {app_file}")
        sys.exit(1)
    
    # Lancer Streamlit
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        str(app_file),
        '--server.port', '8502',  # Port différent pour V2
        '--server.address', '127.0.0.1'
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt de Vekta V2")

def main():
    """Point d'entrée principal"""
    print("🧠 VEKTA V2 - Intelligence Architecture")
    print("=" * 50)
    
    # Changer vers le répertoire du script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        check_dependencies()
        print()
        launch_streamlit_v2()
        
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
