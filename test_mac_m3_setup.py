#!/usr/bin/env python3
"""
Test de Configuration Mac M3 pour Vekta V2
Vérifie que tout est correctement configuré pour votre Mac M3
"""

import subprocess
import requests
import time
import sys
import os

def test_ollama_installation():
    """Test de l'installation Ollama"""
    print("🔍 Test d'installation Ollama...")
    
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installé: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama non installé")
            return False
    except FileNotFoundError:
        print("❌ Ollama non trouvé dans PATH")
        return False

def test_ollama_service():
    """Test du service Ollama"""
    print("🔍 Test du service Ollama...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Service Ollama actif")
            return True
        else:
            print(f"❌ Service Ollama inactif (code: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Service Ollama non accessible: {e}")
        return False

def test_model_availability():
    """Test de la disponibilité du modèle Mac M3"""
    print("🔍 Test du modèle llama3.2:3b...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]
            
            for name in model_names:
                if "llama3.2:3b" in name:
                    print(f"✅ Modèle Mac M3 disponible: {name}")
                    return True
            
            print("❌ Modèle llama3.2:3b non trouvé")
            print("💡 Modèles disponibles:")
            for name in model_names:
                print(f"   - {name}")
            return False
    except Exception as e:
        print(f"❌ Impossible de vérifier les modèles: {e}")
        return False

def test_model_performance():
    """Test de performance du modèle"""
    print("🔍 Test de performance du modèle...")
    
    test_prompt = "Génère un échauffement cycliste de 10 minutes."
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": test_prompt,
                "stream": False,
                "options": {
                    "num_predict": 100,
                    "temperature": 0.1
                }
            },
            timeout=30
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            response_time = end_time - start_time
            result = response.json().get("response", "")
            
            print(f"✅ Test de performance réussi")
            print(f"   ⏱️  Temps de réponse: {response_time:.2f}s")
            print(f"   📝 Réponse (extrait): {result[:100]}...")
            
            if response_time < 10:
                print("   🚀 Performance excellente pour Mac M3")
            elif response_time < 20:
                print("   👍 Performance correcte pour Mac M3")
            else:
                print("   ⚠️  Performance lente - vérifiez la mémoire disponible")
            
            return True
        else:
            print(f"❌ Test échoué (code: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Test de performance échoué: {e}")
        return False

def test_system_resources():
    """Test des ressources système"""
    print("🔍 Test des ressources système...")
    
    try:
        import psutil
        
        # Mémoire
        memory = psutil.virtual_memory()
        available_gb = memory.available / (1024**3)
        total_gb = memory.total / (1024**3)
        
        print(f"   💾 Mémoire: {available_gb:.1f}GB libre / {total_gb:.1f}GB total")
        
        if available_gb >= 8:
            print("   ✅ Mémoire excellente pour llama3.2:3b")
        elif available_gb >= 4:
            print("   ✅ Mémoire suffisante pour llama3.2:3b")
        else:
            print("   ⚠️  Mémoire faible - performances réduites possibles")
        
        # CPU
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        print(f"   🔢 CPU: {cpu_count} cœurs, utilisation: {cpu_percent}%")
        
        if cpu_count >= 8:
            print("   ✅ CPU excellent pour Mac M3")
        elif cpu_count >= 4:
            print("   ✅ CPU suffisant")
        else:
            print("   ⚠️  CPU limité")
        
        return True
        
    except ImportError:
        print("   ⚠️  psutil non installé - impossible de vérifier les ressources")
        return True
    except Exception as e:
        print(f"   ❌ Erreur lors de la vérification: {e}")
        return True

def test_dependencies():
    """Test des dépendances Python"""
    print("🔍 Test des dépendances Python...")
    
    required_packages = [
        'streamlit',
        'requests',
        'plotly',
        'pandas',
        'psutil'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MANQUANT")
            missing.append(package)
    
    if missing:
        print(f"💡 Installez les packages manquants: pip install {' '.join(missing)}")
        return False
    
    return True

def main():
    """Exécute tous les tests"""
    print("🧪 TEST DE CONFIGURATION MAC M3 POUR VEKTA V2")
    print("=" * 50)
    
    tests = [
        ("Installation Ollama", test_ollama_installation),
        ("Service Ollama", test_ollama_service),
        ("Modèle Mac M3", test_model_availability),
        ("Performance", test_model_performance),
        ("Ressources Système", test_system_resources),
        ("Dépendances Python", test_dependencies)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Score: {passed}/{total} tests passés")
    
    if passed == total:
        print("\n🎉 Configuration Mac M3 parfaite !")
        print("🚴‍♂️ Vekta V2 est prêt à l'emploi")
        print("\n💡 Lancez l'application avec: python3 launch_vekta_v2.py")
    elif passed >= total - 1:
        print("\n👍 Configuration Mac M3 très bonne")
        print("⚠️  Un test mineur a échoué, mais Vekta V2 devrait fonctionner")
    else:
        print("\n⚠️  Configuration incomplète")
        print("🔧 Veuillez corriger les erreurs avant d'utiliser Vekta V2")
        
        if not any(result for name, result in results if "Ollama" in name):
            print("\n💡 Solution recommandée:")
            print("   ./install_ollama_mac.sh")

if __name__ == "__main__":
    main() 