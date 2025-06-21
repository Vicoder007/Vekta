#!/usr/bin/env python3
"""
🚀 Vekta API - Service Layer FastAPI
API REST pour le pipeline RAG avec tous les endpoints nécessaires

Endpoints:
- POST /validate: Valide une requête utilisateur
- POST /generate-workout: Génère une séance complète avec fichier .zwo
- GET /health: Health check du service
- GET /metrics: Métriques de performance
- GET /corpus: Informations sur le corpus
"""

import os
import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Import des composants Vekta (à adapter selon la structure finale)
import sys
sys.path.append('.')

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('vekta_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Métriques globales
class APIMetrics:
    def __init__(self):
        self.requests_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.start_time = datetime.now()
        self.endpoint_stats = {}
    
    def record_request(self, endpoint: str, response_time: float, success: bool):
        self.requests_count += 1
        self.total_response_time += response_time
        
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        
        if endpoint not in self.endpoint_stats:
            self.endpoint_stats[endpoint] = {
                'count': 0, 'success': 0, 'error': 0, 'total_time': 0.0
            }
        
        stats = self.endpoint_stats[endpoint]
        stats['count'] += 1
        stats['total_time'] += response_time
        if success:
            stats['success'] += 1
        else:
            stats['error'] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        uptime = (datetime.now() - self.start_time).total_seconds()
        avg_response_time = self.total_response_time / max(self.requests_count, 1)
        
        return {
            'uptime_seconds': uptime,
            'total_requests': self.requests_count,
            'success_rate': self.success_count / max(self.requests_count, 1),
            'average_response_time': avg_response_time,
            'requests_per_second': self.requests_count / max(uptime, 1),
            'endpoint_stats': {
                endpoint: {
                    **stats,
                    'avg_response_time': stats['total_time'] / max(stats['count'], 1),
                    'success_rate': stats['success'] / max(stats['count'], 1)
                }
                for endpoint, stats in self.endpoint_stats.items()
            }
        }

metrics = APIMetrics()

# Modèles Pydantic pour l'API
class QueryRequest(BaseModel):
    query: str = Field(..., description="Requête utilisateur en langage naturel")
    user_id: Optional[str] = Field(None, description="ID utilisateur pour tracking")
    session_id: Optional[str] = Field(None, description="ID de session")

class ValidationResponse(BaseModel):
    success: bool = Field(..., description="Validation réussie")
    confidence: float = Field(..., description="Score de confiance (0-1)")
    message: str = Field(..., description="Message de résultat")
    workout: Optional[Dict[str, Any]] = Field(None, description="Séance recommandée")
    correction_applied: bool = Field(False, description="Corrections orthographiques appliquées")
    corrections: List[str] = Field(default_factory=list, description="Liste des corrections")
    processing_time: float = Field(..., description="Temps de traitement en secondes")

class WorkoutGenerationRequest(BaseModel):
    query: str = Field(..., description="Requête utilisateur")
    generate_zwo: bool = Field(True, description="Générer le fichier .zwo")
    ftp: Optional[int] = Field(None, description="FTP utilisateur en watts")
    user_id: Optional[str] = Field(None, description="ID utilisateur")

class WorkoutGenerationResponse(BaseModel):
    success: bool = Field(..., description="Génération réussie")
    confidence: float = Field(..., description="Score de confiance")
    workout: Dict[str, Any] = Field(..., description="Détails de la séance")
    zwo_file_path: Optional[str] = Field(None, description="Chemin du fichier .zwo généré")
    zwo_download_url: Optional[str] = Field(None, description="URL de téléchargement du .zwo")
    processing_time: float = Field(..., description="Temps de traitement")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Status du service")
    version: str = Field(..., description="Version de l'API")
    uptime: float = Field(..., description="Uptime en secondes")
    components: Dict[str, str] = Field(..., description="Status des composants")

# Variables globales pour les composants (à initialiser au startup)
rag_pipeline = None
spell_checker = None
corpus = None
zwo_generator = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application"""
    logger.info("🚀 Démarrage de l'API Vekta...")
    
    # Initialisation des composants
    global rag_pipeline, spell_checker, corpus, zwo_generator
    
    try:
        # Ici, nous importerions et initialiserions les composants réels
        # Pour l'instant, on simule avec des objets mock
        logger.info("📦 Chargement des composants RAG...")
        
        # TODO: Remplacer par les vrais imports quand les modules seront extraits
        # from vekta.spell_checker import SpellChecker
        # from vekta.corpus import EnhancedCorpus
        # from vekta.rag_pipeline import RAGPipeline
        # from vekta.zwo_generator import ZwoGenerator
        
        # spell_checker = SpellChecker()
        # corpus = EnhancedCorpus()
        # rag_pipeline = RAGPipeline(spell_checker, corpus, embedding_system)
        # zwo_generator = ZwoGenerator()
        
        # Mock pour le développement
        class MockRAGPipeline:
            def validate_query(self, query: str):
                return {
                    'success': True,
                    'confidence': 0.85,
                    'message': 'Séance trouvée avec haute confiance: Mock Workout',
                    'workout': {
                        'text': 'Mock workout text',
                        'metadata': {
                            'name': 'Mock Workout',
                            'description': 'Mock workout description',
                            'duration_minutes': 45,
                            'difficulty': 3
                        },
                        'hybrid_score': 0.85
                    },
                    'correction_applied': False,
                    'corrections': []
                }
        
        class MockZwoGenerator:
            def create_zwo_file(self, workout_text, metadata, output_dir="./generated_workouts"):
                os.makedirs(output_dir, exist_ok=True)
                filename = f"mock_workout_{int(time.time())}.zwo"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'w') as f:
                    f.write(f'<?xml version="1.0"?><workout><name>{metadata["name"]}</name></workout>')
                return filepath
        
        rag_pipeline = MockRAGPipeline()
        zwo_generator = MockZwoGenerator()
        
        logger.info("✅ Composants RAG chargés avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        raise
    
    yield
    
    logger.info("🔄 Arrêt de l'API Vekta...")

# Création de l'application FastAPI
app = FastAPI(
    title="Vekta API",
    description="API REST pour la génération intelligente de séances d'entraînement cyclistes",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour les métriques
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        success = response.status_code < 400
    except Exception as e:
        logger.error(f"Erreur dans la requête: {e}")
        success = False
        response = JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )
    
    process_time = time.time() - start_time
    endpoint = request.url.path
    
    metrics.record_request(endpoint, process_time, success)
    
    return response

@app.get("/", response_model=Dict[str, str])
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🚀 Vekta API - Générateur intelligent de séances d'entraînement cyclistes",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check du service"""
    uptime = (datetime.now() - metrics.start_time).total_seconds()
    
    # Vérification des composants
    components = {
        "rag_pipeline": "healthy" if rag_pipeline else "unavailable",
        "zwo_generator": "healthy" if zwo_generator else "unavailable",
        "database": "healthy",  # TODO: vérifier la base vectorielle
        "filesystem": "healthy"
    }
    
    overall_status = "healthy" if all(status == "healthy" for status in components.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        version="1.0.0",
        uptime=uptime,
        components=components
    )

@app.get("/metrics")
async def get_metrics():
    """Métriques de performance du service"""
    return metrics.get_stats()

@app.get("/corpus")
async def get_corpus_info():
    """Informations sur le corpus d'entraînement"""
    # TODO: Implémenter avec le vrai corpus
    return {
        "total_workouts": 9,
        "workout_types": ["aerobic", "tempo", "vo2", "mixed"],
        "difficulty_levels": [1, 2, 3, 4, 5],
        "average_duration": 35,
        "language_support": ["french"]
    }

@app.post("/validate", response_model=ValidationResponse)
async def validate_query(request: QueryRequest):
    """Valide une requête utilisateur et retourne la séance recommandée"""
    start_time = time.time()
    
    try:
        logger.info(f"Validation de requête: '{request.query}' (user: {request.user_id})")
        
        if not rag_pipeline:
            raise HTTPException(status_code=503, detail="Service RAG indisponible")
        
        # Validation via le pipeline RAG
        result = rag_pipeline.validate_query(request.query)
        
        processing_time = time.time() - start_time
        
        logger.info(f"Validation terminée en {processing_time:.3f}s - Succès: {result['success']}")
        
        return ValidationResponse(
            success=result['success'],
            confidence=result['confidence'],
            message=result['message'],
            workout=result.get('workout'),
            correction_applied=result.get('correction_applied', False),
            corrections=result.get('corrections', []),
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de la validation: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de validation: {str(e)}")

@app.post("/generate-workout", response_model=WorkoutGenerationResponse)
async def generate_workout(request: WorkoutGenerationRequest):
    """Génère une séance complète avec fichier .zwo optionnel"""
    start_time = time.time()
    
    try:
        logger.info(f"Génération de séance: '{request.query}' (user: {request.user_id})")
        
        if not rag_pipeline or not zwo_generator:
            raise HTTPException(status_code=503, detail="Services indisponibles")
        
        # Validation de la requête
        validation_result = rag_pipeline.validate_query(request.query)
        
        if not validation_result['success']:
            raise HTTPException(
                status_code=400, 
                detail=f"Impossible de générer la séance: {validation_result['message']}"
            )
        
        workout = validation_result['workout']
        zwo_file_path = None
        zwo_download_url = None
        
        # Génération du fichier .zwo si demandé
        if request.generate_zwo:
            try:
                zwo_file_path = zwo_generator.create_zwo_file(
                    workout['text'], 
                    workout['metadata']
                )
                zwo_download_url = f"/download-zwo/{os.path.basename(zwo_file_path)}"
                logger.info(f"Fichier .zwo généré: {zwo_file_path}")
            except Exception as e:
                logger.warning(f"Erreur génération .zwo: {e}")
        
        processing_time = time.time() - start_time
        
        logger.info(f"Génération terminée en {processing_time:.3f}s")
        
        return WorkoutGenerationResponse(
            success=True,
            confidence=validation_result['confidence'],
            workout=workout,
            zwo_file_path=zwo_file_path,
            zwo_download_url=zwo_download_url,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la génération: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")

@app.get("/download-zwo/{filename}")
async def download_zwo(filename: str):
    """Télécharge un fichier .zwo généré"""
    file_path = os.path.join("./generated_workouts", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    
    return FileResponse(
        file_path,
        media_type="application/xml",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Endpoint pour les tests de charge
@app.post("/batch-validate")
async def batch_validate(queries: List[str]):
    """Validation en lot pour les tests de performance"""
    if len(queries) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 requêtes par lot")
    
    results = []
    for query in queries:
        try:
            result = rag_pipeline.validate_query(query)
            results.append({
                "query": query,
                "success": result['success'],
                "confidence": result['confidence']
            })
        except Exception as e:
            results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}

if __name__ == "__main__":
    # Configuration pour le développement
    uvicorn.run(
        "vekta_api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 