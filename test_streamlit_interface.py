#!/usr/bin/env python3
"""
Tests d'intégration pour l'interface Streamlit Vekta
"""

import requests
import time
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def test_api_endpoints():
    """Test des endpoints API utilisés par Streamlit"""
    base_url = "http://localhost:8000"
    
    tests = [
        {
            "name": "Health Check",
            "method": "GET",
            "endpoint": "/health",
            "data": None
        },
        {
            "name": "Validation Standard",
            "method": "POST", 
            "endpoint": "/validate",
            "data": {
                "query": "10min échauffement puis 3 séries de 5min à fond avec 2min repos puis 10min retour au calme",
                "author": "Test Streamlit"
            }
        },
        {
            "name": "Validation Familière",
            "method": "POST",
            "endpoint": "/validate", 
            "data": {
                "query": "je doie faire dix minut de chaude, apres 3 set de 5 mn a fond et 2 min pose entre set",
                "author": "Test Streamlit"
            }
        },
        {
            "name": "Génération Workout",
            "method": "POST",
            "endpoint": "/generate-workout",
            "data": {
                "query": "15min échauffement puis 5x5min à 95% FTP avec 2min récup puis 15min retour calme",
                "author": "Test Streamlit",
                "duration_minutes": 60,
                "critical_power": 250
            }
        },
        {
            "name": "Métriques API",
            "method": "GET",
            "endpoint": "/metrics",
            "data": None
        }
    ]
    
    results = []
    
    for test in tests:
        try:
            start_time = time.time()
            
            if test["method"] == "GET":
                response = requests.get(f"{base_url}{test['endpoint']}", timeout=10)
            else:
                response = requests.post(f"{base_url}{test['endpoint']}", json=test["data"], timeout=10)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            
            results.append({
                "name": test["name"],
                "status": "✅ PASS" if response.status_code == 200 else f"❌ FAIL ({response.status_code})",
                "response_time": f"{response_time:.1f}ms",
                "data": response.json() if response.status_code == 200 else None
            })
            
        except Exception as e:
            results.append({
                "name": test["name"],
                "status": f"❌ ERROR: {str(e)[:50]}...",
                "response_time": "N/A",
                "data": None
            })
    
    return results

def test_streamlit_accessibility():
    """Test de l'accessibilité de l'interface Streamlit"""
    try:
        response = requests.get("http://localhost:8501", timeout=5)
        if response.status_code == 200:
            return "✅ Interface Streamlit accessible"
        else:
            return f"❌ Interface Streamlit inaccessible ({response.status_code})"
    except Exception as e:
        return f"❌ Erreur Streamlit: {str(e)}"

def display_results(api_results, streamlit_status):
    """Affichage des résultats de test"""
    
    # Header
    console.print(Panel.fit(
        "🧪 Tests d'Intégration Vekta Streamlit",
        style="bold blue"
    ))
    
    # Test Streamlit
    console.print(f"\n📱 **Interface Streamlit**: {streamlit_status}")
    
    # Tableau des tests API
    table = Table(title="🔧 Tests API")
    table.add_column("Test", style="cyan", no_wrap=True)
    table.add_column("Statut", style="bold")
    table.add_column("Temps", justify="right")
    table.add_column("Détails", style="dim")
    
    for result in api_results:
        details = ""
        if result["data"]:
            if "confidence" in result["data"]:
                details = f"Confiance: {result['data']['confidence']:.1%}"
            elif "status" in result["data"]:
                details = f"Status: {result['data']['status']}"
            elif "total_requests" in result["data"]:
                details = f"Requêtes: {result['data']['total_requests']}"
        
        table.add_row(
            result["name"],
            result["status"],
            result["response_time"],
            details
        )
    
    console.print(table)
    
    # Statistiques
    passed = sum(1 for r in api_results if "PASS" in r["status"])
    total = len(api_results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    console.print(f"\n📊 **Résultats**: {passed}/{total} tests réussis ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        console.print("🎉 **Interface prête pour utilisation !**", style="bold green")
        console.print("🌐 Accédez à l'interface: http://localhost:8501", style="cyan")
    else:
        console.print("⚠️ **Problèmes détectés**", style="bold yellow")
        console.print("🔧 Vérifiez les logs et redémarrez les services si nécessaire")

def main():
    """Fonction principale"""
    console.print("🔄 Démarrage des tests d'intégration...\n")
    
    # Tests API
    console.print("🧪 Test des endpoints API...")
    api_results = test_api_endpoints()
    
    # Test Streamlit
    console.print("🎨 Test de l'interface Streamlit...")
    streamlit_status = test_streamlit_accessibility()
    
    # Affichage des résultats
    display_results(api_results, streamlit_status)
    
    # Test de requête complète (optionnel)
    console.print("\n" + "="*60)
    console.print("🎯 **Test de Requête Complète**")
    
    test_query = "je doie faire dix minut de chaude, apres 3 set de 5 mn a fond et 2 min pose entre set. fini avk 10 min cool down facile"
    console.print(f"📝 Requête: {test_query}")
    
    try:
        # Validation
        val_response = requests.post("http://localhost:8000/validate", json={
            "query": test_query,
            "author": "Test Intégration"
        }, timeout=10)
        
        if val_response.status_code == 200:
            val_data = val_response.json()
            console.print(f"✅ Validation: {val_data.get('confidence', 0):.1%} confiance")
            
            # Génération (si validation OK)
            if val_data.get('confidence', 0) > 0.7:
                gen_response = requests.post("http://localhost:8000/generate-workout", json={
                    "query": test_query,
                    "author": "Test Intégration",
                    "duration_minutes": 45,
                    "critical_power": 250
                }, timeout=15)
                
                if gen_response.status_code == 200:
                    gen_data = gen_response.json()
                    console.print(f"✅ Génération: {gen_data.get('duration_minutes', 0)} min, {len(gen_data.get('steps', []))} étapes")
                else:
                    console.print(f"❌ Génération échouée: {gen_response.status_code}")
            else:
                console.print("⚠️ Confiance trop faible pour génération")
        else:
            console.print(f"❌ Validation échouée: {val_response.status_code}")
            
    except Exception as e:
        console.print(f"❌ Erreur test complet: {str(e)}")
    
    console.print("\n🏁 Tests terminés !")

if __name__ == "__main__":
    main() 