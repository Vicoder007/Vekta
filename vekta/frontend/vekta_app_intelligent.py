import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime
import time

# Import du nouveau parser intelligent
import sys
sys.path.append('../components')
from llm_parser import IntelligentWorkoutParser, WorkoutEntity

# Configuration
st.set_page_config(
    page_title="Vekta V2 - Intelligence Architecture",
    page_icon="🧠",
    layout="wide"
)

# CSS
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
    
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: bold;
    }
    
    .main-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.9;
    }
    
    .entity-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .step-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .success-alert {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border: none;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .error-alert {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border: none;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .pipeline-step {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .power-zone-1 { color: #6b7280; font-weight: bold; }
    .power-zone-2 { color: #3b82f6; font-weight: bold; }
    .power-zone-3 { color: #10b981; font-weight: bold; }
    .power-zone-4 { color: #f59e0b; font-weight: bold; }
    .power-zone-5 { color: #ef4444; font-weight: bold; }
    .power-zone-6 { color: #8b5cf6; font-weight: bold; }
    .power-zone-7 { color: #ec4899; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def get_power_zone_color(zone):
    """Couleurs des zones de puissance"""
    colors = {
        "Zone 1": "#6b7280", "Zone 2": "#3b82f6", "Zone 3": "#10b981",
        "Zone 4": "#f59e0b", "Zone 5": "#ef4444", "Zone 6": "#8b5cf6", "Zone 7": "#ec4899"
    }
    return colors.get(zone, "#6b7280")

def create_power_chart_intelligent(workout_steps, critical_power=250):
    """Graphique de puissance intelligent"""
    if not workout_steps:
        return None
    
    segments = []
    current_time = 0
    
    for step in workout_steps:
        duration = step.get('duration', 0)
        power_watts = step.get('power_watts', 125)
        power_percent = step.get('power_percent', 50)
        zone = step.get('zone', 'Zone 2')
        description = step.get('description', '')
        
        segments.append({
            'start': current_time,
            'end': current_time + duration,
            'power_watts': power_watts,
            'power_percent': power_percent,
            'zone': zone,
            'description': description,
            'duration': duration
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
        
        # Annotations
        mid_time = (segment['start'] + segment['end']) / 2
        mid_power = segment['power_watts'] / 2
        
        if segment['duration'] >= 3:
            fig.add_annotation(
                x=mid_time, y=mid_power,
                text=f"{segment['power_watts']}W<br>{segment['zone']}",
                showarrow=False,
                font=dict(size=11, color="white"),
                bgcolor="rgba(0,0,0,0.6)",
                bordercolor="white", borderwidth=1
            )
    
    # Hover data
    for segment in segments:
        mid_time = (segment['start'] + segment['end']) / 2
        fig.add_trace(go.Scatter(
            x=[mid_time], y=[segment['power_watts']],
            mode='markers', marker=dict(size=1, opacity=0),
            hovertemplate=(
                f"<b>{segment['description']}</b><br>"
                f"💪 {segment['power_watts']}W ({segment['power_percent']}% FTP)<br>"
                f"🎯 {segment['zone']}<br>"
                f"⏱️ {segment['duration']} min<br>"
                "<extra></extra>"
            ),
            showlegend=False, name=""
        ))
    
    max_power = max([s['power_watts'] for s in segments])
    fig.update_layout(
        title="🚴 Profil de Puissance Intelligent",
        xaxis_title="⏱️ Temps (min)",
        yaxis_title="💪 Puissance (Watts)",
        height=450,
        showlegend=False,
        margin=dict(l=60, r=60, t=60, b=60),
        xaxis=dict(range=[0, current_time], dtick=5, gridcolor="lightgray"),
        yaxis=dict(range=[0, max_power + 50], dtick=50, gridcolor="lightgray"),
        plot_bgcolor="white"
    )
    
    return fig

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Vekta V2</h1>
    <p>Intelligence Architecture - LLM Entity Extraction + RAG Validation</p>
</div>
""", unsafe_allow_html=True)

# Configuration
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Parser Intelligent")
    
    # Configuration HF Token
    hf_token = st.text_input(
        "🔑 Hugging Face API Token (optionnel)",
        type="password",
        help="Token pour LLM Llama-3.1-8B. Laissez vide pour mode fallback."
    )
    
    with st.form("intelligent_workout_form"):
        query = st.text_area(
            "💬 Décrivez votre séance (ordre libre):",
            placeholder="Ex:\n• 5 minutes tempo\n• tempo 5 minutes\n• 2 minutes échauffement aerobic puis 2x3x5 minutes tempo\n• 5x3min à 95% avec 2min récup",
            height=120
        )
        
        critical_power = st.number_input("⚡ Critical Power (W)", min_value=100, max_value=500, value=250)
        
        col_submit, col_example = st.columns([1, 1])
        with col_submit:
            submit = st.form_submit_button("🚀 Parser avec LLM", use_container_width=True)
        with col_example:
            if st.form_submit_button("💡 Exemple Complexe", use_container_width=True):
                st.session_state.example_query = "2 minutes échauffement aerobic puis 2x3x5 minutes tempo"

with col2:
    st.subheader("📊 Zones de Puissance")
    
    zones_data = {
        "Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7"],
        "Intensité": ["< 55%", "55-75%", "75-90%", "90-105%", "105-120%", "120-150%", "> 150%"],
        "Puissance": [
            f"< {int(critical_power * 0.55)}W",
            f"{int(critical_power * 0.55)}-{int(critical_power * 0.75)}W",
            f"{int(critical_power * 0.75)}-{int(critical_power * 0.90)}W",
            f"{int(critical_power * 0.90)}-{int(critical_power * 1.05)}W",
            f"{int(critical_power * 1.05)}-{int(critical_power * 1.20)}W",
            f"{int(critical_power * 1.20)}-{int(critical_power * 1.50)}W",
            f"> {int(critical_power * 1.50)}W"
        ]
    }
    
    df_zones = pd.DataFrame(zones_data)
    st.dataframe(df_zones, use_container_width=True, hide_index=True)

# Utiliser exemple si sélectionné
if hasattr(st.session_state, 'example_query') and st.session_state.example_query:
    query = st.session_state.example_query
    submit = True
    delattr(st.session_state, 'example_query')

# Pipeline de traitement
if submit and query:
    st.markdown("---")
    st.subheader("🔄 Pipeline de Traitement Intelligent")
    
    # Initialiser le parser
    parser = IntelligentWorkoutParser(hf_token if hf_token else None)
    
    # ÉTAPE 1: Extraction d'entités LLM
    with st.container():
        st.markdown("""
        <div class="pipeline-step">
            <h4>1️⃣ Extraction d'Entités avec LLM</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("🧠 LLM analyse la requête..."):
            start_time = time.time()
            entities = parser.extract_entities(query)
            extraction_time = time.time() - start_time
        
        st.markdown(f"""
        <div class="entity-card">
            <h4>🎯 Entités Extraites ({extraction_time:.2f}s)</h4>
            <ul>
                <li><strong>Durées</strong>: {entities.durations} min</li>
                <li><strong>Intensités</strong>: {entities.intensities} %</li>
                <li><strong>Types</strong>: {entities.workout_types}</li>
                <li><strong>Structures</strong>: {len(entities.structures)} trouvée(s)</li>
                <li><strong>Phases</strong>: {entities.phases}</li>
                <li><strong>Récupérations</strong>: {entities.recovery_durations} min</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Détail des structures
        if entities.structures:
            for i, structure in enumerate(entities.structures):
                if structure['type'] == 'nested':
                    st.info(f"🔗 Structure {i+1}: {structure['blocks']} blocs × {structure['series']} séries × {structure['duration']}min")
                else:
                    st.info(f"🔄 Structure {i+1}: {structure['reps']} × {structure['duration']}min")
    
    # ÉTAPE 2: Génération structure
    with st.container():
        st.markdown("""
        <div class="pipeline-step">
            <h4>2️⃣ Génération Structure Intelligente</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.spinner("⚙️ Génération de la structure..."):
            workout_steps = parser.generate_workout_structure(entities, critical_power)
        
        if workout_steps:
            st.markdown(f"""
            <div class="success-alert">
                ✅ <strong>Structure générée</strong>: {len(workout_steps)} étapes
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="error-alert">
                ❌ <strong>Échec génération</strong>
            </div>
            """, unsafe_allow_html=True)
    
    # ÉTAPE 3: Validation stricte
    with st.container():
        st.markdown("""
        <div class="pipeline-step">
            <h4>3️⃣ Validation Ultra-Stricte</h4>
        </div>
        """, unsafe_allow_html=True)
        
        is_valid, validation_errors = parser.validate_structure_strict(workout_steps, entities, query)
        
        if is_valid:
            st.markdown("""
            <div class="success-alert">
                ✅ <strong>Validation réussie</strong> - Structure conforme à la demande
            </div>
            """, unsafe_allow_html=True)
            final_structure = workout_steps
        else:
            st.markdown(f"""
            <div class="error-alert">
                ❌ <strong>Validation échouée</strong>:<br>
                {'<br>'.join(f'• {error}' for error in validation_errors)}
            </div>
            """, unsafe_allow_html=True)
            
            # TODO: Implémentation RAG Corpus correction
            st.warning("🔧 Correction RAG non encore implémentée - utilisation structure générée")
            final_structure = workout_steps
    
    # RÉSULTATS FINAUX
    if final_structure:
        st.markdown("---")
        st.subheader("�� Résultats Finaux")
        
        # Métriques
        total_duration = sum(step['duration'] for step in final_structure)
        work_steps = [s for s in final_structure if 'récup' not in s['description'].lower()]
        avg_power = int(sum(s['power_watts'] * s['duration'] for s in work_steps) / sum(s['duration'] for s in work_steps)) if work_steps else 0
        max_power = max(s['power_watts'] for s in final_structure)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏱️ Durée</h3>
                <h2 style="color: #667eea;">{total_duration} min</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>💪 Puissance Moy</h3>
                <h2 style="color: #f093fb;">{avg_power}W</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🔥 Puissance Max</h3>
                <h2 style="color: #f5576c;">{max_power}W</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Étapes</h3>
                <h2 style="color: #764ba2;">{len(final_structure)}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Graphique intelligent
        chart = create_power_chart_intelligent(final_structure, critical_power)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # Détails des étapes
        st.subheader("🏃‍♂️ Structure Détaillée")
        
        for i, step in enumerate(final_structure, 1):
            zone_class = f"power-zone-{step['zone'].split()[-1] if 'Zone' in step['zone'] else '2'}"
            st.markdown(f"""
            <div class="step-card">
                <strong>Étape {i}:</strong> {step['description']}<br>
                <span class="{zone_class}">
                    💪 {step['duration']} min à {step['power_watts']}W ({step['power_percent']}% FTP - {step['zone']})
                </span>
            </div>
            """, unsafe_allow_html=True)

# Sidebar avec infos
with st.sidebar:
    st.subheader("🧠 Architecture V2")
    
    st.markdown("""
    **Pipeline Intelligent:**
    
    1️⃣ **LLM Extraction** - Llama-3.1-8B
    
    2️⃣ **Génération Structure** - Logique intelligente
    
    3️⃣ **Validation Stricte** - Correspondance exacte
    
    4️⃣ **Correction RAG** - Corpus fallback
    """)
    
    st.markdown("---")
    
    st.markdown("""
    **Formats Supportés:**
    
    ✅ Ordre libre
    
    ✅ Structures imbriquées (2x3x5)
    
    ✅ Séances simples
    
    ✅ Séries complexes
    
    ✅ Phases (échauffement/cooldown)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 2rem;'>
    <p>🧠 <strong>Vekta V2</strong> - Intelligence Architecture avec LLM Open Source</p>
    <p>Extraction d'Entités → Génération LLM → Validation Stricte → Correction RAG</p>
</div>
""", unsafe_allow_html=True)
