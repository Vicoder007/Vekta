import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from datetime import datetime
import time

# Configuration de la page
st.set_page_config(
    page_title="Vekta - AI-powered Session Generator",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour reproduire le design Vekta
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    
    .workout-step {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #10b981;
    }
    
    .download-btn {
        background: #fbbf24 !important;
        color: black !important;
        font-weight: bold !important;
        padding: 0.75rem 2rem !important;
        border-radius: 8px !important;
        border: none !important;
        font-size: 1.1rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background: #f1f5f9;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6 !important;
        color: white !important;
    }
    
    .power-zone-1 { color: #6b7280; }
    .power-zone-2 { color: #3b82f6; }
    .power-zone-3 { color: #10b981; }
    .power-zone-4 { color: #f59e0b; }
    .power-zone-5 { color: #ef4444; }
    .power-zone-6 { color: #8b5cf6; }
    .power-zone-7 { color: #ec4899; }
</style>
""", unsafe_allow_html=True)

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"

def call_api(endpoint, data=None, method="GET"):
    """Appel sécurisé à l'API"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erreur API: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "❌ API non disponible. Assurez-vous que l'API Vekta est démarrée."
    except requests.exceptions.Timeout:
        return None, "⏱️ Timeout de l'API. Réessayez."
    except Exception as e:
        return None, f"Erreur: {str(e)}"

def get_power_zone_color(zone):
    """Retourne la couleur correspondant à la zone de puissance"""
    colors = {
        "Zone 1": "#6b7280",
        "Zone 2": "#3b82f6", 
        "Zone 3": "#10b981",
        "Zone 4": "#f59e0b",
        "Zone 5": "#ef4444",
        "Zone 6": "#8b5cf6",
        "Zone 7": "#ec4899"
    }
    return colors.get(zone, "#6b7280")

def create_power_chart(workout_data):
    """Crée le graphique des zones de puissance"""
    if not workout_data or 'steps' not in workout_data:
        return None
    
    # Extraction des données pour le graphique
    times = []
    powers = []
    zones = []
    current_time = 0
    
    for step in workout_data['steps']:
        duration = step.get('duration', 0)
        power = step.get('power_percent', 50)
        zone = step.get('zone', 'Zone 2')
        
        times.extend([current_time, current_time + duration])
        powers.extend([power, power])
        zones.extend([zone, zone])
        current_time += duration
    
    if not times:
        return None
    
    # Création du graphique avec Plotly
    fig = go.Figure()
    
    # Ajout des segments colorés par zone
    for i in range(0, len(times)-1, 2):
        zone = zones[i]
        color = get_power_zone_color(zone)
        
        fig.add_trace(go.Scatter(
            x=[times[i], times[i+1]],
            y=[powers[i], powers[i+1]],
            mode='lines',
            line=dict(color=color, width=4),
            name=zone,
            showlegend=False
        ))
    
    fig.update_layout(
        title="Profil de Puissance",
        xaxis_title="Temps (min)",
        yaxis_title="Puissance (%FTP)",
        height=300,
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🚴 Vekta</h1>
    <p>AI-powered Session Generator</p>
</div>
""", unsafe_allow_html=True)

# Vérification de l'état de l'API
api_status, error = call_api("/health")
if error:
    st.error(error)
    st.info("💡 Pour démarrer l'API: `uvicorn vekta_api:app --reload`")
    st.stop()

# Interface principale avec onglets
tab1, tab2 = st.tabs(["🎯 Main", "⚙️ Options"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Configuration de la Séance")
        
        # Formulaire principal
        with st.form("workout_form"):
            query = st.text_area(
                "Décrivez votre séance d'entraînement :",
                placeholder="Ex: 10min échauffement puis 3 séries de 5min à fond avec 2min repos entre séries puis 10min retour au calme",
                height=100
            )
            
            author = st.text_input("Auteur", value="Vekta AI")
            
            col_duration, col_threshold = st.columns(2)
            with col_duration:
                duration = st.number_input("Durée (min)", min_value=10, max_value=300, value=60)
            
            with col_threshold:
                threshold_override = st.checkbox("Override Threshold")
            
            submit = st.form_submit_button("🚀 Générer la Séance", use_container_width=True)
    
    with col2:
        st.subheader("Zones de Puissance")
        
        # Configuration des zones de puissance
        critical_power = st.number_input("Critical Power (W)", min_value=100, max_value=500, value=250)
        
        # Affichage des zones calculées
        zones_data = {
            "Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7"],
            "% FTP": ["< 55%", "55-75%", "75-90%", "90-105%", "105-120%", "120-150%", "> 150%"],
            "Watts": [
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

# Traitement de la génération
if submit and query:
    with st.spinner("🔄 Génération de la séance en cours..."):
        # Validation de la requête
        validation_data, error = call_api("/validate", {
            "query": query,
            "author": author
        }, "POST")
        
        if error:
            st.error(error)
        elif validation_data:
            # Affichage des résultats de validation
            confidence = validation_data.get('confidence', 0)
            is_valid = validation_data.get('is_valid', False)
            
            if is_valid:
                st.success(f"✅ Requête validée avec {confidence:.1%} de confiance")
                
                # Génération de la séance
                workout_data, error = call_api("/generate-workout", {
                    "query": query,
                    "author": author,
                    "duration_minutes": duration,
                    "critical_power": critical_power
                }, "POST")
                
                if workout_data and not error:
                    # Affichage des métriques
                    st.subheader("📊 Métriques de la Séance")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>⏱️ Durée</h3>
                            <h2>{workout_data.get('duration_minutes', 0)} min</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>⚡ Puissance</h3>
                            <h2>{workout_data.get('avg_power_percent', 0):.0f}% FTP</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🎯 Training Stimulus</h3>
                            <h2>{workout_data.get('training_stimulus', 0):.1f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h3>🔥 Calories</h3>
                            <h2>{workout_data.get('estimated_calories', 0):.0f} kcal</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Graphique de puissance
                    st.subheader("📈 Profil de Puissance")
                    chart = create_power_chart(workout_data)
                    if chart:
                        st.plotly_chart(chart, use_container_width=True)
                    
                    # Structure de la séance
                    st.subheader("🏃‍♂️ Structure de la Séance")
                    
                    if 'steps' in workout_data:
                        for i, step in enumerate(workout_data['steps'], 1):
                            duration = step.get('duration', 0)
                            power = step.get('power_percent', 0)
                            zone = step.get('zone', 'Zone 2')
                            description = step.get('description', f'Étape {i}')
                            
                            st.markdown(f"""
                            <div class="workout-step">
                                <strong>Étape {i}:</strong> {description}<br>
                                <span class="power-zone-{zone.split()[-1] if 'Zone' in zone else '2'}">
                                    📊 {duration} min à {power}% FTP ({zone})
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Bouton de téléchargement
                    st.subheader("💾 Téléchargement")
                    
                    if 'zwo_content' in workout_data:
                        st.download_button(
                            label="📥 Download .zwo",
                            data=workout_data['zwo_content'],
                            file_name=f"vekta_workout_{int(time.time())}.zwo",
                            mime="application/xml",
                            help="Téléchargez le fichier .zwo pour Zwift"
                        )
                    
                    # Détails techniques
                    with st.expander("🔧 Détails Techniques"):
                        st.json(workout_data)
                
                else:
                    st.error("❌ Erreur lors de la génération de la séance")
            
            else:
                st.warning(f"⚠️ Requête peu claire (confiance: {confidence:.1%})")
                
                if 'suggestions' in validation_data:
                    st.info("💡 Suggestions:")
                    for suggestion in validation_data['suggestions']:
                        st.write(f"• {suggestion}")

with tab2:
    st.subheader("⚙️ Options Avancées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Paramètres de Validation**")
        confidence_threshold = st.slider("Seuil de confiance", 0.0, 1.0, 0.85, 0.05)
        enable_spell_check = st.checkbox("Correction orthographique", value=True)
        
        st.write("**Paramètres de Génération**")
        default_power_zones = st.checkbox("Zones de puissance par défaut", value=True)
        include_warmup = st.checkbox("Inclure échauffement", value=True)
        include_cooldown = st.checkbox("Inclure retour au calme", value=True)
    
    with col2:
        st.write("**Statistiques de l'API**")
        
        metrics_data, error = call_api("/metrics")
        if metrics_data and not error:
            st.metric("Requêtes traitées", metrics_data.get('total_requests', 0))
            st.metric("Taux de succès", f"{metrics_data.get('success_rate', 0):.1%}")
            st.metric("Temps de réponse moyen", f"{metrics_data.get('avg_response_time', 0):.2f}s")
        
        # Test de l'API
        if st.button("🔍 Tester l'API"):
            test_data, error = call_api("/health")
            if error:
                st.error(error)
            else:
                st.success("✅ API fonctionnelle")
                st.json(test_data)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; padding: 1rem;'>
    <p>🚴 <strong>Vekta AI</strong> - Générateur de séances d'entraînement cycliste alimenté par l'IA</p>
    <p>Développé avec ❤️ pour la communauté cycliste</p>
</div>
""", unsafe_allow_html=True) 