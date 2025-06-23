#!/usr/bin/env python3
"""
Test de Précision Pipeline Vekta Hybride
Validation avec les tests réels observés en production
"""

import sys
import os
import time

# Ajout du chemin des modules Vekta
sys.path.append('./vekta')

def test_vekta_precision_parsing():
    """Test du parsing structurel avec les cas Vekta réels"""
    print("🎯 Test Parsing Structurel Vekta - Précision Numérique")
    print("=" * 65)
    
    try:
        from components.vekta_components import RAGPipeline, VektaStructuralParser
        
        # Initialisation
        pipeline = RAGPipeline()
        parser = VektaStructuralParser()
        
        # Tests de précision observés chez Vekta
        precision_tests = [
            # Test 1: Précision au niveau seconde
            {
                'query': "13x4min33s à 87.3%FTP avec 2min47s récup",
                'expected_precision': 'second',
                'expected_reps': 13,
                'expected_intensity': 87.3
            },
            # Test 2: Calculs automatiques
            {
                'query': "Alternance 47s entre 103% et 91%FTP pendant 23min",
                'expected_structure': 'alternation',
                'expected_calculation': True
            },
            # Test 3: Séquences mathématiques
            {
                'query': "Progression fibonacci: 1-1-2-3-5-8min à intensités croissantes",
                'expected_structure': 'fibonacci',
                'expected_sequence': [1,1,2,3,5,8]
            },
            # Test 4: Structures complexes
            {
                'query': "Séance spirale: 1min@80%, 2min@85%, 3min@90% puis redescendre",
                'expected_structure': 'spiral',
                'expected_completeness': 0.8
            }
        ]
        
        for i, test in enumerate(precision_tests, 1):
            print(f"\n🔬 Test {i}: Parsing Précision")
            print(f"   Requête: '{test['query']}'")
            
            # Test parsing structurel
            parsed = parser.parse_query(test['query'])
            
            print(f"   📊 Résultats Parsing:")
            print(f"      • Complétude: {parsed['completeness_score']:.1%}")
            print(f"      • Structure: {parsed['structure_type']}")
            print(f"      • Précision durée: {parsed['durations']['precision_level']}")
            print(f"      • Précision intensité: {parsed['intensities']['precision_level']}")
            
            # Vérifications spécifiques
            if 'expected_precision' in test:
                precision_ok = parsed['durations']['precision_level'] == test['expected_precision']
                print(f"      ✅ Précision attendue: {precision_ok}")
            
            if 'expected_reps' in test:
                reps_ok = parsed['repetitions']['primary'] == test['expected_reps']
                print(f"      ✅ Répétitions: {reps_ok} ({parsed['repetitions']['primary']})")
            
            if 'expected_intensity' in test:
                intensity_ok = abs(parsed['intensities']['primary'] - test['expected_intensity']) < 0.1
                print(f"      ✅ Intensité: {intensity_ok} ({parsed['intensities']['primary']}%)")
            
            if 'expected_calculation' in test:
                calc_ok = 'alternation' in parsed['calculated_values']
                print(f"      ✅ Calcul automatique: {calc_ok}")
                if calc_ok:
                    calc = parsed['calculated_values']['alternation']
                    print(f"         → {calc['calculated_repetitions']} répétitions calculées")
            
            print(f"   ⚡ Parsing: {'✅ Précision Vekta' if parsed['completeness_score'] >= 0.9 else '⚠️ Partiel'}")
        
        print(f"\n✅ Tests parsing structurel terminés!")
        
    except Exception as e:
        print(f"❌ Erreur test parsing: {e}")
        import traceback
        traceback.print_exc()

def test_vekta_mode_coach():
    """Test du mode coach sans validation (comportement Vekta)"""
    print(f"\n🔥 Test Mode Coach Expert - Zero Validation")
    print("=" * 55)
    
    try:
        from components.vekta_components import RAGPipeline
        
        pipeline = RAGPipeline()
        
        # Tests mode coach avec cas aberrants (acceptés par Vekta)
        coach_tests = [
            "6 heures à 130%FTP sans pause",  # Physiologiquement impossible
            "10x20min à 150%FTP avec 30s récup",  # Aberrant
            "juste du vélo très très dur",  # Très vague
            "séance de la mort qui tue",  # Créatif mais vague
        ]
        
        for i, query in enumerate(coach_tests, 1):
            print(f"\n🎯 Test Coach {i}: '{query}'")
            
            # Test mode coach
            result = pipeline.hybrid_process(query, coach_mode=True, ftp_watts=280)
            
            print(f"   📋 Résultat Mode Coach:")
            print(f"      • Succès: {result['success']}")
            print(f"      • Confiance: {result['confidence']:.0%}")
            print(f"      • Mode: {result.get('mode', 'N/A')}")
            print(f"      • Message: {result['message'][:100]}...")
            
            # Vérifications comportement coach
            coach_ok = result['success'] and result['confidence'] >= 0.85
            print(f"   🔥 Mode Coach: {'✅ Accepte tout' if coach_ok else '❌ Validation présente'}")
        
        print(f"\n✅ Tests mode coach terminés!")
        
    except Exception as e:
        print(f"❌ Erreur test mode coach: {e}")
        import traceback
        traceback.print_exc()

def test_vekta_error_messages():
    """Test des messages d'erreur style Vekta"""
    print(f"\n❌ Test Messages Erreur Style Vekta")
    print("=" * 45)
    
    try:
        from components.vekta_components import RAGPipeline
        
        pipeline = RAGPipeline()
        
        # Tests cas d'erreur observés chez Vekta
        error_tests = [
            {
                'query': "Séance lactate shuttle avec over-under threshold",
                'expected_error': "missing required information"
            },
            {
                'query': "jvvee fairrr duu velooo trreeee duuurrr 30miiinn",
                'expected_error': "language"  # Test limite NLU
            },
            {
                'query': "Séance de 2h avec 5x30min de travail",
                'expected_error': "intensity"
            }
        ]
        
        for i, test in enumerate(error_tests, 1):
            print(f"\n⚠️  Test Erreur {i}: '{test['query']}'")
            
            # Test mode utilisateur (validation stricte)
            result = pipeline.validate_query(test['query'])
            
            print(f"   📋 Résultat:")
            print(f"      • Succès: {result['success']}")
            print(f"      • Confiance: {result['confidence']:.0%}")
            print(f"      • Message: {result['message'][:120]}...")
            
            # Vérification message style Vekta
            error_style_ok = not result['success'] and "missing required information" in result['message']
            print(f"   ✅ Style Vekta: {'✅ Conforme' if error_style_ok else '⚠️ Différent'}")
        
        print(f"\n✅ Tests messages erreur terminés!")
        
    except Exception as e:
        print(f"❌ Erreur test messages: {e}")
        import traceback
        traceback.print_exc()

def test_vekta_comparaison_modes():
    """Comparaison directe modes utilisateur vs coach"""
    print(f"\n⚔️  Test Comparaison Modes User vs Coach")
    print("=" * 50)
    
    try:
        from components.vekta_components import RAGPipeline
        
        pipeline = RAGPipeline()
        
        # Requête test commune
        test_query = "3 séries de 5 minutes à fond avec 2 minutes de repos"
        
        print(f"📝 Requête test: '{test_query}'")
        
        # Mode utilisateur
        print(f"\n👤 MODE UTILISATEUR:")
        user_result = pipeline.hybrid_process(test_query, coach_mode=False)
        print(f"   • Succès: {user_result['success']}")
        print(f"   • Confiance: {user_result['confidence']:.0%}")
        print(f"   • Mode: {user_result.get('mode', 'validate_query')}")
        
        # Mode coach
        print(f"\n🔥 MODE COACH EXPERT:")
        coach_result = pipeline.hybrid_process(test_query, coach_mode=True)
        print(f"   • Succès: {coach_result['success']}")
        print(f"   • Confiance: {coach_result['confidence']:.0%}")
        print(f"   • Mode: {coach_result.get('mode', 'N/A')}")
        
        # Comparaison
        print(f"\n📊 COMPARAISON:")
        print(f"   • Confiance coach > user: {coach_result['confidence'] > user_result['confidence']}")
        print(f"   • Mode coach accepte plus: {coach_result['success'] or not user_result['success']}")
        print(f"   • Pipeline différencié: {coach_result.get('mode') != user_result.get('mode')}")
        
        print(f"\n✅ Comparaison modes terminée!")
        
    except Exception as e:
        print(f"❌ Erreur comparaison modes: {e}")
        import traceback
        traceback.print_exc()

def test_vekta_performance():
    """Test performance pipeline hybride"""
    print(f"\n⚡ Test Performance Pipeline Vekta")
    print("=" * 40)
    
    try:
        from components.vekta_components import RAGPipeline
        
        pipeline = RAGPipeline()
        
        # Tests de performance
        perf_queries = [
            "13x4min33s à 87.3%FTP avec 2min47s récup",  # Parsing précis
            "10min échauffement puis 3x5min VO2max",      # Structure simple
            "séance vague de vélo",                        # Cas fallback
        ]
        
        total_time = 0
        for i, query in enumerate(perf_queries, 1):
            start = time.time()
            result = pipeline.validate_query(query)
            duration = time.time() - start
            total_time += duration
            
            print(f"   Test {i}: {duration*1000:.1f}ms - {'✅' if result['success'] else '❌'}")
        
        avg_time = total_time / len(perf_queries)
        print(f"\n📊 Performance Moyenne: {avg_time*1000:.1f}ms")
        print(f"   🎯 Objectif Vekta <100ms: {'✅' if avg_time < 0.1 else '❌'}")
        
    except Exception as e:
        print(f"❌ Erreur test performance: {e}")

if __name__ == "__main__":
    print("🚴 TESTS PIPELINE VEKTA HYBRIDE - VALIDATION PRÉCISION")
    print("=" * 70)
    
    # Exécution séquentielle des tests
    test_vekta_precision_parsing()
    test_vekta_mode_coach()
    test_vekta_error_messages()
    test_vekta_comparaison_modes()
    test_vekta_performance()
    
    print(f"\n" + "=" * 70)
    print("✅ TOUS LES TESTS TERMINÉS")
    print("🎯 Pipeline Vekta Hybride: Parseur Structurel + Corpus Validation")
    print("🔥 Mode Coach: Zero validation physiologique")
    print("👤 Mode User: Validation hybride intelligente")
    print("⚡ Performance: Optimisée pour <100ms") 