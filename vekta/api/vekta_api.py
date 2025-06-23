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
    critical_power: Optional[int] = Field(250, description="Puissance critique en watts")
    author: Optional[str] = Field("Vekta AI", description="Auteur de la séance")
    user_id: Optional[str] = Field(None, description="ID utilisateur")

class ParametricWorkoutRequest(BaseModel):
    query: str = Field(..., description="Requête utilisateur")
    ftp_watts: int = Field(250, description="FTP en watts")
    coach_mode: bool = Field(True, description="Mode coach expert (génération paramétrique)")
    generate_zwo: bool = Field(True, description="Générer le fichier .zwo")
    use_advanced: bool = Field(True, description="Utiliser le générateur avancé")
    user_id: Optional[str] = Field(None, description="ID utilisateur")

class WorkoutGenerationResponse(BaseModel):
    success: bool = Field(..., description="Génération réussie")
    confidence: float = Field(..., description="Score de confiance")
    workout: Dict[str, Any] = Field(..., description="Détails de la séance")
    zwo_file_path: Optional[str] = Field(None, description="Chemin du fichier .zwo généré")
    zwo_download_url: Optional[str] = Field(None, description="URL de téléchargement du .zwo")
    processing_time: float = Field(..., description="Temps de traitement")

class ParametricWorkoutResponse(BaseModel):
    success: bool = Field(..., description="Génération réussie")
    confidence: float = Field(..., description="Score de confiance")
    mode: str = Field(..., description="Mode de génération utilisé")
    workout: Optional[Dict[str, Any]] = Field(None, description="Détails de la séance")
    zwo_file_path: Optional[str] = Field(None, description="Chemin du fichier .zwo généré")
    zwo_download_url: Optional[str] = Field(None, description="URL de téléchargement du .zwo")
    features: Optional[Dict[str, bool]] = Field(None, description="Fonctionnalités utilisées")
    correction_applied: bool = Field(False, description="Corrections orthographiques appliquées")
    corrections: List[str] = Field(default_factory=list, description="Liste des corrections")
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
        
        # Import des vrais composants RAG
        import sys
        import os
        
        # Import des composants depuis le package components
        from components.vekta_components import RAGPipeline, ZwoGenerator
        
        rag_pipeline = RAGPipeline()
        zwo_generator = ZwoGenerator()
        
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
        
        # Enrichissement avec les données utilisateur
        workout_metadata = workout['metadata'].copy()
        workout_metadata['author'] = request.author
        workout_metadata['critical_power'] = request.critical_power
        workout_metadata['generated_at'] = datetime.now().isoformat()
        
        # Génération de données supplémentaires pour l'interface
        duration_minutes = workout_metadata['duration_minutes']
        avg_power_percent = 75 + (workout_metadata['difficulty'] * 5)  # 80-95% selon difficulté
        training_stimulus = duration_minutes * (avg_power_percent / 100) * 1.2
        estimated_calories = duration_minutes * 12 * (avg_power_percent / 100)
        
        # Génération d'étapes structurées pour l'interface
        steps = _generate_workout_steps(workout['text'], workout_metadata)
        
        # Construction de la réponse enrichie
        enriched_workout = {
            **workout,
            'metadata': workout_metadata,
            'duration_minutes': duration_minutes,
            'avg_power_percent': avg_power_percent,
            'training_stimulus': training_stimulus,
            'estimated_calories': estimated_calories,
            'steps': steps
        }
        
        zwo_file_path = None
        zwo_download_url = None
        
        # Génération du fichier .zwo si demandé
        if request.generate_zwo:
            try:
                zwo_file_path = zwo_generator.create_zwo_file(
                    workout['text'], 
                    workout_metadata
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
            workout=enriched_workout,
            zwo_file_path=zwo_file_path,
            zwo_download_url=zwo_download_url,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la génération: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur de génération: {str(e)}")

@app.post("/generate-parametric", response_model=ParametricWorkoutResponse)
async def generate_parametric_workout(request: ParametricWorkoutRequest):
    """Génère une séance paramétrique pour coachs experts"""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="Service RAG non initialisé")
    
    start_time = time.time()
    
    try:
        # Génération paramétrique via le pipeline hybride
        result = rag_pipeline.hybrid_process(
            query=request.query,
            coach_mode=request.coach_mode,
            ftp_watts=request.ftp_watts
        )
        
        # Enregistrement des métriques
        success = result.get('success', False)
        processing_time = time.time() - start_time
        metrics.record_request('/generate-parametric', processing_time, success)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.get('message', 'Génération échouée'))
        
        # Construction de l'URL de téléchargement
        zwo_download_url = None
        if result.get('zwo_file'):
            filename = os.path.basename(result['zwo_file'])
            zwo_download_url = f"/download-zwo/{filename}"
        
        return ParametricWorkoutResponse(
            success=result['success'],
            confidence=result['confidence'],
            mode=result.get('mode', 'parametric'),
            workout=result.get('workout'),
            zwo_file_path=result.get('zwo_file'),
            zwo_download_url=zwo_download_url,
            features=result.get('features'),
            correction_applied=result.get('correction_applied', False),
            corrections=result.get('corrections', []),
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        metrics.record_request('/generate-parametric', processing_time, False)
        logger.error(f"Erreur lors de la génération paramétrique: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.post("/hybrid-process", response_model=ParametricWorkoutResponse)
async def hybrid_process_workout(request: ParametricWorkoutRequest):
    """Pipeline hybride : RAG ou génération paramétrique selon le mode"""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="Service RAG non initialisé")
    
    start_time = time.time()
    
    try:
        # Traitement hybride
        if request.coach_mode:
            # Mode coach : génération paramétrique
            result = rag_pipeline.generate_parametric_workout(
                query=request.query,
                ftp_watts=request.ftp_watts,
                use_advanced=request.use_advanced
            )
        else:
            # Mode utilisateur : RAG classique
            result = rag_pipeline.validate_query(request.query)
            # Adapter le format de retour pour la cohérence
            result['mode'] = 'rag_classic'
            result['features'] = {
                'rag_search': True,
                'semantic_matching': True,
                'corpus_based': True
            }
        
        # Enregistrement des métriques
        success = result.get('success', False)
        processing_time = time.time() - start_time
        metrics.record_request('/hybrid-process', processing_time, success)
        
        # Construction de l'URL de téléchargement
        zwo_download_url = None
        if result.get('zwo_file'):
            filename = os.path.basename(result['zwo_file'])
            zwo_download_url = f"/download-zwo/{filename}"
        
        return ParametricWorkoutResponse(
            success=result['success'],
            confidence=result['confidence'],
            mode=result.get('mode', 'unknown'),
            workout=result.get('workout'),
            zwo_file_path=result.get('zwo_file'),
            zwo_download_url=zwo_download_url,
            features=result.get('features'),
            correction_applied=result.get('correction_applied', False),
            corrections=result.get('corrections', []),
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        metrics.record_request('/hybrid-process', processing_time, False)
        logger.error(f"Erreur lors du traitement hybride: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

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

def _generate_workout_steps(workout_text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Génère les étapes structurées d'une séance pour l'interface"""
    steps = []
    difficulty = metadata.get('difficulty', 3)
    zone = metadata.get('zone', 'Zone 3')
    
    # Analyse basique du texte pour extraire la structure
    text_lower = workout_text.lower()
    
    # Échauffement
    if 'echauffement' in text_lower or 'warm' in text_lower:
        warmup_duration = 10  # défaut
        if '15min' in text_lower and 'echauffement' in text_lower:
            warmup_duration = 15
        elif '20min' in text_lower and 'echauffement' in text_lower:
            warmup_duration = 20
        
        steps.append({
            'duration': warmup_duration,
            'power_percent': 60,
            'zone': 'Zone 2',
            'description': 'Échauffement progressif'
        })
    
    # Travail principal
    main_duration = max(10, metadata['duration_minutes'] - 20)  # Total - échauffement - retour calme
    main_power = 70 + (difficulty * 5)  # 75-95% selon difficulté
    
    if 'series' in text_lower or 'set' in text_lower:
        # Séries avec récupération
        if '3' in text_lower and '5min' in text_lower:
            # 3x5min
            for i in range(3):
                steps.append({
                    'duration': 5,
                    'power_percent': main_power,
                    'zone': zone,
                    'description': f'Série {i+1} - Travail intensif'
                })
                if i < 2:  # Pas de récup après la dernière série
                    steps.append({
                        'duration': 2,
                        'power_percent': 50,
                        'zone': 'Zone 1',
                        'description': 'Récupération'
                    })
        elif '5' in text_lower and '5min' in text_lower:
            # 5x5min
            for i in range(5):
                steps.append({
                    'duration': 5,
                    'power_percent': main_power,
                    'zone': zone,
                    'description': f'Série {i+1} - Travail intensif'
                })
                if i < 4:
                    steps.append({
                        'duration': 2,
                        'power_percent': 50,
                        'zone': 'Zone 1',
                        'description': 'Récupération'
                    })
    else:
        # Travail continu
        steps.append({
            'duration': main_duration,
            'power_percent': main_power,
            'zone': zone,
            'description': 'Travail principal continu'
        })
    
    # Retour au calme
    if 'retour' in text_lower or 'cool' in text_lower or 'calme' in text_lower:
        cooldown_duration = 10
        if '15min' in text_lower and ('retour' in text_lower or 'cool' in text_lower):
            cooldown_duration = 15
        
        steps.append({
            'duration': cooldown_duration,
            'power_percent': 50,
            'zone': 'Zone 1',
            'description': 'Retour au calme'
        })
    
    return steps

if __name__ == "__main__":
    # Configuration pour le développement
    uvicorn.run(
        "vekta_api:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 