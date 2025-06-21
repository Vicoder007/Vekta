#!/usr/bin/env python3
"""
🧪 Client de test pour l'API Vekta
Tests complets de tous les endpoints avec différents scénarios
"""

import asyncio
import json
import time
from typing import Dict, List, Any
import httpx
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

class VektaAPIClient:
    """Client de test pour l'API Vekta"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
    
    async def test_root_endpoint(self) -> Dict[str, Any]:
        """Test de l'endpoint racine"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            return {
                "endpoint": "/",
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response_time": response.elapsed.total_seconds(),
                "data": response.json() if response.status_code == 200 else None
            }
        except Exception as e:
            return {
                "endpoint": "/",
                "success": False,
                "error": str(e)
            }
    
    async def test_health_endpoint(self) -> Dict[str, Any]:
        """Test du health check"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            data = response.json() if response.status_code == 200 else None
            return {
                "endpoint": "/health",
                "status_code": response.status_code,
                "success": response.status_code == 200 and data.get("status") == "healthy",
                "response_time": response.elapsed.total_seconds(),
                "data": data
            }
        except Exception as e:
            return {
                "endpoint": "/health",
                "success": False,
                "error": str(e)
            }
    
    async def test_metrics_endpoint(self) -> Dict[str, Any]:
        """Test des métriques"""
        try:
            response = await self.client.get(f"{self.base_url}/metrics")
            data = response.json() if response.status_code == 200 else None
            return {
                "endpoint": "/metrics",
                "status_code": response.status_code,
                "success": response.status_code == 200 and "total_requests" in data,
                "response_time": response.elapsed.total_seconds(),
                "data": data
            }
        except Exception as e:
            return {
                "endpoint": "/metrics",
                "success": False,
                "error": str(e)
            }
    
    async def test_corpus_endpoint(self) -> Dict[str, Any]:
        """Test des informations corpus"""
        try:
            response = await self.client.get(f"{self.base_url}/corpus")
            data = response.json() if response.status_code == 200 else None
            return {
                "endpoint": "/corpus",
                "status_code": response.status_code,
                "success": response.status_code == 200 and "total_workouts" in data,
                "response_time": response.elapsed.total_seconds(),
                "data": data
            }
        except Exception as e:
            return {
                "endpoint": "/corpus",
                "success": False,
                "error": str(e)
            }
    
    async def test_validate_endpoint(self, query: str, expected_success: bool = True) -> Dict[str, Any]:
        """Test de validation d'une requête"""
        try:
            payload = {
                "query": query,
                "user_id": "test_user",
                "session_id": "test_session"
            }
            response = await self.client.post(
                f"{self.base_url}/validate",
                json=payload
            )
            data = response.json() if response.status_code == 200 else None
            
            success = (
                response.status_code == 200 and 
                data.get("success") == expected_success
            )
            
            return {
                "endpoint": "/validate",
                "query": query,
                "status_code": response.status_code,
                "success": success,
                "response_time": response.elapsed.total_seconds(),
                "data": data,
                "expected_success": expected_success
            }
        except Exception as e:
            return {
                "endpoint": "/validate",
                "query": query,
                "success": False,
                "error": str(e)
            }
    
    async def test_generate_workout_endpoint(self, query: str) -> Dict[str, Any]:
        """Test de génération de séance"""
        try:
            payload = {
                "query": query,
                "generate_zwo": True,
                "ftp": 250,
                "user_id": "test_user"
            }
            response = await self.client.post(
                f"{self.base_url}/generate-workout",
                json=payload
            )
            data = response.json() if response.status_code == 200 else None
            
            return {
                "endpoint": "/generate-workout",
                "query": query,
                "status_code": response.status_code,
                "success": response.status_code == 200 and data.get("success"),
                "response_time": response.elapsed.total_seconds(),
                "data": data
            }
        except Exception as e:
            return {
                "endpoint": "/generate-workout",
                "query": query,
                "success": False,
                "error": str(e)
            }
    
    async def test_batch_validate_endpoint(self, queries: List[str]) -> Dict[str, Any]:
        """Test de validation en lot"""
        try:
            response = await self.client.post(
                f"{self.base_url}/batch-validate",
                json=queries
            )
            data = response.json() if response.status_code == 200 else None
            
            return {
                "endpoint": "/batch-validate",
                "queries_count": len(queries),
                "status_code": response.status_code,
                "success": response.status_code == 200 and "results" in data,
                "response_time": response.elapsed.total_seconds(),
                "data": data
            }
        except Exception as e:
            return {
                "endpoint": "/batch-validate",
                "success": False,
                "error": str(e)
            }
    
    async def run_comprehensive_tests(self):
        """Exécute une suite complète de tests"""
        console.print(Panel("🧪 TESTS COMPLETS API VEKTA", style="bold blue"))
        
        test_queries = [
            ("je doie faire dix minut de chaude, apres 3 set de 5 mn a fond et 2 min pose entre set. fini avk 10 min cool down facile", True),
            ("20 minutes tempo seuil", True),
            ("8 fois 1 minute max avec 1 minute repos", True),
            ("45min aerobic zone2", True),
            ("faire du sport", False),  # Requête ambiguë
            ("piramide aerobik avec recupe", True)  # Fautes multiples
        ]
        
        batch_queries = [
            "tempo 20min",
            "vo2max intervals",
            "aerobic base"
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Tests des endpoints de base
            task1 = progress.add_task("Tests endpoints de base...", total=4)
            
            self.test_results.append(await self.test_root_endpoint())
            progress.advance(task1)
            
            self.test_results.append(await self.test_health_endpoint())
            progress.advance(task1)
            
            self.test_results.append(await self.test_metrics_endpoint())
            progress.advance(task1)
            
            self.test_results.append(await self.test_corpus_endpoint())
            progress.advance(task1)
            
            # Tests de validation
            task2 = progress.add_task("Tests validation...", total=len(test_queries))
            
            for query, expected_success in test_queries:
                result = await self.test_validate_endpoint(query, expected_success)
                self.test_results.append(result)
                progress.advance(task2)
            
            # Tests de génération
            task3 = progress.add_task("Tests génération...", total=2)
            
            result = await self.test_generate_workout_endpoint(test_queries[0][0])
            self.test_results.append(result)
            progress.advance(task3)
            
            # Test batch
            result = await self.test_batch_validate_endpoint(batch_queries)
            self.test_results.append(result)
            progress.advance(task3)
        
        # Affichage des résultats
        self.display_results()
    
    def display_results(self):
        """Affiche les résultats des tests"""
        table = Table(title="📊 Résultats des Tests API")
        table.add_column("Endpoint", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Temps (ms)", justify="right")
        table.add_column("Détails")
        
        success_count = 0
        total_tests = len(self.test_results)
        total_time = 0
        
        for result in self.test_results:
            endpoint = result.get("endpoint", "Unknown")
            success = result.get("success", False)
            response_time = result.get("response_time", 0) * 1000  # Convert to ms
            
            status = "✅ PASS" if success else "❌ FAIL"
            status_style = "green" if success else "red"
            
            details = ""
            if "query" in result:
                details = f"Query: {result['query'][:30]}..."
            elif "error" in result:
                details = f"Error: {result['error'][:50]}..."
            elif result.get("data"):
                if endpoint == "/health":
                    details = f"Status: {result['data'].get('status', 'unknown')}"
                elif endpoint == "/metrics":
                    details = f"Requests: {result['data'].get('total_requests', 0)}"
                elif endpoint == "/validate":
                    details = f"Confidence: {result['data'].get('confidence', 0):.3f}"
            
            table.add_row(
                endpoint,
                f"[{status_style}]{status}[/{status_style}]",
                f"{response_time:.1f}",
                details
            )
            
            if success:
                success_count += 1
            total_time += response_time
        
        console.print(table)
        
        # Résumé
        success_rate = (success_count / total_tests) * 100
        avg_response_time = total_time / total_tests
        
        summary = f"""
📈 Résumé des Tests:
• Tests réussis: {success_count}/{total_tests} ({success_rate:.1f}%)
• Temps de réponse moyen: {avg_response_time:.1f}ms
• Temps total: {total_time:.1f}ms
        """
        
        summary_style = "green" if success_rate >= 90 else "yellow" if success_rate >= 70 else "red"
        console.print(Panel(summary.strip(), style=summary_style))
        
        # Détails des échecs
        failures = [r for r in self.test_results if not r.get("success")]
        if failures:
            console.print("\n❌ Échecs détaillés:")
            for failure in failures:
                console.print(f"• {failure.get('endpoint')}: {failure.get('error', 'Unknown error')}")
    
    async def close(self):
        """Ferme le client HTTP"""
        await self.client.aclose()

async def main():
    """Fonction principale"""
    client = VektaAPIClient()
    
    try:
        await client.run_comprehensive_tests()
    except KeyboardInterrupt:
        console.print("\n⚠️ Tests interrompus par l'utilisateur")
    except Exception as e:
        console.print(f"\n❌ Erreur lors des tests: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    # Vérifier que l'API est démarrée
    console.print("🚀 Démarrage des tests API Vekta...")
    console.print("📍 URL de base: http://127.0.0.1:8000")
    console.print("⚠️  Assurez-vous que l'API est démarrée avec: python vekta_api.py\n")
    
    asyncio.run(main()) 