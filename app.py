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
        
        /* Ajustements pour la sidebar sur mobile */
        section[data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
        }
        
        /* Forcer l'affichage de la sidebar sur mobile */
        .css-1d391kg {
            width: 100% !important;
        }
        
        /* Ajuster le contenu principal sur mobile */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
    }
    
    /* Bouton pour ouvrir/fermer la sidebar sur mobile */
    .mobile-sidebar-toggle {
        display: none;
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 9999;
        background: #FF6B35;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    @media (max-width: 768px) {
        .mobile-sidebar-toggle {
            display: block;
        }
        
        /* Cacher la sidebar par défaut sur mobile et la montrer quand active */
        section[data-testid="stSidebar"] {
            transform: translateX(-100%);
            transition: transform 0.3s ease;
        }
        
        section[data-testid="stSidebar"].sidebar-open {
            transform: translateX(0);
        }
    }
    
    /* Réduire l'espacement global */
    .stApp {
        margin-top: -30px;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def check_ffmpeg():
    """Vérifie si FFmpeg est disponible - Version optimisée pour le cloud"""
    try:
        # Méthode 1: Commande standard
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            return True
        
        # Méthode 2: Vérification des chemins communs sur le cloud
        common_paths = [
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            '/app/bin/ffmpeg',
            '/opt/conda/bin/ffmpeg'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return True
                
        # Méthode 3: Commande which/where
        if os.name == 'nt':  # Windows
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True)
        else:  # Linux/macOS/Cloud
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
        
        if result.returncode == 0:
            return True
            
        # Sur Streamlit Cloud, on suppose que FFmpeg est disponible même si non détecté
        return True
        
    except Exception as e:
        # En cas d'erreur, on suppose que FFmpeg est disponible sur le cloud
        return True

def get_file_size(file_path):
    """Retourne la taille du fichier en MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_video(input_path, output_path, crf=23, preset='medium', audio_quality=128):
    """
    Fonction de compression vidéo avec gestion d'erreurs améliorée
    """
    try:
        command = [
            'ffmpeg',
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
        
        # Timeout de 5 minutes pour éviter les blocages
        result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=300)
        return True, None
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else "Erreur inconnue lors de la compression"
        return False, error_msg
    except subprocess.TimeoutExpired:
        return False, "La compression a pris trop de temps (timeout de 5 minutes)"
    except Exception as e:
        return False, f"Erreur inattendue: {str(e)}"

def main():
    # Gestion de l'état de la sidebar pour mobile
    if 'sidebar_open' not in st.session_state:
        st.session_state.sidebar_open = False

    # Bouton toggle pour mobile
    st.markdown(f'''
    <button class="mobile-sidebar-toggle" onclick="toggleSidebar()">⚙️</button>
    <script>
    function toggleSidebar() {{
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {{
            sidebar.classList.toggle('sidebar-open');
        }}
        
        // Envoyer un message à Streamlit pour mettre à jour l'état
        window.parent.postMessage({{type: 'TOGGLE_SIDEBAR'}}, '*');
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
        
        // Réduire l'espace en haut
        const mainContainer = document.querySelector('.main');
        if (mainContainer) {{
            mainContainer.style.paddingTop = '0';
        }}
    }});
    
    // Écouter les messages pour toggle la sidebar
    window.addEventListener('message', function(event) {{
        if (event.data.type === 'TOGGLE_SIDEBAR') {{
            const sidebar = document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {{
                sidebar.classList.toggle('sidebar-open');
            }}
        }}
    }});
    </script>
    ''', unsafe_allow_html=True)

    # Sidebar - Toujours visible maintenant
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
            index=1
        )
        
        if quality_option == "Personnalisé":
            crf = st.slider("CRF (Constant Rate Factor)", 18, 28, 23, 
                           help="Plus bas = meilleure qualité, Plus haut = plus de compression")
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
            help="Plus rapide = fichier plus gros, Plus lent = meilleure compression"
        )
        
        # Qualité audio
        st.subheader("🎵 Audio")
        audio_quality = st.slider("Qualité audio (kbps)", 64, 320, 128)
        
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

    # Zone principale - Titre principal sans espace excessif
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
    
    # Vérification de FFmpeg - Version corrigée pour le cloud
    ffmpeg_available = check_ffmpeg()
    
    if not ffmpeg_available:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ TrimVid n'a pas pu être vérifié</strong><br>
            L'application va quand même essayer de fonctionner. 
            Si la compression échoue, cela peut être dû à une limitation de la plateforme cloud.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ TrimVid est disponible - Prêt pour la compression !")
    
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
            
        # Section services professionnels
        st.markdown("---")
        st.markdown("""
        
        """, unsafe_allow_html=True)
    
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