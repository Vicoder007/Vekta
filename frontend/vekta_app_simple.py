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
components_path = os.path.join(os.path.dirname(current_dir), 'components')
if components_path not in sys.path:
    sys.path.insert(0, components_path)

try:
    from llm_parser import IntelligentWorkoutParser, WorkoutEntity
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
    st.stop()

# Configuration
st.set_page_config(
    page_title="🧠 Vekta V2 - Simple",
    page_icon="🚴",
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

def get_power_zone_color(zone):
    """Couleurs des zones de puissance"""
    colors = {
        "Zone 1": "#6b7280", "Zone 2": "#3b82f6", "Zone 3": "#10b981",
        "Zone 4": "#f59e0b", "Zone 5": "#ef4444", "Zone 6": "#8b5cf6", "Zone 7": "#ec4899"
    }
    return colors.get(zone, "#6b7280")

def create_simple_power_chart(workout_steps, critical_power=250):
    """Graphique de puissance simple"""
    if not workout_steps:
        return None
    
    segments = []
    current_time = 0
    
    for step in workout_steps:
        duration = step.get('duration', 0)
        power_watts = step.get('power_watts', 125)
        zone = step.get('zone', 'Zone 2')
        description = step.get('description', '')
        
        segments.append({
            'start': current_time,
            'end': current_time + duration,
            'power_watts': power_watts,
            'zone': zone,
            'description': description
        })
        current_time += duration
    
    fig = go.Figure()
    
    # Segments colorés
    for segment in segments:
        color = get_power_zone_color(segment['zone'])
        
        fig.add_shape(
            type="rect",
            x0=segment['start'], x1=segment['end'],
            y0=0, y1=segment['power_watts'],
            fillcolor=color, opacity=0.8,
            line=dict(width=2, color=color)
        )
    
    max_power = max([s['power_watts'] for s in segments]) if segments else 250
    fig.update_layout(
        title="🚴 Profil de Puissance",
        xaxis_title="Temps (min)",
        yaxis_title="Puissance (Watts)",
        height=400,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(range=[0, current_time], gridcolor="lightgray"),
        yaxis=dict(range=[0, max_power + 50], gridcolor="lightgray"),
        plot_bgcolor="white"
    )
    
    return fig

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Vekta V2</h1>
    <p>Générateur d'Entraînements Intelligents</p>
</div>
""", unsafe_allow_html=True)

# Interface principale

# Définir critical_power par défaut pour éviter l'erreur
critical_power = 250

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Décrivez votre séance")
    
    with st.form("workout_form"):
        query = st.text_area(
            "Que voulez-vous faire aujourd'hui ?",
            placeholder="Ex: 5 minutes tempo, 2x3x5 minutes seuil, 5x3min à 95%...",
            height=100
        )
        
        col_cp, col_token = st.columns(2)
        with col_cp:
            critical_power = st.number_input("⚡ Critical Power (W)", min_value=100, max_value=500, value=250)
        with col_token:
            hf_token = st.text_input("🔑 Token HF (optionnel)", type="password")
        
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

# Traitement de la requête
if submit and query:
    # Initialiser le parser
    parser = IntelligentWorkoutParser(hf_token if hf_token else None)
    
    with st.spinner("🧠 Génération en cours..."):
        start_time = time.time()
        
        # Extraction + Génération
        entities = parser.extract_entities(query)
        workout_steps = parser.generate_workout_structure(entities, critical_power)
        
        generation_time = time.time() - start_time
    
    if workout_steps:
        st.markdown("---")
        
        # Métriques rapides
        total_duration = sum(step['duration'] for step in workout_steps)
        work_steps = [s for s in workout_steps if 'récup' not in s['description'].lower()]
        avg_power = int(sum(s['power_watts'] * s['duration'] for s in work_steps) / sum(s['duration'] for s in work_steps)) if work_steps else 0
        max_power = max(s['power_watts'] for s in workout_steps)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>⏱️ Durée</h4>
                <h2>{total_duration} min</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>💪 Moy</h4>
                <h2>{avg_power}W</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🔥 Max</h4>
                <h2>{max_power}W</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h4>⚡ Temps</h4>
                <h2>{generation_time:.1f}s</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphique
        chart = create_simple_power_chart(workout_steps, critical_power)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # Résumé textuel simple
        st.markdown(f"""
        <div class="workout-card">
            <h3>📝 Votre Séance</h3>
            <p><strong>Requête:</strong> "{query}"</p>
            <p><strong>Structure générée:</strong> {len(workout_steps)} étapes sur {total_duration} minutes</p>
            <p><strong>Entités détectées:</strong> 
                Durées: {entities.durations}, 
                Types: {entities.workout_types}, 
                Intensités: {entities.intensities}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("❌ Impossible de générer l'entraînement")

# Footer simple
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1rem;'>
    🧠 <strong>Vekta V2</strong> - Interface Simple
</div>
""", unsafe_allow_html=True) 