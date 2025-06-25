#!/usr/bin/env python3
"""
Vekta V2 - Interface Simple
Interface épurée sans étapes détaillées
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os
import sys
import time

# Import du parser intelligent
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
components_path = os.path.join(parent_dir, 'components')
sys.path.insert(0, components_path)

try:
    from llm_parser_simple import IntelligentWorkoutParser, WorkoutEntity
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
    st.stop()

# Configuration
st.set_page_config(
    page_title="🚴‍♂️ Vekta V2 - Générateur d'Entraînements",
    page_icon="🚴‍♂️",
    layout="wide"
)

# CSS Simple
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .workout-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Interface sans sidebar - plus épurée

def show_system_info():
    """Affiche les informations système pour Mac M3"""
    with st.expander("🖥️ Informations Système", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🧠 Modèle IA:**")
            st.markdown("- Modèle: `llama3.2:3b`")
            st.markdown("- Paramètres: 3 milliards")
            st.markdown("- Optimisé pour: Mac M3")
            
        with col2:
            st.markdown("**⚙️ Configuration:**")
            st.markdown("- Moteur: Ollama local")
            st.markdown("- Mémoire: Optimisée")
            st.markdown("- Performance: Locale")
            
        # Vérification de la connexion Ollama
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                st.success("✅ Ollama connecté et fonctionnel")
                models = response.json().get("models", [])
                if models:
                    st.markdown("**Modèles disponibles:**")
                    for model in models:
                        model_name = model.get("name", "Unknown")
                        if "llama3.2:3b" in model_name:
                            st.markdown(f"- ✅ {model_name}")
                        else:
                            st.markdown(f"- {model_name}")
            else:
                st.error("❌ Ollama non disponible")
        except:
            st.warning("⚠️ Impossible de vérifier Ollama")

def format_time(minutes):
    """Convertit les minutes en format HH:MM:SS"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}:00"

def get_zone_name(power_percent):
    """Détermine le nom de la zone basé sur le pourcentage"""
    if power_percent < 55:
        return "recovery"
    elif power_percent < 75:
        return "aerobic"
    elif power_percent < 90:
        return "tempo"
    elif power_percent < 105:
        return "threshold"
    else:
        return "vo2max"

def generate_detailed_steps(workout_steps, critical_power):
    """Génère un descriptif détaillé des étapes"""
    detailed_steps = []
    
    for step in workout_steps:
        duration_formatted = format_time(step['duration'])
        power_percent = step['power_percent']
        zone_name = get_zone_name(power_percent)
        
        # Calcul des plages de puissance
        min_watts = int(critical_power * (power_percent - 10) / 100) if power_percent > 10 else 0
        max_watts = int(critical_power * (power_percent + 15) / 100)
        min_percent = max(0, power_percent - 10)
        max_percent = power_percent + 15
        
        step_info = {
            'description': step['description'],
            'duration': duration_formatted,
            'zone': zone_name,
            'power_range': f"{min_watts} - {max_watts} W",
            'percent_range': f"{min_percent} - {max_percent} % CP"
        }
        
        detailed_steps.append(step_info)
    
    return detailed_steps

def create_zwift_workout(workout_steps, workout_name="Vekta Custom Workout"):
    """Génère un fichier de workout Zwift au format ZWO"""
    zwift_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<workout_file>
    <author>Vekta V2</author>
    <name>{workout_name}</name>
    <description>Entraînement généré par Vekta V2</description>
    <sportType>bike</sportType>
    <tags>
        <tag name="Custom"/>
        <tag name="Vekta"/>
    </tags>
    <workout>
'''
    
    for step in workout_steps:
        duration_seconds = step['duration'] * 60
        power_percent = step['power_percent'] / 100  # Zwift utilise 0.0-1.0
        
        # Détermine le type d'effort
        if 'récup' in step['description'].lower() or 'recovery' in step['description'].lower():
            zwift_xml += f'        <Ramp Duration="{duration_seconds}" PowerLow="{power_percent:.2f}" PowerHigh="{power_percent:.2f}"/>\n'
        else:
            zwift_xml += f'        <SteadyState Duration="{duration_seconds}" Power="{power_percent:.2f}"/>\n'
    
    zwift_xml += '''    </workout>
</workout_file>'''
    
    return zwift_xml

def get_power_zone_color(zone):
    """Couleurs des zones de puissance - palette cycliste professionnelle"""
    colors = {
        "Zone 1": "#94a3b8",    # Gris clair - Récupération active
        "Zone 2": "#60a5fa",    # Bleu - Endurance aérobie  
        "Zone 3": "#34d399",    # Vert - Tempo
        "Zone 4": "#fbbf24",    # Orange - Seuil lactique
        "Zone 5": "#f87171",    # Rouge - VO2max
        "Zone 6": "#a78bfa",    # Violet - Capacité anaérobie
        "Zone 7": "#fb7185",    # Rose - Puissance neuromusculaire
        # Zones nommées
        "recovery": "#94a3b8",
        "aerobic": "#60a5fa", 
        "tempo": "#34d399",
        "threshold": "#fbbf24",
        "vo2max": "#f87171",
        "anaerobic": "#a78bfa",
        "neuromuscular": "#fb7185"
    }
    return colors.get(zone, "#6b7280")

def create_simple_power_chart(workout_steps, critical_power=250):
    """Graphique de puissance interactif avec couleurs par zone et hover détaillé"""
    if not workout_steps:
        return None
    
    # Préparation des données pour les barres
    times = []
    powers = []
    zones = []
    colors = []
    durations = []
    percentages = []
    descriptions = []
    hover_texts = []
    
    current_time = 0
    
    for step in workout_steps:
        duration = step.get('duration', 0)
        power_percent = step.get('power_percent', 70)
        power_watts = int(critical_power * power_percent / 100)
        zone = get_zone_name(power_percent)
        description = step.get('description', '').replace(' - Zone', ' -')
        color = get_power_zone_color(zone)
        
        # Point de départ
        times.append(current_time)
        powers.append(power_watts)
        zones.append(zone)
        colors.append(color)
        durations.append(duration)
        percentages.append(power_percent)
        descriptions.append(description)
        
        # Texte hover détaillé
        hover_text = f"""
<b>{description}</b><br>
<b>Zone:</b> {zone}<br>
<b>Durée:</b> {duration} min<br>
<b>Puissance:</b> {power_watts}W ({power_percent}% CP)<br>
<b>Temps:</b> {current_time}min → {current_time + duration}min
""".strip()
        hover_texts.append(hover_text)
        
        # Point de fin (même puissance)
        current_time += duration
        times.append(current_time)
        powers.append(power_watts)
        zones.append(zone)
        colors.append(color)
        durations.append(duration)
        percentages.append(power_percent)
        descriptions.append(description)
        hover_texts.append(hover_text)
    
    fig = go.Figure()
    
    # Créer les segments comme des barres individuelles avec hover
    step_index = 0
    legend_zones = set()
    
    for i in range(0, len(times)-1, 2):
        start_time = times[i]
        end_time = times[i+1]
        power = powers[i]
        zone = zones[i]
        color = colors[i]
        hover_text = hover_texts[i]
        
        # Créer un rectangle pour chaque segment
        fig.add_trace(go.Scatter(
            x=[start_time, end_time, end_time, start_time, start_time],
            y=[0, 0, power, power, 0],
            fill='toself',
            fillcolor=color,
            line=dict(color=color, width=2),
            mode='lines',
            name=zone if zone not in legend_zones else "",
            showlegend=zone not in legend_zones,
            hovertemplate=hover_text + '<extra></extra>',
            opacity=0.85
        ))
        
        legend_zones.add(zone)
        step_index += 1
    
    # Configuration du layout
    max_power = max(powers) if powers else 250
    total_time = times[-1] if times else 30
    
    fig.update_layout(
        title={
            'text': "🚴 Profil de Puissance Interactive",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        xaxis_title="Temps (minutes)",
        yaxis_title="Puissance (Watts)",
        height=450,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(
            range=[0, total_time],
            gridcolor="lightgray",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max_power + 50],
            gridcolor="lightgray",
            showgrid=True,
            zeroline=False
        ),
        plot_bgcolor="white",
        hovermode='closest'
    )
    
    return fig

def calculate_session_metrics(workout_steps, critical_power):
    """Calcule les métriques complètes de la séance"""
    if not workout_steps:
        return {}
    
    total_duration_min = sum(step['duration'] for step in workout_steps)
    total_duration_hours = total_duration_min // 60
    total_duration_mins = total_duration_min % 60
    total_duration_formatted = f"{total_duration_hours:02d}:{total_duration_mins:02d}:00"
    
    # Calcul de la puissance moyenne pondérée - convertir power_percent en watts
    total_energy = sum((step['power_percent'] / 100 * critical_power) * step['duration'] for step in workout_steps)
    avg_power = int(total_energy / total_duration_min) if total_duration_min > 0 else 0
    
    # Calcul du travail total (kJ) - 1W pendant 1min = 0.06 kJ
    total_work = int(total_energy * 0.06)  # kJ
    
    # Estimation des calories actives (approximation: 1 kJ ≈ 1 kcal pour le cyclisme)
    active_calories = total_work
    
    # Détermine le stimulus d'entraînement dominant
    work_steps = [s for s in workout_steps if 'récup' not in s['description'].lower()]
    if work_steps:
        # Calcule le temps passé dans chaque zone
        zone_times = {}
        for step in work_steps:
            power_percent = step['power_percent']
            duration = step['duration']
            
            if power_percent >= 105:
                zone = "vo2max"
            elif power_percent >= 90:
                zone = "threshold"
            elif power_percent >= 75:
                zone = "tempo"
            elif power_percent >= 55:
                zone = "aerobic"
            else:
                zone = "recovery"
                
            zone_times[zone] = zone_times.get(zone, 0) + duration
        
        # Zone dominante = celle avec le plus de temps
        dominant_zone = max(zone_times.keys(), key=lambda k: zone_times[k]) if zone_times else "aerobic"
        training_stimulus = dominant_zone
    else:
        training_stimulus = "recovery"
    
    return {
        'total_duration': total_duration_formatted,
        'total_distance': "—",  # Non calculable sans vitesse
        'avg_power': f"{avg_power} W",
        'total_work': f"{total_work} kJ",
        'training_stimulus': training_stimulus,
        'active_calories': f"{active_calories} kcal",
        'elevation_gain': "—",  # Non applicable pour l'indoor
        'rpe': "—"  # Non calculable automatiquement
    }

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Vekta V2</h1>
    <p>Générateur d'Entraînements Intelligents pour Mac M3</p>
</div>
""", unsafe_allow_html=True)

# Informations système Mac M3
show_system_info()

# Interface principale

# Info intelligence sémantique en haut
st.info("🧠 **Parser Hiérarchique Ultra-Intelligent Activé** - Comprend les structures complexes imbriquées, blocs répétés, intervalles et langage familier")

# Définir critical_power par défaut pour éviter l'erreur
critical_power = 250

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💬 Décrivez votre séance")
    
    with st.form("workout_form"):
        query = st.text_area(
            "Que voulez-vous faire aujourd'hui ?",
            placeholder="Ex: je doie faire 10 min chofe, apres 3 set de 5 mn a fond et 2 min pose...",
            height=120,
            help="Utilisez votre langage naturel ! L'IA comprend les fautes d'orthographe et le langage familier."
        )
        
        col_cp, col_btn = st.columns([1, 1])
        with col_cp:
            critical_power = st.number_input("⚡ Critical Power (W)", min_value=100, max_value=500, value=250)
        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)  # Espacement
            submit = st.form_submit_button("🚀 Générer l'entraînement", use_container_width=True)

with col2:
    st.subheader("📊 Zones de Puissance")
    
    zones_data = {
        "Zone": ["Z1", "Z2", "Z3", "Z4", "Z5"],
        "Intensité": ["< 55%", "55-75%", "75-90%", "90-105%", "> 105%"],
        "Puissance": [
            f"< {int(critical_power * 0.55)}W",
            f"{int(critical_power * 0.55)}-{int(critical_power * 0.75)}W", 
            f"{int(critical_power * 0.75)}-{int(critical_power * 0.90)}W",
            f"{int(critical_power * 0.90)}-{int(critical_power * 1.05)}W",
            f"> {int(critical_power * 1.05)}W"
        ]
    }
    
    df_zones = pd.DataFrame(zones_data)
    st.dataframe(df_zones, use_container_width=True, hide_index=True)
    
    # Exemples d'utilisation
    with st.expander("💡 Exemples Ultra-Intelligents"):
        st.markdown("""
        **Structures Complexes Supportées :**
        - "10 min échauffement, puis 2 blocs. Chaque bloc: 3 répétitions de (2 min VO2max, 1 min récup), puis 5 min endurance. 10 min retour au calme"
        - "3x(4x30s à fond + 30s récup) avec 5min entre séries"
        - "Pyramide: 1-2-3-4-3-2-1 min seuil, 1min récup entre chaque"
        
        **Langage Familier :**
        - "chofe/chaude" → Échauffement
        - "à fond/max" → VO2max  
        - "pose/pause" → Récupération
        - Fautes d'orthographe auto-corrigées
        """)

# Traitement de la requête
if submit and query:
    try:
        # Initialiser le parser hiérarchique ultra-intelligent
        parser = IntelligentWorkoutParser()
        
        with st.spinner("🧠 Parsing Hiérarchique Multi-Phase en cours..."):
            start_time = time.time()
            
            # Parse complet avec nouvelle architecture
            workout_steps, metadata = parser.parse_workout(query)
            
            generation_time = time.time() - start_time
    
    except Exception as e:
        if "Ollama" in str(e):
            st.error(f"""
            ### ❌ Ollama Requis pour Vekta V2

            **Ollama est obligatoire** pour faire fonctionner le pipeline Vekta V2.

            #### 🚀 Solution recommandée :
            **Utilisez le lanceur automatique** qui configure tout pour vous :
            ```bash
            python launch_vekta_v2.py
            ```

            #### 🔧 Ou installation manuelle :

            1. **Installez Ollama :**
               ```
               https://ollama.ai
               ```

            2. **Démarrez le service :**
               ```
               ollama serve
               ```

            3. **Relancez Vekta V2**
               (Le modèle sera installé automatiquement à la première utilisation)

            ---
            **Erreur technique :** {str(e)}
            """)
        else:
            st.error(f"❌ Erreur inattendue : {str(e)}")
        
        st.stop()
        
        # Affichage du mode de parsing utilisé
        if metadata.get('source') == 'llm_hierarchical':
            st.success(f"✅ LLM Hiérarchique utilisé - {len(workout_steps)} étapes générées")
        elif metadata.get('source') == 'semantic_blocks':
            st.info(f"🧠 Parsing Sémantique Avancé - {metadata.get('block_count', 0)} blocs détectés")
        else:
            st.info("🎯 Parsing Sémantique Standard")
    
    if workout_steps:
        st.markdown("---")
        

        
        # Section Generated Session
        st.markdown("### Generated Session")
        session_metrics = calculate_session_metrics(workout_steps, critical_power)
        
        # Affichage en 2 lignes × 4 colonnes comme dans l'image
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='text-align: left;'>
                <small style='color: #666;'>Total Duration</small><br>
                <strong style='font-size: 24px;'>{session_metrics['total_duration']}</strong><br><br>
                <small style='color: #666;'>Total Distance</small><br>
                <strong style='font-size: 24px;'>{session_metrics['total_distance']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: left;'>
                <small style='color: #666;'>Average Power</small><br>
                <strong style='font-size: 24px;'>{session_metrics['avg_power']}</strong><br><br>
                <small style='color: #666;'>Total Work</small><br>
                <strong style='font-size: 24px;'>{session_metrics['total_work']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='text-align: left;'>
                <small style='color: #666;'>Training Stimulus</small><br>
                <strong style='font-size: 24px;'>{session_metrics['training_stimulus']}</strong><br><br>
                <small style='color: #666;'>Active Calories</small><br>
                <strong style='font-size: 24px;'>{session_metrics['active_calories']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='text-align: left;'>
                <small style='color: #666;'>Elevation Gain</small><br>
                <strong style='font-size: 24px;'>{session_metrics['elevation_gain']}</strong><br><br>
                <small style='color: #666;'>RPE</small><br>
                <strong style='font-size: 24px;'>{session_metrics['rpe']}</strong>
            </div>
                         """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Affichage Steps et Chart côte à côte comme dans l'image
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### Steps")
            detailed_steps = generate_detailed_steps(workout_steps, critical_power)
            
            # Rendu intelligent basé sur la structure générée par le parser
            steps_text = ""
            
            # Détection intelligente de la structure selon metadata
            if metadata.get('source') == 'semantic_blocks':
                # Structure en blocs - rendu hiérarchique
                block_count = metadata.get('block_count', 0)
                if block_count > 1:
                    steps_text += f"• {block_count} x\n"
                
                current_block = None
                in_block_intervals = False
                interval_count = 0
                
                for step_detail in detailed_steps:
                    description = step_detail['description']
                    step_type = None
                    
                    # Détermine le type d'étape selon la description
                    if 'échauffement' in description.lower() or 'warmup' in description.lower():
                        step_type = 'warmup'
                    elif 'bloc' in description.lower() and ('interval' in description.lower() or 'vo2max' in description.lower()):
                        step_type = 'block_interval'
                    elif 'récup' in description.lower() and 'bloc' not in description.lower():
                        step_type = 'recovery'
                    elif 'endurance' in description.lower() and 'bloc' in description.lower():
                        step_type = 'block_endurance'
                    elif 'retour' in description.lower() or 'cooldown' in description.lower():
                        step_type = 'cooldown'
                    else:
                        step_type = 'active'
                    
                    # Rendu selon le type
                    if step_type == 'warmup':
                        steps_text += f"• warm up: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    
                    elif step_type == 'block_interval':
                        # Nouveau bloc détecté
                        if not in_block_intervals:
                            steps_text += "  ° 3 x\n"
                            in_block_intervals = True
                            interval_count = 0
                        
                        interval_count += 1
                        steps_text += f"    ▪ active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    
                    elif step_type == 'recovery' and in_block_intervals:
                        steps_text += f"    ▪ intra-recovery: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    
                    elif step_type == 'block_endurance':
                        in_block_intervals = False
                        steps_text += f"  ° active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    
                    elif step_type == 'cooldown':
                        steps_text += f"• cool down: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    
                    else:
                        steps_text += f"• active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
            
            elif metadata.get('source') == 'semantic_intervals':
                # Structure d'intervalles - rendu simple mais intelligent
                pattern = metadata.get('pattern', '')
                
                # Détecte le nombre de répétitions
                reps_count = len([s for s in workout_steps if 'set' in s.get('description', '').lower() or 'interval' in s.get('description', '').lower()])
                if reps_count > 1:
                    steps_text += f"• {reps_count} x\n"
                
                for step_detail in detailed_steps:
                    description = step_detail['description'].lower()
                    
                    if 'échauffement' in description or 'warmup' in description:
                        steps_text += f"• warm up: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    elif 'set' in description or 'interval' in description:
                        steps_text += f"  ° active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    elif 'récup' in description:
                        steps_text += f"  ° intra-recovery: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    elif 'retour' in description or 'cooldown' in description:
                        steps_text += f"• cool down: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    else:
                        steps_text += f"• active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
            
            else:
                # Structure linéaire simple - rendu direct
                for step_detail in detailed_steps:
                    description = step_detail['description'].lower()
                    
                    if 'échauffement' in description or 'warmup' in description:
                        steps_text += f"• warm up: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    elif 'retour' in description or 'cooldown' in description:
                        steps_text += f"• cool down: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
                    else:
                        steps_text += f"• active: {step_detail['duration']} - {step_detail['zone']} / {step_detail['power_range']} / {step_detail['percent_range']}\n"
            
            st.markdown(f"```\n{steps_text}\n```")
        
        with col_right:
            st.markdown("### Chart")
            # Graphique
            chart = create_simple_power_chart(workout_steps, critical_power)
            if chart:
                st.plotly_chart(chart, use_container_width=True)
        
        # Bouton de téléchargement Zwift
        zwift_content = create_zwift_workout(workout_steps, f"Vekta - {query[:30]}...")
        st.download_button(
            label="📥 Télécharger pour Zwift (.zwo)",
            data=zwift_content,
            file_name=f"vekta_workout_{int(time.time())}.zwo",
            mime="application/xml",
            use_container_width=True
        )
        

    else:
        st.error("❌ Impossible de générer l'entraînement")

# Footer simple
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1rem;'>
    🧠 <strong>Vekta V2</strong> - Interface Simple
</div>
""", unsafe_allow_html=True) 