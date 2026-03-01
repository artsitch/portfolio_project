import streamlit as st


def main():
    # 1. Configuration et Style
    st.set_page_config(page_title="Data Portfolio", layout="wide")
    
# CSS personnalisé pour la sidebar
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

    /* === SIDEBAR === */
    [data-testid="stSidebar"] {
        background: #0a0a0f;
        border-right: 1px solid #1e1e2e;
        min-width: 260px !important;
        max-width: 260px !important;
    }

    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: radial-gradient(ellipse at top left, rgba(99,102,241,0.12) 0%, transparent 60%);
        pointer-events: none;
    }

    /* Titre de la sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] .sidebar-title {
        font-family: 'Syne', sans-serif !important;
        font-weight: 800;
        font-size: 1.1rem;
        color: #6366f1 !important;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 1.5rem 1rem 0.5rem;
    }

    /* Séparateur sous le titre */
    [data-testid="stSidebar"] hr {
        border-color: #1e1e2e;
        margin: 0.5rem 1rem 1rem;
    }

    /* Radio buttons - conteneur */
    [data-testid="stSidebar"] [data-testid="stRadio"] {
        padding: 0 0.5rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 0.25rem;
        display: flex;
        flex-direction: column;
    }

    /* Chaque item radio - label */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.82rem !important;
        color: #6b7280 !important;
        cursor: pointer;
        padding: 0.6rem 1rem !important;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        letter-spacing: 0.05em;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem;
    }

    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        color: #e2e8f0 !important;
        background: rgba(99,102,241,0.08) !important;
        border-color: rgba(99,102,241,0.2) !important;
    }

    /* Item sélectionné */
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {
        color: #a5b4fc !important;
        background: rgba(99,102,241,0.15) !important;
        border-color: rgba(99,102,241,0.4) !important;
    }

    /* Masquer les boutons radio natifs */
    [data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    /* Masquer le label généré "Aller à" */
    [data-testid="stSidebar"] [data-testid="stRadio"] > label:first-child {
        display: none !important;
    }

    /* Footer de la sidebar */
    .sidebar-footer {
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        color: #374151;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #1e1e2e;
        letter-spacing: 0.05em;
    }

    .sidebar-footer span {
        color: #6366f1;
    }

    /* === CONTENU PRINCIPAL === */
    [data-testid="stMain"] {
        background: #07070d;
    }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
        color: #f1f5f9 !important;
    }

    p, li, div {
        font-family: 'Space Mono', monospace !important;
        color: #9ca3af;
        font-size: 0.85rem;
    }

    /* Badge info */
    [data-testid="stAlert"] {
        background: rgba(99,102,241,0.08) !important;
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 10px !important;
        color: #a5b4fc !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.78rem !important;
    }

    /* Tag version en sidebar */
    .nav-tag {
        display: inline-block;
        font-size: 0.6rem;
        background: rgba(99,102,241,0.2);
        color: #818cf8;
        border-radius: 4px;
        padding: 1px 5px;
        margin-left: 4px;
        font-family: 'Space Mono', monospace;
        vertical-align: middle;
    }
    </style>
    """, unsafe_allow_html=True)

    # 2. Barre latérale (Navigation)
    with st.sidebar:
        st.markdown("""
        <div style="
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 1rem;
            color: #6366f1;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            padding: 1.5rem 0.5rem 0.25rem;
        "> Portfolio</div>
        <hr style="border-color:#1e1e2e; margin: 0.5rem 0 1rem;">
        """, unsafe_allow_html=True)

        nav_items = {
            " Accueil": "Accueil",
            "  Projets": "Projets",
            "  Compétences": "Compétences",
            "  Contact": "Contact",
        }

        selection_label = st.radio(
            label="",
            options=list(nav_items.keys()),
            label_visibility="collapsed"
        )
        selection = nav_items[selection_label]

        st.markdown("""
        <div class="sidebar-footer">
            v1.0.0 &nbsp;·&nbsp; <span>Arthur S.</span><br>
            Data Engineer Junior
        </div>
        """, unsafe_allow_html=True)

    # 3. Logique d'affichage
    if selection == "Accueil":
        render_header()
    elif selection == "Projets":
        render_projects()
    elif selection == "Compétences":
        render_skill()
    

def render_header():
    # Utilisation de colonnes pour séparer le texte d'une éventuelle image ou d'un badge
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("SITCHEPING Arthur")
        st.subheader("Data Engineer Junior | Spécialiste Big Data & Pipelines Scalables")
        st.markdown("""
        **Expertise :** Transformer des flux de données brutes en assets stratégiques.  
        Passionné par l'optimisation des architectures et la fiabilité des données.
        """)
    
    with col2:
        # On pourrait ici ajouter une photo ou un badge de certification
        st.info("Basé à Valence (France) \n\n 🎓 Dernière année Big Data")

def render_projects():
    st.header("Mes Projets")
    # C'est ici qu'on construira les "cartes" de projets avec schémas et liens GitHub

if __name__ == "__main__":
    main()