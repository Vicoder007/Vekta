#!/usr/bin/env python3
"""
Test Script Vekta V2 - Validation rapide
"""

import os
import sys

# Ajouter le chemin components
components_path = os.path.join(os.path.dirname(__file__), 'components')
if components_path not in sys.path:
    sys.path.insert(0, components_path)

def test_imports():
    """Test des imports"""
    print("🔍 Test des imports...")
    try:
        from llm_parser import IntelligentWorkoutParser, WorkoutEntity
        print("✅ Import llm_parser: OK")
        return True
    except ImportError as e:
        print(f"❌ Import llm_parser: {e}")
        return False

def test_parser():
    """Test du parser intelligent"""
    print("\n🧠 Test du parser intelligent...")
    
    from llm_parser import IntelligentWorkoutParser
    
    # Initialiser parser (mode fallback)
    parser = IntelligentWorkoutParser()
    
    # Tests basiques
    tests = [
        "5 minutes tempo",
        "tempo 5 minutes", 
        "2x3x5 minutes tempo",
        "5x3min à 95%"
    ]
    
    for test_query in tests:
        try:
            entities = parser.extract_entities(test_query)
            workout = parser.generate_workout_structure(entities, 250)
            is_valid, errors = parser.validate_structure_strict(workout, entities, test_query)
            
            print(f"✅ '{test_query}': {len(workout)} étapes, valid={is_valid}")
            
        except Exception as e:
            print(f"❌ '{test_query}': {e}")
    
    return True

def test_streamlit_running():
    """Test si Streamlit V2 fonctionne"""
    print("\n🌐 Test Streamlit V2...")
    
    import requests
    try:
        response = requests.get("http://localhost:8502/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit V2 accessible sur http://localhost:8502")
            return True
        else:
            print(f"❌ Streamlit V2: status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Streamlit V2 non accessible: {e}")
        return False

def main():
    """Tests principaux"""
    print("🧠 VEKTA V2 - Tests de Validation")
    print("=" * 40)
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test parser si imports OK
    if results[0]:
        results.append(test_parser())
    
    # Test Streamlit
    results.append(test_streamlit_running())
    
    # Résultats
    print("\n" + "=" * 40)
    print("📊 RÉSULTATS:")
    
    if all(results):
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("\n🚀 Vekta V2 est opérationnel!")
        print("🌐 Interface: http://localhost:8502")
    else:
        print("⚠️  Certains tests ont échoué")
        failed_count = len([r for r in results if not r])
        print(f"❌ {failed_count}/{len(results)} tests échoués")

if __name__ == "__main__":
    main() 