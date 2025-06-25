#!/usr/bin/env python3
"""
Parser Hiérarchique Multi-Phase Ultra-Intelligent pour Vekta V2
Gère les structures complexes imbriquées avec LLM + analyse compositionnelle
"""

import json
import re
import requests
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass

@dataclass
class WorkoutEntity:
    """Entité d'entraînement extraite avec structures hiérarchiques"""
    durations: List[int]
    intensities: List[int]  
    workout_types: List[str]
    structures: List[Dict]
    phases: List[str]
    recovery_durations: List[int]
    hierarchical_structure: Optional[Dict] = None

@dataclass
class WorkoutBlock:
    """Bloc d'entraînement avec structure interne"""
    name: str
    repetitions: int
    components: List[Dict]
    total_duration: int

class OllamaLLMClient:
    """Client pour Ollama local optimisé pour Mac M3"""
    
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.base_url = "http://localhost:11434"
    
    def query_llm(self, prompt: str, max_tokens: int = 800) -> str:
        """Requête vers Ollama avec installation automatique du modèle"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.1,
                        "top_p": 0.9
                    }
                },
                timeout=45
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            elif response.status_code == 404:
                # Modèle manquant - installation automatique
                print(f"📥 Modèle {self.model_name} manquant - Installation automatique...")
                if self._auto_install_model():
                    # Retry après installation
                    return self.query_llm(prompt, max_tokens)
                else:
                    raise Exception(f"Impossible d'installer le modèle {self.model_name}")
            else:
                raise Exception(f"Ollama error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama non disponible. Démarrez Ollama avec: ollama serve")
        except Exception as e:
            raise e
    
    def _auto_install_model(self) -> bool:
        """Installation automatique du modèle requis"""
        import subprocess
        
        print(f"⏳ Installation du modèle {self.model_name}... (peut prendre quelques minutes)")
        
        try:
            result = subprocess.run(
                ['ollama', 'pull', self.model_name],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes max
            )
            
            if result.returncode == 0:
                print(f"✅ Modèle {self.model_name} installé avec succès")
                return True
            else:
                print(f"❌ Échec installation: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Timeout lors de l'installation")
            return False
        except Exception as e:
            print(f"❌ Erreur installation: {e}")
            return False

class AdvancedWorkoutParser:
    """Parser Hiérarchique Ultra-Intelligent - Architecture Multi-Phase"""
    
    def __init__(self):
        # Initialiser le client Ollama (test de connexion différé)
        try:
            self.llm_client = OllamaLLMClient()
            print("🧠 Parser Hiérarchique Ultra-Intelligent activé")
        except Exception as e:
            error_msg = f"❌ ERREUR: Impossible d'initialiser le client Ollama!\n\n🔧 Pour démarrer Ollama:\n1. Installez Ollama: https://ollama.ai\n2. Lancez: 'ollama serve'\n\nErreur technique: {e}"
            print(error_msg)
            raise Exception(error_msg)
        
        # Mappings intensités étendus
        self.intensity_mapping = {
            'recovery': {'intensity': 45, 'zone': 'Zone 1', 'description': 'Récupération'},
            'recuperation': {'intensity': 45, 'zone': 'Zone 1', 'description': 'Récupération'},
            'warmup': {'intensity': 60, 'zone': 'Zone 2', 'description': 'Échauffement'},
            'endurance': {'intensity': 65, 'zone': 'Zone 2', 'description': 'Endurance'},
            'aerobic': {'intensity': 70, 'zone': 'Zone 2', 'description': 'Aérobie'},
            'tempo': {'intensity': 82, 'zone': 'Zone 3', 'description': 'Tempo'},
            'threshold': {'intensity': 95, 'zone': 'Zone 4', 'description': 'Seuil'},
            'seuil': {'intensity': 95, 'zone': 'Zone 4', 'description': 'Seuil'},
            'vo2max': {'intensity': 110, 'zone': 'Zone 5', 'description': 'VO2max'},
            'vo2': {'intensity': 110, 'zone': 'Zone 5', 'description': 'VO2max'},
            'cooldown': {'intensity': 50, 'zone': 'Zone 1', 'description': 'Retour au calme'}
        }
        
        # Patterns structurels avancés
        self.structural_patterns = {
            'blocks': r'(\d+)\s*blocs?',
            'repetitions': r'(\d+)\s*répétitions?\s*de',
            'sets': r'(\d+)\s*(?:sets?|séries?|set)\s*de',
            'intervals_x': r'(\d+)\s*[x×]\s*(\d+)\s*(?:min|mn)',  # "3 x 5 min"
            'intervals_x_extended': r'(\d+)\s*[x×]\s*(\d+)\s*(?:min|mn)\s+(\w+)',  # "3 × 10 min threshold"
            'nested_intervals': r'\(([^)]+)\)',
            'each_block': r'chaque\s+bloc\s+(?:consiste\s+en|comprend)',
            'then': r'puis|ensuite|après',
            'duration': r'(\d+)\s*(?:min|minutes?|mn)',
            'word_duration': r'(dix|cinq|deux|trois|quatre|six|sept|huit|neuf|une?)\s*(?:minut|min)'
        }
        
        self.word_to_number = {
            'un': 1, 'une': 1, 'deux': 2, 'trois': 3, 'quatre': 4, 'cinq': 5,
            'six': 6, 'sept': 7, 'huit': 8, 'neuf': 9, 'dix': 10
        }
    
    def parse_workout(self, query: str) -> Tuple[List[Dict], Dict]:
        """Parse complet multi-phase ultra-intelligent"""
        print("🧠 === PARSING HIÉRARCHIQUE MULTI-PHASE ===")
        
        # Phase 1: Analyse structurelle
        structure_analysis = self._analyze_structure(query)
        print(f"📊 Structure détectée: {structure_analysis}")
        
        # Phase 2: Décomposition hiérarchique
        if structure_analysis['is_complex']:
            return self._parse_complex_structure(query, structure_analysis)
        else:
            return self._parse_simple_structure(query)
    
    def _analyze_structure(self, query: str) -> Dict:
        """Phase 1: Analyse structurelle intelligente"""
        analysis = {
            'is_complex': False,
            'has_blocks': False,
            'has_nested_intervals': False,
            'has_repetitions': False,
            'block_count': 0,
            'phases': [],
            'complexity_score': 0
        }
        
        query_lower = query.lower()
        
        # Détection blocs
        block_match = re.search(self.structural_patterns['blocks'], query_lower)
        if block_match:
            analysis['has_blocks'] = True
            analysis['block_count'] = int(block_match.group(1))
            analysis['complexity_score'] += 3
        
        # Détection structures imbriquées
        if re.search(self.structural_patterns['nested_intervals'], query):
            analysis['has_nested_intervals'] = True
            analysis['complexity_score'] += 2
        
        # Détection répétitions/intervalles
        if re.search(self.structural_patterns['repetitions'], query_lower) or \
           re.search(self.structural_patterns['sets'], query_lower) or \
           re.search(self.structural_patterns['intervals_x'], query_lower) or \
           re.search(self.structural_patterns['intervals_x_extended'], query_lower):
            analysis['has_repetitions'] = True
            analysis['complexity_score'] += 2
        
        # Détection "chaque bloc"
        if re.search(self.structural_patterns['each_block'], query_lower):
            analysis['complexity_score'] += 2
        
        # Phases principales
        if any(word in query_lower for word in ['échauff', 'warmup', 'warm']):
            analysis['phases'].append('warmup')
        if any(word in query_lower for word in ['retour', 'cooldown', 'cool']):
            analysis['phases'].append('cooldown')
        
        # Détermination complexité
        analysis['is_complex'] = analysis['complexity_score'] >= 3
        
        return analysis
    
    def _parse_complex_structure(self, query: str, structure_analysis: Dict) -> Tuple[List[Dict], Dict]:
        """Parse structures complexes avec LLM + fallbacks robustes"""
        print("🎯 Parsing structure complexe détectée")
        
        try:
            # Tentative LLM hiérarchique
            return self._llm_hierarchical_parsing(query, structure_analysis)
        except Exception as e:
            print(f"⚠️ LLM parsing échoué: {e}")
            # Fallback parsing sémantique avancé
            print("🔄 Fallback vers parsing sémantique avancé...")
            try:
                return self._advanced_semantic_parsing(query, structure_analysis)
            except Exception as e2:
                print(f"⚠️ Parsing sémantique avancé échoué: {e2}")
                # Fallback final vers génération compositionnelle
                print("🔄 Fallback final vers génération compositionnelle...")
                return self._fallback_compositional_generation(query)
    
    def _check_ollama_connection(self):
        """Vérifie la connexion Ollama avec test simple"""
        try:
            # Test simple de connexion
            import requests
            response = requests.get(f"{self.llm_client.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return True
            else:
                raise Exception(f"Ollama répond mais erreur {response.status_code}")
        except requests.exceptions.ConnectionError:
            raise Exception("Ollama non disponible. Démarrez Ollama avec: ollama serve")
        except Exception as e:
            raise Exception(f"Problème Ollama: {e}")

    def _llm_hierarchical_parsing(self, query: str, structure_analysis: Dict) -> Tuple[List[Dict], Dict]:
        """Parsing LLM hiérarchique en 2 phases"""
        
        # Vérifier la connexion Ollama avant d'essayer
        self._check_ollama_connection()
        
        # Phase LLM 1: Décomposition structurelle
        decomposition_prompt = f"""Analyse cette séance cycliste complexe: "{query}"

DÉCOMPOSE en blocs numérotés avec structure claire:

Exemple de format attendu:
BLOC 1: Échauffement - 10 min aerobic
BLOC 2: Intervalles - 3 répétitions de (2 min vo2max + 1 min récupération)  
BLOC 3: Endurance - 5 min endurance
BLOC 4: Retour au calme - 10 min recovery

Réponds EXACTEMENT dans ce format pour: "{query}"
"""
        
        try:
            decomposition = self.llm_client.query_llm(decomposition_prompt, max_tokens=600)
            print(f"🔍 Décomposition LLM: {decomposition}")
            
            # Phase LLM 2: Génération détaillée
            generation_prompt = f"""À partir de cette décomposition: 
{decomposition}

Génère la structure JSON détaillée:
{{
    "workout_steps": [
        {{"duration": X, "type": "warmup|vo2max|recovery|etc", "power_percent": Y, "description": "..."}},
        ...
    ]
}}

Règles:
- warmup: 60% CP
- vo2max: 110% CP  
- recovery: 45% CP
- endurance: 65% CP
- threshold: 95% CP
- Détaille TOUS les intervalles individuellement
"""
            
            detailed_response = self.llm_client.query_llm(generation_prompt, max_tokens=800)
            return self._parse_llm_response(detailed_response, query)
            
        except Exception as e:
            error_msg = f"❌ ERREUR LLM: {e}\n\n🔧 Vérifiez qu'Ollama fonctionne avec: 'ollama serve'"
            print(error_msg)
            raise Exception(error_msg)
    
    def _parse_llm_response(self, response: str, original_query: str) -> Tuple[List[Dict], Dict]:
        """Parse la réponse LLM et extrait la structure avec fallback robuste"""
        try:
            # Nettoyage de la réponse
            response = response.strip()
            
            # Extraction JSON avec plusieurs tentatives
            json_attempts = [
                # Tentative 1: JSON complet
                (response.find('{'), response.rfind('}') + 1),
                # Tentative 2: JSON sur une seule ligne
                (response.find('{"workout_steps"'), response.find('}]}')+3),
                # Tentative 3: Chercher après les deux-points
                (response.find(':{'), response.rfind('}') + 1)
            ]
            
            for json_start, json_end in json_attempts:
                if json_start != -1 and json_end > json_start:
                    try:
                        json_str = response[json_start:json_end]
                        
                        # Nettoyage du JSON
                        json_str = json_str.replace('\n', ' ')
                        json_str = re.sub(r'\s+', ' ', json_str)
                        json_str = json_str.replace('" }', '"}')
                        json_str = json_str.replace('" ]', '"]')
                        
                        parsed = json.loads(json_str)
                        
                        if 'workout_steps' in parsed and isinstance(parsed['workout_steps'], list):
                            steps = parsed['workout_steps']
                            metadata = {'source': 'llm_hierarchical', 'original_query': original_query}
                            print(f"✅ LLM généré {len(steps)} étapes")
                            return steps, metadata
                    except json.JSONDecodeError:
                        continue
            
            # Si JSON échoue, parsing manuel de la décomposition
            print("⚠️ JSON invalide, parsing manuel de la décomposition...")
            return self._parse_decomposition_manually(response, original_query)
            
        except Exception as e:
            print(f"⚠️ Parsing LLM échoué: {e}")
            print("🔄 Fallback vers parsing sémantique...")
            # Fallback total vers parsing sémantique
            return self._fallback_compositional_generation(original_query)
    
    def _parse_decomposition_manually(self, decomposition: str, original_query: str) -> Tuple[List[Dict], Dict]:
        """Parse manuellement la décomposition en blocs"""
        print("🔧 Parsing manuel de la décomposition...")
        
        workout_steps = []
        metadata = {'source': 'llm_manual_parsing', 'original_query': original_query}
        
        # Extraction des blocs
        bloc_pattern = r'BLOC\s*(\d+)\s*:\s*([^-]+)-\s*(.+)'
        blocs = re.findall(bloc_pattern, decomposition)
        
        for bloc_num, bloc_type, bloc_description in blocs:
            bloc_type = bloc_type.strip().lower()
            description = bloc_description.strip()
            
            # Parsing de chaque type de bloc
            if 'échauffement' in bloc_type or 'warmup' in bloc_type:
                duration_match = re.search(r'(\d+)\s*min', description)
                duration = int(duration_match.group(1)) if duration_match else 10
                
                workout_steps.append({
                    'duration': duration,
                    'type': 'warmup',
                    'power_percent': 60,
                    'description': f'Échauffement {duration}min - Zone 2'
                })
                
            elif 'intervalles' in bloc_type or 'intervals' in bloc_type:
                # Parsing complexe des intervalles
                rep_match = re.search(r'(\d+)\s*répétitions?\s*de', description)
                work_match = re.search(r'(\d+)\s*min\s*(vo2max|seuil|threshold)', description)
                recovery_match = re.search(r'(\d+)\s*min\s*(récupération|recovery)', description)
                
                if rep_match and work_match:
                    repetitions = int(rep_match.group(1))
                    work_duration = int(work_match.group(1))
                    work_intensity = work_match.group(2).lower()
                    recovery_duration = int(recovery_match.group(1)) if recovery_match else 1
                    
                    # Mapping intensités
                    intensity_map = {
                        'vo2max': 110,
                        'seuil': 95, 
                        'threshold': 95
                    }
                    power_percent = intensity_map.get(work_intensity, 110)
                    
                    for rep in range(repetitions):
                        # Travail
                        workout_steps.append({
                            'duration': work_duration,
                            'type': work_intensity,
                            'power_percent': power_percent,
                            'description': f'Interval {rep+1}/{repetitions}: {work_duration}min {work_intensity} - Zone 5'
                        })
                        
                        # Récupération (sauf dernière)
                        if rep < repetitions - 1:
                            workout_steps.append({
                                'duration': recovery_duration,
                                'type': 'recovery',
                                'power_percent': 45,
                                'description': f'Récupération {recovery_duration}min - Zone 1'
                            })
                            
            elif 'endurance' in bloc_type:
                duration_match = re.search(r'(\d+)\s*min', description)
                duration = int(duration_match.group(1)) if duration_match else 5
                
                workout_steps.append({
                    'duration': duration,
                    'type': 'endurance',
                    'power_percent': 65,
                    'description': f'Endurance {duration}min - Zone 2'
                })
                
            elif 'retour' in bloc_type or 'cooldown' in bloc_type:
                duration_match = re.search(r'(\d+)\s*min', description)
                duration = int(duration_match.group(1)) if duration_match else 10
                
                workout_steps.append({
                    'duration': duration,
                    'type': 'cooldown',
                    'power_percent': 50,
                    'description': f'Retour au calme {duration}min - Zone 1'
                })
        
        if workout_steps:
            print(f"✅ Parsing manuel réussi: {len(workout_steps)} étapes")
            return workout_steps, metadata
        else:
            # Fallback final
            print("🔄 Fallback vers parsing sémantique...")
            return self._fallback_compositional_generation(original_query)
    
    def _advanced_semantic_parsing(self, query: str, structure_analysis: Dict) -> Tuple[List[Dict], Dict]:
        """Parsing sémantique avancé avec composition hiérarchique"""
        print("🧠 Parsing sémantique hiérarchique avancé")
        
        # Extraction composants
        components = self._extract_workout_components(query)
        
        # Ajouter la requête originale aux composants
        components['_original_query'] = query
        
        # Composition intelligente
        if structure_analysis['has_blocks'] and structure_analysis['block_count'] > 1:
            return self._compose_block_structure(query, components, structure_analysis)
        else:
            return self._compose_linear_structure(components)
    
    def _extract_workout_components(self, query: str) -> Dict:
        """Extraction intelligente de tous les composants"""
        components = {
            'durations': [],
            'intensities': [],
            'repetitions': [],
            'structures': [],
            'phases': {'warmup': None, 'cooldown': None}
        }
        
        # Extraction durées (numériques + textuelles)
        for pattern in [self.structural_patterns['duration'], self.structural_patterns['word_duration']]:
            matches = re.findall(pattern, query.lower())
            for match in matches:
                if match.isdigit():
                    components['durations'].append(int(match))
                elif match in self.word_to_number:
                    components['durations'].append(self.word_to_number[match])
        
        # Extraction intensités avec contexte
        components['intensities'] = self._detect_intensities_with_context(query)
        
        # Extraction répétitions/sets
        rep_patterns = [self.structural_patterns['repetitions'], self.structural_patterns['sets']]
        for pattern in rep_patterns:
            matches = re.findall(pattern, query.lower())
            components['repetitions'].extend([int(m) for m in matches])
        
        # Extraction structures imbriquées
        nested_matches = re.findall(self.structural_patterns['nested_intervals'], query)
        for match in nested_matches:
            components['structures'].append(match)
        
        return components
    
    def _detect_intensities_with_context(self, query: str) -> List[str]:
        """Détection intelligente avec analyse contextuelle"""
        detected = []
        query_lower = query.lower()
        
        # Contexte haute intensité  
        if any(word in query_lower for word in ['vo2max', 'vo2', 'fond', 'max', 'intense']):
            detected.append('vo2max')
        
        # Contexte seuil
        if any(word in query_lower for word in ['seuil', 'threshold', 'effort']):
            detected.append('threshold')
        
        # Contexte endurance/aérobie
        if any(word in query_lower for word in ['endurance', 'aerobic', 'aérobie']):
            detected.append('endurance')
        
        # Contexte récupération
        if any(word in query_lower for word in ['récup', 'pause', 'pose', 'repos', 'recovery']):
            detected.append('recovery')
        
        # Phases spéciales
        if any(word in query_lower for word in ['échauff', 'warmup', 'warm', 'chaude']):
            detected.append('warmup')
        
        if any(word in query_lower for word in ['retour', 'cooldown', 'cool', 'calme']):
            detected.append('cooldown')
        
        return detected
    
    def _compose_block_structure(self, query: str, components: Dict, structure_analysis: Dict) -> Tuple[List[Dict], Dict]:
        """Composition intelligente structure en blocs"""
        print(f"🏗️ Composition {structure_analysis['block_count']} blocs")
        
        workout_steps = []
        metadata = {'source': 'semantic_blocks', 'block_count': structure_analysis['block_count']}
        
        # 1. Échauffement (si présent)
        if 'warmup' in components['intensities']:
            warmup_duration = 10  # défaut
            if components['durations']:
                # Première durée souvent échauffement
                warmup_duration = components['durations'][0]
            
            workout_steps.append({
                'duration': warmup_duration,
                'type': 'warmup',
                'power_percent': 60,
                'description': f'Échauffement {warmup_duration}min - Zone 2'
            })
        
        # 2. Génération des blocs principaux
        block_count = structure_analysis['block_count']
        
        # Analyse de la structure de bloc via regex avancée
        if re.search(r'3\s*répétitions?\s*de\s*\(([^)]+)\)', query.lower()):
            # Structure détectée: "3 répétitions de (2 min VO2max, 1 min récupération)"
            interval_match = re.search(r'(\d+)\s*min\s+vo2max.*?(\d+)\s*min\s+récupération', query.lower())
            if interval_match:
                work_duration = int(interval_match.group(1))
                recovery_duration = int(interval_match.group(2))
                
                for block_num in range(block_count):
                    # Chaque bloc = 3 répétitions
                    for rep in range(3):
                        # Travail VO2max
                        workout_steps.append({
                            'duration': work_duration,
                            'type': 'vo2max',
                            'power_percent': 110,
                            'description': f'Bloc {block_num+1} - Interval {rep+1}/3: {work_duration}min VO2max - Zone 5'
                        })
                        
                        # Récupération (sauf dernière répétition du bloc)
                        if rep < 2:  # Pas de récupération après la 3ème répétition
                            workout_steps.append({
                                'duration': recovery_duration,
                                'type': 'recovery',
                                'power_percent': 45,
                                'description': f'Récupération {recovery_duration}min - Zone 1'
                            })
                    
                    # Endurance après chaque bloc (si mentionnée)
                    if 'endurance' in components['intensities']:
                        endurance_duration = 5  # défaut ou depuis durées détectées
                        workout_steps.append({
                            'duration': endurance_duration,
                            'type': 'endurance',
                            'power_percent': 65,
                            'description': f'Bloc {block_num+1} - Endurance {endurance_duration}min - Zone 2'
                        })
        
        # 3. Retour au calme (si présent)
        if 'cooldown' in components['intensities']:
            cooldown_duration = 10  # défaut
            if len(components['durations']) > 1:
                # Dernière durée souvent cooldown
                cooldown_duration = components['durations'][-1]
            
            workout_steps.append({
                'duration': cooldown_duration,
                'type': 'cooldown',
                'power_percent': 50,
                'description': f'Retour au calme {cooldown_duration}min - Zone 1'
            })
        
        return workout_steps, metadata
    
    def _compose_linear_structure(self, components: Dict) -> Tuple[List[Dict], Dict]:
        """Composition structure linéaire intelligente"""
        workout_steps = []
        original_query = components.get('_original_query', '') or ""
        
        # === DÉTECTION PATTERNS SPÉCIAUX ===
        
        # Pattern "X x Y min intensity" (ex: "3 x 5 min seuil")
        interval_x_match = re.search(self.structural_patterns['intervals_x_extended'], original_query.lower())
        if not interval_x_match:
            interval_x_match = re.search(self.structural_patterns['intervals_x'], original_query.lower())
        
        # Pattern "X set de Y mn intensity"
        set_pattern_match = re.search(r'(\d+)\s*set\s*de\s*(\d+)\s*mn\s*(\w+)', original_query.lower())
        
        if interval_x_match:
            # Parsing "3 x 5 min seuil" ou "3 × 10 min threshold"
            reps = int(interval_x_match.group(1))
            duration = int(interval_x_match.group(2))
            
            # Trouve l'intensité dans la requête
            main_intensity = 'threshold'  # défaut
            if 'vo2max' in components['intensities'] or 'vo2' in components['intensities']:
                main_intensity = 'vo2max'
            elif 'seuil' in components['intensities'] or 'threshold' in components['intensities']:
                main_intensity = 'threshold'
            elif 'tempo' in components['intensities']:
                main_intensity = 'tempo'
            
            # Phases
            if 'warmup' in components['intensities']:
                warmup_duration = components['durations'][0] if components['durations'] else 10
                workout_steps.append({
                    'duration': warmup_duration,
                    'type': 'warmup',
                    'power_percent': 60,
                    'description': f'Échauffement {warmup_duration}min - Zone 2'
                })
            
            # Intervalles
            intensity_data = self.intensity_mapping[main_intensity]
            for rep in range(reps):
                workout_steps.append({
                    'duration': duration,
                    'type': main_intensity,
                    'power_percent': intensity_data['intensity'],
                    'description': f'Interval {rep+1}/{reps}: {duration}min {intensity_data["description"]} - {intensity_data["zone"]}'
                })
                
                # Récupération entre intervalles (sauf dernier)
                if rep < reps - 1:
                    recovery_duration = 2  # défaut
                    workout_steps.append({
                        'duration': recovery_duration,
                        'type': 'recovery',
                        'power_percent': 45,
                        'description': f'Récupération {recovery_duration}min - Zone 1'
                    })
            
            # Cooldown
            if 'cooldown' in components['intensities']:
                cooldown_duration = components['durations'][-1] if len(components['durations']) > 1 else 10
                workout_steps.append({
                    'duration': cooldown_duration,
                    'type': 'cooldown',
                    'power_percent': 50,
                    'description': f'Retour au calme {cooldown_duration}min - Zone 1'
                })
            
            return workout_steps, {'source': 'semantic_intervals', 'pattern': 'x_intervals'}
        
        elif set_pattern_match:
            # Parsing "3 set de 5 mn à fond"
            reps = int(set_pattern_match.group(1))
            duration = int(set_pattern_match.group(2))
            
            # Détecte l'intensité depuis "fond" ou autre
            main_intensity = 'vo2max' if any(word in original_query.lower() for word in ['fond', 'max']) else 'threshold'
            
            # Phases
            if 'warmup' in components['intensities']:
                warmup_duration = next((d for d in components['durations'] if d >= 8 and d <= 15), 10)
                workout_steps.append({
                    'duration': warmup_duration,
                    'type': 'warmup',
                    'power_percent': 60,
                    'description': f'Échauffement {warmup_duration}min - Zone 2'
                })
            
            # Intervalles avec récupération
            intensity_data = self.intensity_mapping[main_intensity]
            recovery_duration = next((d for d in components['durations'] if d <= 3), 2)
            
            for rep in range(reps):
                workout_steps.append({
                    'duration': duration,
                    'type': main_intensity,
                    'power_percent': intensity_data['intensity'],
                    'description': f'Set {rep+1}/{reps}: {duration}min {intensity_data["description"]} - {intensity_data["zone"]}'
                })
                
                if rep < reps - 1:
                    workout_steps.append({
                        'duration': recovery_duration,
                        'type': 'recovery',
                        'power_percent': 45,
                        'description': f'Récupération {recovery_duration}min - Zone 1'
                    })
            
            # Cooldown
            if 'cooldown' in components['intensities']:
                cooldown_duration = next((d for d in components['durations'] if d >= 8), 10)
                workout_steps.append({
                    'duration': cooldown_duration,
                    'type': 'cooldown',
                    'power_percent': 50,
                    'description': f'Retour au calme {cooldown_duration}min - Zone 1'
                })
            
            return workout_steps, {'source': 'semantic_intervals', 'pattern': 'set_intervals'}
        
        # === STRUCTURE LINÉAIRE CLASSIQUE ===
        
        # Si pas assez d'infos, génère structure basique
        if not components['durations'] or not components['intensities']:
            return [{
                'duration': 30,
                'type': 'aerobic',
                'power_percent': 70,
                'description': 'Séance aérobie 30min - Zone 2'
            }], {'source': 'fallback'}
        
        # Structure linéaire basée sur les composants détectés
        durations = components['durations']
        intensities = components['intensities']
        
        for i, intensity in enumerate(intensities):
            duration = durations[i] if i < len(durations) else 10
            intensity_data = self.intensity_mapping.get(intensity, self.intensity_mapping['aerobic'])
            
            workout_steps.append({
                'duration': duration,
                'type': intensity,
                'power_percent': intensity_data['intensity'],
                'description': f'{intensity_data["description"]} {duration}min - {intensity_data["zone"]}'
            })
        
        return workout_steps, {'source': 'semantic_linear'}
    
    def _fallback_compositional_generation(self, query: str) -> Tuple[List[Dict], Dict]:
        """Génération de secours compositionnelle"""
        print("🔄 Génération de secours compositionnelle")
        
        # Parsing basique mais robuste
        components = self._extract_workout_components(query)
        
        if not components['durations']:
            raise ValueError(f"❌ Aucune durée détectée dans: '{query}'")
        
        if not components['intensities']:
            raise ValueError(f"❌ Aucune intensité détectée dans: '{query}'")
        
        return self._compose_linear_structure(components)
    
    def _parse_simple_structure(self, query: str) -> Tuple[List[Dict], Dict]:
        """Parse structures simples avec intelligence sémantique"""
        print("🎯 Parsing structure simple")
        
        components = self._extract_workout_components(query)
        components['_original_query'] = query
        
        # Validation
        if not components['durations'] and not components['intensities']:
            raise ValueError(f"❌ Aucun élément d'entraînement détecté dans: '{query}'")
        
        if components['durations'] and not components['intensities']:
            raise ValueError(f"❌ Durée détectée mais aucune intensité dans: '{query}'")
        
        return self._compose_linear_structure(components)

# Alias pour compatibilité
IntelligentWorkoutParser = AdvancedWorkoutParser 