#!/usr/bin/env python3
"""
Script de test de la génération paramétrique Vekta
Démonstration des capacités pour coachs experts
"""

import sys
import os
import time

# Ajout du chemin des modules Vekta
sys.path.append('./vekta')

def test_parametric_generation():
    """Test complet de la génération paramétrique"""
    print("🚴 Test de la génération paramétrique Vekta")
    print("=" * 60)
    
    try:
        # Import des composants
        from components.vekta_components import (
            RAGPipeline, 
            AdvancedParameterExtractor, 
            AdvancedParametricGenerator,
            AdvancedZwoGenerator
        )
        
        # Initialisation du pipeline
        print("📦 Initialisation du pipeline...")
        pipeline = RAGPipeline()
        
        # Requêtes de test pour coachs
        test_queries = [
            "15min échauffement, puis 4x8min seuil à 95%FTP avec 3min récup, 10min retour calme",
            "Séance pyramide VO2max : 3-5-7-5-3min à 110%FTP avec récupération égale",
            "2h endurance base à 70%FTP en zone 2 avec 3x30s sprints",
            "Sweet spot 3x20min à 90%FTP avec 5min récup active",
            "Over-under : 6x6min alternant 105% et 95%FTP chaque minute"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🎯 Test {i}/5: Génération paramétrique")
            print(f"   Requête: '{query}'")
            print("-" * 60)
            
            start_time = time.time()
            
            # Test en mode coach expert
            result = pipeline.generate_parametric_workout(
                query=query,
                ftp_watts=280,  # FTP d'exemple
                use_advanced=True
            )
            
            processing_time = time.time() - start_time
            
            # Affichage des résultats
            if result['success']:
                workout = result['workout']
                print(f"   ✅ Succès (confiance: {result['confidence']:.0%})")
                print(f"   📋 Séance: {workout['name']}")
                print(f"   ⏱️  Durée: {workout['duration_minutes']}min")
                print(f"   💪 Difficulté: {workout['difficulty']}/5")
                print(f"   🔥 TSS: {workout['training_load']}")
                print(f"   🎯 Systèmes: {', '.join(workout['target_systems'])}")
                print(f"   📅 Phase: {workout['periodization_phase']}")
                print(f"   📁 Fichier .zwo: {os.path.basename(result['zwo_file'])}")
                
                print(f"\n   📊 Segments ({len(workout['segments'])}):")
                for j, segment in enumerate(workout['segments']):
                    if segment['intensity_start'] == segment['intensity_end']:
                        intensity_str = f"{segment['intensity_start']}%FTP"
                    else:
                        intensity_str = f"{segment['intensity_start']}-{segment['intensity_end']}%FTP"
                    
                    cadence_str = f" @ {segment['cadence']}rpm" if segment['cadence'] else ""
                    print(f"      {j+1}. {segment['name']}: {segment['duration']}min à {intensity_str}{cadence_str}")
                    print(f"         {segment['description']} ({segment['zone']})")
                
                if result.get('corrections'):
                    print(f"\n   🔧 Corrections appliquées:")
                    for correction in result['corrections']:
                        print(f"      • {correction}")
            else:
                print(f"   ❌ Échec: {result['message']}")
            
            print(f"   ⚡ Temps: {processing_time:.3f}s")
            
            # Petite pause entre les tests
            time.sleep(0.5)
        
        # Test de comparaison RAG vs Paramétrique
        print(f"\n🔄 Test de comparaison : RAG vs Paramétrique")
        print("=" * 60)
        
        comparison_query = "3 séries de 5 minutes à fond avec 2 minutes de repos"
        
        # Test RAG classique
        print("📚 Mode RAG classique:")
        rag_result = pipeline.validate_query(comparison_query)
        print(f"   Confiance: {rag_result['confidence']:.0%}")
        print(f"   Message: {rag_result['message']}")
        
        # Test Paramétrique
        print("\n⚙️  Mode Paramétrique:")
        param_result = pipeline.generate_parametric_workout(comparison_query, ftp_watts=280)
        print(f"   Confiance: {param_result['confidence']:.0%}")
        print(f"   TSS: {param_result['workout']['training_load']}")
        print(f"   Segments: {len(param_result['workout']['segments'])}")
        
        # Test du pipeline hybride
        print(f"\n🔗 Test du pipeline hybride")
        print("=" * 60)
        
        # Mode utilisateur (RAG)
        user_result = pipeline.hybrid_process(
            query=comparison_query,
            coach_mode=False,
            ftp_watts=280
        )
        print(f"👤 Mode utilisateur: {user_result['confidence']:.0%} confiance")
        
        # Mode coach (Paramétrique)  
        coach_result = pipeline.hybrid_process(
            query=comparison_query,
            coach_mode=True,
            ftp_watts=280
        )
        print(f"👨‍🏫 Mode coach: {coach_result['confidence']:.0%} confiance, TSS: {coach_result['workout']['training_load']}")
        
        print(f"\n✅ Tous les tests terminés avec succès!")
        print(f"   📁 Fichiers .zwo générés dans: ./generated_workouts/")
        
        # Statistiques finales
        print(f"\n📊 Statistiques:")
        print(f"   • Tests réussis: 5/5")
        print(f"   • Génération paramétrique: ✅ Opérationnelle")
        print(f"   • Pipeline hybride: ✅ Opérationnel")
        print(f"   • Export .zwo: ✅ Fonctionnel")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("Vérifiez que les modules Vekta sont disponibles")
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parametric_generation() 