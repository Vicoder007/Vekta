#!/usr/bin/env python3
"""
Test Simple - Vekta V2 Structure Aplatie
"""

import os
import sys
import requests

# Ajouter components au path
components_path = os.path.join(os.path.dirname(__file__), 'components')
if components_path not in sys.path:
    sys.path.insert(0, components_path)

def test_structure():
    """Test de la structure aplatie"""
    print("🏗️ Test structure aplatie...")
    
    expected_files = [
        'components/llm_parser.py',
        'frontend/vekta_app_simple.py', 
        'launch_vekta_v2.py',
        'README.md'
    ]
    
    missing = []
    for file_path in expected_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ Fichiers manquants: {missing}")
        return False
    else:
        print("✅ Structure aplatie correcte")
        return True

def test_parser_import():
    """Test import parser"""
    print("🧠 Test import parser...")
    
    try:
        from llm_parser import IntelligentWorkoutParser
        parser = IntelligentWorkoutParser()
        
        # Test simple
        entities = parser.extract_entities("5 minutes tempo")
        workout = parser.generate_workout_structure(entities, 250)
        
        print(f"✅ Parser opérationnel: {len(workout)} étapes générées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur parser: {e}")
        return False

def test_interface():
    """Test interface simple"""
    print("🌐 Test interface simple...")
    
    try:
        response = requests.get("http://localhost:8502/_stcore/health", timeout=5)
        if response.status_code == 200:
            print("✅ Interface V2 Simple accessible")
            return True
        else:
            print(f"❌ Interface: status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Interface non accessible: {e}")
        return False

def main():
    print("🧠 VEKTA V2 - Test Structure Simple")
    print("=" * 40)
    
    tests = [
        test_structure(),
        test_parser_import(),
        test_interface()
    ]
    
    print("\n" + "=" * 40)
    if all(tests):
        print("🎉 STRUCTURE SIMPLE VALIDÉE!")
        print("🌐 Interface: http://localhost:8502")
    else:
        failed = len([t for t in tests if not t])
        print(f"⚠️  {failed}/{len(tests)} tests échoués")

if __name__ == "__main__":
    main() 