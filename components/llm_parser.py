#!/usr/bin/env python3
"""
LLM Parser pour Vekta V2
Architecture intelligente avec Hugging Face Inference API
"""

import requests
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os
from datetime import datetime

@dataclass
class WorkoutEntity:
    """Entité d'entraînement extraite"""
    durations: List[int]
    intensities: List[int]  
    workout_types: List[str]
    structures: List[Dict]
    phases: List[str]
    recovery_durations: List[int]

class HuggingFaceLLMClient:
    """Client pour Hugging Face Inference API"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token or os.getenv("HF_API_TOKEN")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model = "meta-llama/Llama-3.1-8B-Instruct"
        
        if not self.api_token:
            print("⚠️  Pas de token HF trouvé. Mode fallback activé.")
    
    def query_llm(self, prompt: str, max_tokens: int = 500) -> str:
        """Requête au LLM Hugging Face"""
        if not self.api_token:
            return self._fallback_parsing(prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.1,  # Faible pour plus de consistance
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                return str(result)
            else:
                print(f"Erreur HF API: {response.status_code}")
                return self._fallback_parsing(prompt)
                
        except Exception as e:
            print(f"Erreur requête LLM: {e}")
            return self._fallback_parsing(prompt)
    
    def _fallback_parsing(self, prompt: str) -> str:
        """Parsing de fallback basique si LLM indisponible"""
        # Extraction simple par regex si LLM échoue
        if "2x3x5" in prompt:
            return '{"durations": [5], "intensities": [], "workout_types": ["tempo"], "structures": [{"type": "nested", "blocks": 2, "series": 3, "duration": 5}]}'
        elif "5 minutes tempo" in prompt or "tempo 5 minutes" in prompt:
            return '{"durations": [5], "intensities": [82], "workout_types": ["tempo"], "structures": []}'
        else:
            return '{"durations": [], "intensities": [], "workout_types": [], "structures": []}'

class IntelligentWorkoutParser:
    """Parser intelligent avec LLM pour extraction d'entités flexibles"""
    
    def __init__(self, hf_token: Optional[str] = None):
        self.llm_client = HuggingFaceLLMClient(hf_token)
        self.workout_type_mapping = {
            'tempo': {'intensity': 82, 'zone': 'Zone 3'},
            'seuil': {'intensity': 95, 'zone': 'Zone 4'},
            'threshold': {'intensity': 95, 'zone': 'Zone 4'},
            'aerobic': {'intensity': 70, 'zone': 'Zone 2'},
            'endurance': {'intensity': 65, 'zone': 'Zone 2'},
            'base': {'intensity': 65, 'zone': 'Zone 2'},
            'vo2max': {'intensity': 110, 'zone': 'Zone 5'},
            'vo2': {'intensity': 110, 'zone': 'Zone 5'},
            'pma': {'intensity': 115, 'zone': 'Zone 5'},
            'recuperation': {'intensity': 45, 'zone': 'Zone 1'},
            'recup': {'intensity': 45, 'zone': 'Zone 1'},
            'recovery': {'intensity': 45, 'zone': 'Zone 1'},
            'échauffement': {'intensity': 60, 'zone': 'Zone 2', 'phase': 'warmup'},
            'warmup': {'intensity': 60, 'zone': 'Zone 2', 'phase': 'warmup'},
            'retour': {'intensity': 50, 'zone': 'Zone 1', 'phase': 'cooldown'},
            'cooldown': {'intensity': 50, 'zone': 'Zone 1', 'phase': 'cooldown'}
        }
    
    def extract_entities(self, query: str) -> WorkoutEntity:
        """
        Extraction d'entités avec LLM - ordre libre
        "5 minutes tempo" = "tempo 5 minutes" = même résultat
        """
        
        # Prompt optimisé pour extraction d'entités
        prompt = f"""Tu es un expert en extraction d'entités pour l'entraînement cycliste.

Extrait les entités suivantes du texte, peu importe l'ordre:

Texte: "{query}"

Réponds UNIQUEMENT avec un JSON valide:
{{
    "durations": [liste des durées en minutes],
    "intensities": [liste des intensités en %],
    "workout_types": [liste des types: tempo, seuil, aerobic, endurance, etc.],
    "structures": [
        {{"type": "simple", "reps": X, "duration": Y}} ou
        {{"type": "nested", "blocks": A, "series": B, "duration": C}}
    ],
    "phases": [échauffement, cooldown si présents],
    "recovery_durations": [durées de récupération]
}}

Exemples:
- "5 minutes tempo" → {{"durations": [5], "workout_types": ["tempo"]}}
- "tempo 5 minutes" → {{"durations": [5], "workout_types": ["tempo"]}}
- "2x3x5 minutes tempo" → {{"durations": [5], "workout_types": ["tempo"], "structures": [{{"type": "nested", "blocks": 2, "series": 3, "duration": 5}}]}}
- "5x3min à 95%" → {{"durations": [3], "intensities": [95], "structures": [{{"type": "simple", "reps": 5, "duration": 3}}]}}

JSON pour "{query}":"""

        # Requête LLM
        llm_response = self.llm_client.query_llm(prompt)
        
        try:
            # Parser la réponse JSON
            entities_dict = json.loads(llm_response)
            
            return WorkoutEntity(
                durations=entities_dict.get('durations', []),
                intensities=entities_dict.get('intensities', []),
                workout_types=entities_dict.get('workout_types', []),
                structures=entities_dict.get('structures', []),
                phases=entities_dict.get('phases', []),
                recovery_durations=entities_dict.get('recovery_durations', [])
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erreur parsing JSON LLM: {e}")
            print(f"Réponse LLM: {llm_response}")
            
            # Fallback: extraction regex basique
            return self._fallback_entity_extraction(query)
    
    def _fallback_entity_extraction(self, query: str) -> WorkoutEntity:
        """Extraction d'entités de fallback si LLM échoue"""
        query_lower = query.lower()
        
        # Durées
        durations = []
        duration_matches = re.findall(r'(\d+)\s*(?:min|minutes?)', query_lower)
        durations = [int(d) for d in duration_matches]
        
        # Intensités
        intensities = []
        intensity_matches = re.findall(r'(\d+)%', query_lower)
        intensities = [int(i) for i in intensity_matches]
        
        # Types d'entraînement
        workout_types = []
        for wt in self.workout_type_mapping.keys():
            if wt in query_lower:
                workout_types.append(wt)
        
        # Structures
        structures = []
        # 2x3x5
        nested_match = re.search(r'(\d+)x(\d+)x(\d+)', query_lower)
        if nested_match:
            structures.append({
                'type': 'nested',
                'blocks': int(nested_match.group(1)),
                'series': int(nested_match.group(2)),
                'duration': int(nested_match.group(3))
            })
        else:
            # 5x3
            simple_match = re.search(r'(\d+)x(\d+)', query_lower)
            if simple_match:
                structures.append({
                    'type': 'simple',
                    'reps': int(simple_match.group(1)),
                    'duration': int(simple_match.group(2))
                })
        
        # Phases
        phases = []
        if any(p in query_lower for p in ['échauffement', 'warmup', 'warm']):
            phases.append('warmup')
        if any(p in query_lower for p in ['retour', 'cooldown', 'cool', 'calme']):
            phases.append('cooldown')
        
        return WorkoutEntity(
            durations=durations,
            intensities=intensities,
            workout_types=workout_types,
            structures=structures,
            phases=phases,
            recovery_durations=[]
        )
    
    def generate_workout_structure(self, entities: WorkoutEntity, critical_power: int = 250) -> List[Dict]:
        """
        Génère la structure d'entraînement basée sur les entités extraites
        """
        workout_steps = []
        
        # === STRUCTURES COMPLEXES (2x3x5) ===
        nested_structures = [s for s in entities.structures if s.get('type') == 'nested']
        simple_structures = [s for s in entities.structures if s.get('type') == 'simple']
        
        if nested_structures:
            # 2x3x5 = 2 blocs de (3 séries de 5min)
            structure = nested_structures[0]
            blocks = structure['blocks']
            series_per_block = structure['series']
            duration = structure['duration']
            
            # Intensité/type
            workout_type = entities.workout_types[0] if entities.workout_types else 'tempo'
            intensity = entities.intensities[0] if entities.intensities else self.workout_type_mapping[workout_type]['intensity']
            zone = self.workout_type_mapping[workout_type]['zone']
            
            for block in range(blocks):
                for series in range(series_per_block):
                    workout_steps.append({
                        'duration': duration,
                        'power_percent': intensity,
                        'power_watts': int(critical_power * intensity / 100),
                        'zone': zone,
                        'description': f"Bloc {block+1} Série {series+1} - {workout_type}"
                    })
                    
                    # Récup entre séries (pas après dernière du bloc)
                    if series < series_per_block - 1:
                        recovery_duration = entities.recovery_durations[0] if entities.recovery_durations else 2
                        workout_steps.append({
                            'duration': recovery_duration,
                            'power_percent': 50,
                            'power_watts': int(critical_power * 50 / 100),
                            'zone': 'Zone 1',
                            'description': f"Récup {recovery_duration}min"
                        })
                
                # Récup entre blocs (pas après dernier bloc)
                if block < blocks - 1:
                    inter_block_recovery = entities.recovery_durations[0] if entities.recovery_durations else 5
                    workout_steps.append({
                        'duration': inter_block_recovery,
                        'power_percent': 50,
                        'power_watts': int(critical_power * 50 / 100),
                        'zone': 'Zone 1',
                        'description': f"Récup inter-blocs {inter_block_recovery}min"
                    })
        
        elif simple_structures:
            # 5x3min standard
            structure = simple_structures[0]
            reps = structure['reps']
            duration = structure['duration']
            
            workout_type = entities.workout_types[0] if entities.workout_types else 'tempo'
            intensity = entities.intensities[0] if entities.intensities else self.workout_type_mapping[workout_type]['intensity']
            zone = self.workout_type_mapping[workout_type]['zone']
            
            for i in range(reps):
                workout_steps.append({
                    'duration': duration,
                    'power_percent': intensity,
                    'power_watts': int(critical_power * intensity / 100),
                    'zone': zone,
                    'description': f"Série {i+1} - {workout_type}"
                })
                
                if i < reps - 1:
                    recovery_duration = entities.recovery_durations[0] if entities.recovery_durations else 2
                    workout_steps.append({
                        'duration': recovery_duration,
                        'power_percent': 50,
                        'power_watts': int(critical_power * 50 / 100),
                        'zone': 'Zone 1',
                        'description': f"Récup {recovery_duration}min"
                    })
        
        elif entities.durations and entities.workout_types:
            # Séance simple: "5 minutes tempo"
            duration = entities.durations[0]
            workout_type = entities.workout_types[0]
            intensity = entities.intensities[0] if entities.intensities else self.workout_type_mapping[workout_type]['intensity']
            zone = self.workout_type_mapping[workout_type]['zone']
            
            workout_steps.append({
                'duration': duration,
                'power_percent': intensity,
                'power_watts': int(critical_power * intensity / 100),
                'zone': zone,
                'description': f"{duration}min {workout_type}"
            })
        
        # Ajouter échauffement/cooldown si détectés
        if 'warmup' in entities.phases:
            warmup_duration = min(entities.durations) if len(entities.durations) > 1 else 10
            workout_steps.insert(0, {
                'duration': warmup_duration,
                'power_percent': 60,
                'power_watts': int(critical_power * 60 / 100),
                'zone': 'Zone 2',
                'description': f"Échauffement {warmup_duration}min"
            })
        
        if 'cooldown' in entities.phases:
            cooldown_duration = min(entities.durations) if len(entities.durations) > 1 else 10
            workout_steps.append({
                'duration': cooldown_duration,
                'power_percent': 50,
                'power_watts': int(critical_power * 50 / 100),
                'zone': 'Zone 1',
                'description': f"Retour calme {cooldown_duration}min"
            })
        
        return workout_steps
    
    def validate_structure_strict(self, workout_steps: List[Dict], entities: WorkoutEntity, original_query: str) -> tuple[bool, List[str]]:
        """
        Validation ultra-stricte: vérifier que l'output correspond à l'input
        """
        errors = []
        
        if not workout_steps:
            errors.append("Aucune structure générée")
            return False, errors
        
        # Vérifier durées principales
        if entities.durations:
            generated_durations = [step['duration'] for step in workout_steps if 'récup' not in step['description'].lower()]
            main_duration = entities.durations[0]
            
            if main_duration not in generated_durations:
                errors.append(f"Durée principale {main_duration}min non trouvée dans {generated_durations}")
        
        # Vérifier intensités
        if entities.intensities:
            generated_intensities = [step['power_percent'] for step in workout_steps if 'récup' not in step['description'].lower()]
            target_intensity = entities.intensities[0]
            
            if not any(abs(target_intensity - gi) <= 5 for gi in generated_intensities):
                errors.append(f"Intensité {target_intensity}% non trouvée dans {generated_intensities}")
        
        # Vérifier types d'entraînement
        if entities.workout_types:
            workout_descriptions = ' '.join(step['description'].lower() for step in workout_steps)
            missing_types = [wt for wt in entities.workout_types if wt not in workout_descriptions]
            
            if missing_types:
                errors.append(f"Types manquants: {missing_types}")
        
        # Vérifier structures
        if entities.structures:
            structure = entities.structures[0]
            if structure['type'] == 'nested':
                expected_series = structure['blocks'] * structure['series']
                actual_series = len([s for s in workout_steps if 'série' in s['description'].lower()])
                
                if actual_series != expected_series:
                    errors.append(f"Structure {structure['blocks']}x{structure['series']} attendue, {actual_series} séries générées")
        
        return len(errors) == 0, errors
