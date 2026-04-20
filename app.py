
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:53:39 2025

@author: prince CHABI
"""
import streamlit as st
import subprocess
import os
import tempfile
import time
from pathlib import Path
import base64
import sys

# Configuration de la page
st.set_page_config(
    page_title="TrimVid Pro - Compresseur Vidéo",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cacher TOUS les éléments Streamlit par défaut
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
#stDecoration {display:none;}
.viewerBadge_container__1QSob {
    display: none !important;
}
[data-testid="stDeployButton"] {
    display: none !important;
}
.stApp [data-testid="stToolbar"] {
    display: none;
}
.stApp [data-testid="stDecoration"] {
    display: none;
}
.stApp [data-testid="stStatusWidget"] {
    display: none;
}
/* Cacher le badge GitHub et Streamlit Cloud */
[data-testid="stAppViewContainer"] > footer {
    display: none !important;
}
[class*="viewerBadge"] {
    display: none !important;
}
a[href*="streamlit.io"] {
    display: none !important;
}

/* Réduire l'espace en haut */
.stApp {
    margin-top: -50px;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* Styles pour forcer l'ouverture de la sidebar */
.sidebar-open {
    transform: translateX(0) !important;
}

/* CACHER LA SIDEBAR SUR MOBILE */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Afficher un message informatif */
    .mobile-sidebar-message {
        display: block !important;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
        text-align: center;
    }
}

@media (min-width: 769px) {
    .mobile-sidebar-message {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: block !important;
    }
}

/* Style pour le message d'information mobile */
.mobile-sidebar-message {
    display: none;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# CSS personnalisé avec responsive design
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .pro-text {
        font-size: 2rem;
        color: #FF8E53;
        vertical-align: super;
        font-weight: 600;
    }
    .professional-title {
        font-size: 1.4rem;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-msg {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        color: #155724;
    }
    .error-msg {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        color: #721c24;
    }
    .compression-stats {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    .upload-box {
        border: 2px dashed #FF6B35;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        background-color: #FFF5F0;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 1rem;
        padding: 1rem;
    }
    .sidebar-header {
        color: #FF6B35;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .stButton button {
        background-color: #FF6B35;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #E55A2B;
        color: white;
    }
    .website-promo {
        background: linear-gradient(135deg, #FF6B35, #FF8E53);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .website-promo a {
        color: white !important;
        text-decoration: none;
        font-weight: bold;
    }
    .website-promo a:hover {
        text-decoration: underline;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .enterprise-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .enterprise-button {
        background: white;
        color: #667eea;
        padding: 1rem 2rem;
        border-radius: 2rem;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
        transition: transform 0.3s ease;
    }
    .enterprise-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .signature {
        text-align: center;
        font-style: italic;
        color: #666;
        margin-top: 1rem;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
    }
    .developer-name {
        font-weight: bold;
        color: #FF6B35;
    }
    .developer-title {
        color: #667eea;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #856404;
    }
    .file-size-warning {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #721c24;
    }
    
    /* Styles responsives pour mobile */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .pro-text {
            font-size: 1.5rem;
        }
        .professional-title {
            font-size: 1.1rem;
        }
        
        /* Ajustements pour le contenu principal sur mobile */
        .main-content {
            padding: 0.5rem;
        }
        
        /* Ajustement des colonnes sur mobile */
        .column-adjust {
            margin-bottom: 1rem;
        }
    }
    
    /* Style pour le bouton Paramètres */
    .settings-button-container {
        text-align: center;
        margin: 1rem 0 2rem 0;
    }
    
    .settings-button {
        background-color: #FF6B35;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        box-shadow: 0 2px 8px rgba(255, 107, 53, 0.3);
        transition: all 0.3s ease;
        margin: 0.5rem 0;
        width: auto;
        min-width: 280px;
    }
    
    .settings-button:hover {
        background-color: #E55A2B;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
    }
    
    /* Cacher le bouton mobile en haut à gauche */
    .mobile-sidebar-toggle {
        display: none !important;
    }
    
    /* Styles pour les paramètres qui s'ouvrent en bas du bouton */
    .settings-container {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-top: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .settings-section {
        margin-bottom: 1.5rem;
    }
    
    .settings-title {
        color: #FF6B35;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Style pour le texte d'avertissement */
    .settings-warning {
        text-align: center;
        font-size: 0.85rem;
        color: #FF6B35;
        background-color: #FFF5F0;
        border: 1px solid #FFE0D6;
        border-radius: 0.3rem;
        padding: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Style pour les paramètres mobiles */
    .mobile-settings-container {
        background: linear-gradient(135deg, #FF6B35, #FF8E53);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def install_ffmpeg():
    """Tente d'installer FFmpeg si disponible"""
    try:
        # Sur Streamlit Cloud, FFmpeg est généralement préinstallé
        # Mais on peut essayer de l'installer via apt si nécessaire
        subprocess.run(['apt-get', 'update'], capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'ffmpeg'], capture_output=True)
        return True
    except:
        return False

def find_ffmpeg():
    """Trouve le chemin de FFmpeg"""
    # Chemins possibles pour FFmpeg
    possible_paths = [
        'ffmpeg',
        '/usr/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        '/app/bin/ffmpeg',
        '/opt/conda/bin/ffmpeg',
        './ffmpeg'
    ]
    
    for path in possible_paths:
        try:
            result = subprocess.run([path, '-version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return path
        except:
            continue
    
    return None

def check_ffmpeg():
    """Vérifie si FFmpeg est disponible - Version optimisée pour le cloud"""
    try:
        # Essayer de trouver FFmpeg
        ffmpeg_path = find_ffmpeg()
        if ffmpeg_path:
            return True, ffmpeg_path
        
        # Si non trouvé, essayer d'installer
        st.info("🔧 Installation de FFmpeg en cours...")
        if install_ffmpeg():
            ffmpeg_path = find_ffmpeg()
            if ffmpeg_path:
                return True, ffmpeg_path
        
        return False, None
        
    except Exception as e:
        st.warning(f"⚠️ Erreur lors de la vérification FFmpeg: {str(e)}")
        return False, None

def get_file_size(file_path):
    """Retourne la taille du fichier en MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_video(input_path, output_path, crf=23, preset='medium', audio_quality=128):
    """
    Fonction de compression vidéo avec gestion d'erreurs améliorée
    """
    try:
        # Obtenir le chemin de FFmpeg
        ffmpeg_available, ffmpeg_path = check_ffmpeg()
        
        if not ffmpeg_available:
            return False, "FFmpeg n'est pas disponible sur ce système"
        
        command = [
            ffmpeg_path,
            '-i', input_path,
            '-c:v', 'libx264',
            '-crf', str(crf),
            '-preset', preset,
            '-profile:v', 'high',
            '-level', '4.0',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-b:a', f'{audio_quality}k',
            '-movflags', '+faststart',
            '-y',
            output_path
        ]
        
        # Afficher la commande pour le débogage
        st.write(f"🔧 Commande exécutée: {' '.join(command)}")
        
        # Timeout de 5 minutes pour éviter les blocages
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=300)
        return True, None
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else "Erreur inconnue lors de la compression"
        return False, f"Erreur de compression: {error_msg}"
    except subprocess.TimeoutExpired:
        return False, "La compression a pris trop de temps (timeout de 5 minutes)"
    except FileNotFoundError:
        return False, "FFmpeg n'a pas été trouvé. Vérifiez l'installation."
    except Exception as e:
        return False, f"Erreur inattendue: {str(e)}"

def main():
    # JavaScript pour gérer l'ouverture de la sidebar
    st.markdown(f'''
    <script>
    function openSidebar() {{
        // Cette fonction ouvre la sidebar Streamlit
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {{
            // Forcer l'ouverture de la sidebar
            sidebar.style.transform = 'translateX(0)';
            sidebar.style.visibility = 'visible';
            sidebar.style.width = 'auto';
            
            // Ajouter une classe pour confirmer l'ouverture
            sidebar.classList.add('sidebar-open');
            
            // Déclencher l'événement de redimensionnement pour Streamlit
            window.dispatchEvent(new Event('resize'));
        }}
        
        // Afficher un message de débogage dans la console
        console.log("Bouton Paramètres cliqué - Sidebar devrait s'ouvrir");
    }}
    
    // Cacher tous les éléments GitHub et Streamlit
    document.addEventListener('DOMContentLoaded', function() {{
        // Supprimer les badges GitHub
        const badges = document.querySelectorAll('[class*="viewerBadge"], [class*="github"]');
        badges.forEach(badge => badge.style.display = 'none');
        
        // Supprimer les liens Streamlit
        const links = document.querySelectorAll('a[href*="streamlit.io"], a[href*="github.com"]');
        links.forEach(link => {{
            if (link.textContent.includes('streamlit.io') || link.textContent.includes('github.com')) {{
                link.style.display = 'none';
            }}
        }});
        
        // Supprimer le footer
        const footer = document.querySelector('footer');
        if (footer) footer.style.display = 'none';
        
        // Vérifier si la sidebar est déjà ouverte au chargement
        setTimeout(function() {{
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar && window.innerWidth > 768) {{
                sidebar.style.transform = 'translateX(0)';
                sidebar.style.visibility = 'visible';
            }}
        }}, 1000);
    }});
    </script>
    ''', unsafe_allow_html=True)

    # Initialisation de l'état pour le bouton paramètres
    if 'show_settings' not in st.session_state:
        st.session_state.show_settings = False

    # Message d'information pour mobile
    st.markdown("""
    <div class="mobile-sidebar-message">
        📱 <strong>Version Mobile</strong> - Utilisez le bouton "Paramètres de Compression" ci-dessous pour ajuster les paramètres
    </div>
    """, unsafe_allow_html=True)

    # Sidebar (uniquement visible sur desktop)
    with st.sidebar:
        # Promotion du site web
        st.markdown("""
        <div class="website-promo">
            <strong>🚀 Découvrez nos services professionnels</strong><br>
            <a href="https://btece.netlify.app/siteweb/mon_entreprise_en_ligne.com" target="_blank">
                Visitez notre site web
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Paramètres de compression
        st.markdown('<p class="sidebar-header">⚙️ PARAMÈTRES DE COMPRESSION</p>', unsafe_allow_html=True)
        
        # Qualité vidéo
        st.subheader("🎯 Qualité Vidéo")
        quality_option = st.selectbox(
            "Niveau de qualité",
            ["Haute qualité (CRF 18)", "Équilibré (CRF 23)", "Compression élevée (CRF 26)", "Personnalisé"],
            index=1,
            key="sidebar_quality"
        )
        
        if quality_option == "Personnalisé":
            crf = st.slider("CRF (Constant Rate Factor)", 18, 28, 23, 
                           help="Plus bas = meilleure qualité, Plus haut = plus de compression",
                           key="sidebar_crf")
        else:
            crf_map = {
                "Haute qualité (CRF 18)": 18,
                "Équilibré (CRF 23)": 23,
                "Compression élevée (CRF 26)": 26
            }
            crf = crf_map[quality_option]
        
        # Vitesse de compression
        st.subheader("⚡ Vitesse")
        preset = st.selectbox(
            "Préréglage de compression",
            ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
            index=5,
            help="Plus rapide = fichier plus gros, Plus lent = meilleure compression",
            key="sidebar_preset"
        )
        
        # Qualité audio
        st.subheader("🎵 Audio")
        audio_quality = st.slider("Qualité audio (kbps)", 64, 320, 128, key="sidebar_audio")
        
        # Informations sur les paramètres
        st.markdown("---")
        st.markdown('<p class="sidebar-header">💡 CONSEILS TRIMVID PRO</p>', unsafe_allow_html=True)
        
        with st.expander("Optimiser vos paramètres"):
            st.markdown("""
            **🎯 Pour une qualité optimale :**
            - CRF: 18-20
            - Preset: slow
            - Audio: 192 kbps
            
            **📱 Pour les réseaux sociaux :**
            - CRF: 23-25
            - Preset: medium
            - Audio: 128 kbps
            
            **💾 Compression maximale :**
            - CRF: 26-28
            - Preset: veryslow
            - Audio: 96 kbps
            """)
        
        # Limitations du cloud
        st.markdown("---")
        st.markdown('<p class="sidebar-header">📋 LIMITATIONS CLOUD</p>', unsafe_allow_html=True)
        st.warning("""
        **Streamlit Cloud :**
        - Taille max : 200MB par fichier
        - Timeout : 5 minutes
        - Stockage temporaire uniquement
        """)

    # Zone principale - Titre principal
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 class="main-header">TrimVid<span class="pro-text"> Pro</span></h1>
        <div class="professional-title">
            APPLICATION WEB TRIMVID PRO - COMPRESSEUR VIDÉO PROFESSIONNEL
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Signature du développeur
    st.markdown("""
    <div class="signature">
        Développé par <span class="developer-name">Sunny</span>, 
        <span class="developer-title">Ingénieur en Data, Expert Certifié</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Vérification de FFmpeg au démarrage
    ffmpeg_available, ffmpeg_path = check_ffmpeg()
    
    if not ffmpeg_available:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ FFmpeg n'est pas disponible</strong><br>
            L'application ne peut pas fonctionner sans FFmpeg. 
            Veuillez contacter l'administrateur pour installer FFmpeg sur le système.
        </div>
        """, unsafe_allow_html=True)
        
        # Instructions d'installation
        with st.expander("🔧 Instructions d'installation FFmpeg"):
            st.markdown("""
            **Pour installer FFmpeg :**
            
            **Sur Ubuntu/Debian :**
            ```bash
            sudo apt update
            sudo apt install ffmpeg
            ```
            
            **Sur Streamlit Cloud :**
            Ajoutez cette ligne à votre fichier `requirements.txt` :
            ```
            ffmpeg-python
            ```
            
            **Alternative Python :**
            Si FFmpeg n'est pas disponible, vous pouvez utiliser la bibliothèque `moviepy` :
            ```python
            pip install moviepy
            ```
            """)
        return  # Arrêter l'exécution si FFmpeg n'est pas disponible
    else:
        st.success(f"✅ Trimvid Pro prêt pour la compression : {ffmpeg_path}")
    
    # Bouton Paramètres de compression - CORRECTION PRINCIPALE
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⚙️ Paramètres de Compression", key="settings_button", use_container_width=True):
            st.session_state.show_settings = not st.session_state.show_settings
            st.rerun()
    
    # Texte d'avertissement ajouté sous le bouton
    st.markdown("""
    <div class="settings-warning">
        ⚠️ Paramètres par défaut Actifs (Recommandé si vous êtes débutant en traitement vidéo)
    </div>
    """, unsafe_allow_html=True)
    
    # Affichage des paramètres en dessous du bouton (pour mobile et desktop)
    if st.session_state.show_settings:
        with st.container():
            st.markdown('<div class="settings-container">', unsafe_allow_html=True)
            st.markdown('<div class="settings-title">⚙️ PARAMÈTRES DE COMPRESSION</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="settings-section">', unsafe_allow_html=True)
                st.subheader("🎯 Qualité Vidéo")
                quality_option = st.selectbox(
                    "Niveau de qualité",
                    ["Haute qualité (CRF 18)", "Équilibré (CRF 23)", "Compression élevée (CRF 26)", "Personnalisé"],
                    index=1,
                    key="main_quality"
                )
                
                if quality_option == "Personnalisé":
                    crf = st.slider("CRF (Constant Rate Factor)", 18, 28, 23, 
                                   help="Plus bas = meilleure qualité, Plus haut = plus de compression",
                                   key="main_crf")
                else:
                    crf_map = {
                        "Haute qualité (CRF 18)": 18,
                        "Équilibré (CRF 23)": 23,
                        "Compression élevée (CRF 26)": 26
                    }
                    crf = crf_map[quality_option]
                
                st.subheader("⚡ Vitesse")
                preset = st.selectbox(
                    "Préréglage de compression",
                    ["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
                    index=5,
                    help="Plus rapide = fichier plus gros, Plus lent = meilleure compression",
                    key="main_preset"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="settings-section">', unsafe_allow_html=True)
                st.subheader("🎵 Audio")
                audio_quality = st.slider("Qualité audio (kbps)", 64, 320, 128, key="main_audio")
                
                st.subheader("📊 Résumé des paramètres")
                st.write(f"**CRF:** {crf}")
                st.write(f"**Preset:** {preset}")
                st.write(f"**Audio:** {audio_quality} kbps")
                
                # Indicateur visuel de qualité
                if crf <= 20:
                    st.success("🎯 Qualité Excellente")
                elif crf <= 23:
                    st.info("⚖️ Qualité Équilibrée")
                else:
                    st.warning("💾 Compression Élevée")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Bouton pour fermer les paramètres
            if st.button("✓ Appliquer les paramètres", key="apply_settings", use_container_width=True):
                st.session_state.show_settings = False
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Zone principale - Contenu
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="upload-box">', unsafe_allow_html=True)
        st.subheader("📤 TÉLÉVERSEZ VOTRE VIDÉO")
        
        uploaded_file = st.file_uploader(
            "Glissez-déposez votre fichier vidéo ici",
            type=['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'wmv', 'm4v'],
            help="Formats supportés : MP4, AVI, MOV, MKV, WEBM, FLV, WMV, M4V | Taille max: 200MB"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            # Vérification de la taille du fichier
            file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
            
            if file_size_mb > 200:
                st.markdown(f"""
                <div class="file-size-warning">
                    ❌ <strong>Fichier trop volumineux : {file_size_mb:.1f} MB</strong><br>
                    La limite sur Streamlit Cloud est de 200 MB par fichier.
                </div>
                """, unsafe_allow_html=True)
            else:
                # Affichage des informations du fichier
                file_details = {
                    "📝 Nom": uploaded_file.name,
                    "📊 Type": uploaded_file.type,
                    "💾 Taille": f"{file_size_mb:.2f} MB"
                }
                
                st.subheader("📋 INFORMATIONS DU FICHIER")
                for key, value in file_details.items():
                    st.write(f"**{key}:** {value}")
                
                # Aperçu de la vidéo
                st.subheader("👀 APERÇU DE LA VIDÉO")
                st.video(uploaded_file)
    
    with col2:
        st.subheader("🎯 RÉSUMÉ DES PARAMÈTRES")
        
        if uploaded_file is not None and (uploaded_file.size / (1024 * 1024)) <= 200:
            # Affichage des paramètres sélectionnés
            st.write(f"**🎯 Qualité :** CRF {crf}")
            st.write(f"**⚡ Vitesse :** {preset}")
            st.write(f"**🎵 Audio :** {audio_quality} kbps")
            st.write(f"**🔧 Codec :** H.264 (MP4)")
            
            # Estimation de la taille (approximative)
            original_size = len(uploaded_file.getvalue()) / (1024*1024)
            estimated_reduction = {
                18: 0.4,   # 40% de réduction
                19: 0.45,  # 45% de réduction
                20: 0.5,   # 50% de réduction
                21: 0.55,  # 55% de réduction
                22: 0.6,   # 60% de réduction
                23: 0.65,  # 65% de réduction
                24: 0.7,   # 70% de réduction
                25: 0.75,  # 75% de réduction
                26: 0.8,   # 80% de réduction
                27: 0.85,  # 85% de réduction
                28: 0.9    # 90% de réduction
            }
            
            reduction = estimated_reduction.get(crf, 0.6)
            estimated_size = original_size * (1 - reduction)
            
            st.write(f"**📊 Taille estimée :** {estimated_size:.1f} MB")
            st.write(f"**📉 Réduction estimée :** {reduction*100:.0f}%")
            
            # Indicateur visuel de qualité
            if crf <= 20:
                st.success("🎯 Qualité Excellente")
            elif crf <= 23:
                st.info("⚖️ Qualité Équilibrée")
            else:
                st.warning("💾 Compression Élevée")
        else:
            st.info("📤 Téléversez une vidéo pour voir les estimations")
    
    # Bouton de compression
    if uploaded_file is not None and (uploaded_file.size / (1024 * 1024)) <= 200:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚀 DÉMARRER LA COMPRESSION TRIMVID PRO", use_container_width=True):
                with st.spinner("🔄 Compression en cours... Cette opération peut prendre quelques minutes selon la taille de la vidéo."):
                    # Création des fichiers temporaires
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_input:
                        tmp_input.write(uploaded_file.getvalue())
                        input_path = tmp_input.name
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_output:
                        output_path = tmp_output.name
                    
                    try:
                        # Compression
                        start_time = time.time()
                        success, error = compress_video(input_path, output_path, crf, preset, audio_quality)
                        compression_time = time.time() - start_time
                        
                        if success:
                            # Calcul des statistiques
                            original_size = get_file_size(input_path)
                            compressed_size = get_file_size(output_path)
                            
                            if compressed_size > 0:
                                reduction = (1 - compressed_size/original_size) * 100
                            else:
                                reduction = 0
                                st.warning("Impossible de calculer la réduction - la taille du fichier compressé est nulle")
                            
                            # Affichage des résultats
                            st.markdown("---")
                            st.balloons()
                            st.success("✅ Compression TrimVid Pro réussie !")
                            
                            # Statistiques détaillées
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Taille originale", f"{original_size:.2f} MB", delta=None)
                            with col2:
                                st.metric("Taille compressée", f"{compressed_size:.2f} MB", 
                                         delta=f"-{(original_size - compressed_size):.1f} MB" if original_size > compressed_size else None)
                            with col3:
                                st.metric("Réduction", f"{reduction:.1f}%")
                            with col4:
                                st.metric("Temps", f"{compression_time:.1f}s")
                            
                            # Barre de progression visuelle
                            if reduction > 0:
                                st.progress(min(reduction/100, 1.0))
                            
                            # Téléchargement du fichier
                            with open(output_path, 'rb') as f:
                                video_data = f.read()
                            
                            output_filename = f"trimvid_pro_compressed_{Path(uploaded_file.name).stem}.mp4"
                            
                            st.download_button(
                                label="📥 TÉLÉCHARGER LA VIDÉO COMPRESSÉE",
                                data=video_data,
                                file_name=output_filename,
                                mime="video/mp4",
                                use_container_width=True
                            )
                            
                            # Informations techniques détaillées
                            with st.expander("🔧 DÉTAILS TECHNIQUES"):
                                st.write(f"**⏱️ Temps de compression :** {compression_time:.1f} secondes")
                                if compressed_size > 0 and original_size > 0:
                                    st.write(f"**📈 Ratio de compression :** {original_size/compressed_size:.2f}:1")
                                st.write(f"**💾 Économie d'espace :** {original_size - compressed_size:.2f} MB")
                                st.write(f"**⚙️ Paramètres utilisés :**")
                                st.write(f"  - CRF: {crf}")
                                st.write(f"  - Preset: {preset}")
                                st.write(f"  - Audio: {audio_quality}kbps")
                                st.write(f"  - Codec: H.264")
                                st.write(f"  - Profile: High")
                        
                        else:
                            st.error(f"❌ Erreur lors de la compression : {error}")
                            st.info("""
                            **💡 Solutions possibles :**
                            - Essayez avec un CRF plus élevé (26-28)
                            - Utilisez le preset 'ultrafast' ou 'superfast'
                            - Réduisez la qualité audio à 96 kbps
                            - Vérifiez que la vidéo n'est pas corrompue
                            """)
                    
                    except Exception as e:
                        st.error(f"❌ Une erreur s'est produite : {str(e)}")
                        st.info("Si le problème persiste, essayez avec une vidéo plus petite ou différents paramètres.")
                    
                    finally:
                        # Nettoyage des fichiers temporaires
                        try:
                            if 'input_path' in locals() and os.path.exists(input_path):
                                os.unlink(input_path)
                            if 'output_path' in locals() and os.path.exists(output_path):
                                os.unlink(output_path)
                        except Exception as e:
                            # Ignorer les erreurs de nettoyage
                            pass
    
    # Section caractéristiques professionnelles
    with st.expander("🌟 POURQUOI CHOISIR TRIMVID PRO ?"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>🔒 Sécurité Maximale</h4>
                <p>Traitement 100% local, aucune donnée envoyée sur internet, fichiers temporaires supprimés automatiquement</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>⚡ Performance Pro</h4>
                <p>Compression optimisée avec algorithmes avancés, interface fluide, multi-threading</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🎯 Qualité Expert</h4>
                <p>Préservation maximale de la qualité, formats multiples supportés, paramètres professionnels</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Section guide professionnel
    with st.expander("📚 GUIDE PROFESSIONNEL TRIMVID PRO"):
        st.markdown("""
        ### 🎬 Utilisation Professionnelle :
        
        **Workflow recommandé :**
        1. **📤 Téléversement** de la vidéo source
        2. **⚙️ Analyse** des paramètres optimaux
        3. **🚀 Compression** avec monitoring en temps réel
        4. **📥 Téléchargement** et vérification qualité
        
        ### 🎯 Paramètres Avancés :
        
        **Pour la production vidéo :**
        - CRF: 18-20 avec preset 'slow'
        - Audio: 192-256 kbps
        - Profile: High, Level: 4.0
        
        **Pour le streaming :**
        - CRF: 23-25 avec preset 'medium'
        - Audio: 128 kbps
        - Movflags: +faststart
        
        **Pour l'archivage :**
        - CRF: 18 avec preset 'veryslow'
        - Audio: 320 kbps
        - Profile: High 4.1
        """)
    
    # Section dépannage
    with st.expander("🔧 DÉPANNAGE ET CONSEILS"):
        st.markdown("""
        **Problèmes courants et solutions :**
        
        **❌ La compression échoue :**
        - Essayez avec des paramètres plus simples (CRF 26, preset 'medium')
        - Vérifiez que la vidéo n'est pas corrompue
        - Réduisez la taille de la vidéo (< 100MB)
        
        **❌ Fichier trop volumineux :**
        - La limite est de 200MB sur notre Cloud
        - Compressez d'abord avec un outil local si nécessaire
        
        **❌ Timeout pendant la compression :**
        - Utilisez le preset 'ultrafast' ou 'superfast'
        - Réduisez la qualité (CRF 26-28)
        - Essayez avec une vidéo plus courte
        
        **✅ Pour de meilleurs résultats :**
        - Utilisez des vidéos en MP4 ou MOV
        - Évitez les vidéos 4K très longues
        - Testez d'abord avec de petites vidéos
        """)
    
    # Section Solutions Professionnelles
    st.markdown("""
    <div class="enterprise-section">
        <h2 style="color: white; margin-bottom: 1rem;">🚀 SOLUTIONS PROFESSIONNELLES</h2>
        <p style="font-size: 1.3rem; margin-bottom: 1rem; color: white;">
            Besoin de solutions de compression vidéo avancées pour votre entreprise ?
        </p>
        <p style="font-size: 1.1rem; margin-bottom: 2rem; color: white; opacity: 0.9;">
            Nous développons des solutions sur mesure adaptées à vos besoins spécifiques.
        </p>
        <a href="https://btece.netlify.app/siteweb/mon_entreprise_en_ligne.com" 
           target="_blank" 
           class="enterprise-button">
           📞 Contactez-nous
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Pied de page professionnel
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 2rem;'>"
        "<strong>TrimVid Pro</strong> 🎬 | Application Web Professionnelle de Compression Vidéo<br>"
        "Développé par <strong>Sunny</strong>, Ingénieur en Data, Expert Certifié<br>"
        "<span style='font-size: 0.9rem;'>"
        "<a href='https://btece.netlify.app/siteweb/mon_entreprise_en_ligne.com' target='_blank' style='color: #FF6B35;'>Visitez notre site web professionnel</a> | "
        "© 2025 Tous droits réservés"
        "</span>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()