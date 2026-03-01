import streamlit as st


# ===========================================================================
# MODELE DE DONNEES — PROJECTS
#
# Structure standardisee pour chaque projet :
#   title             (str)        Titre affiché dans le hero et le selectbox
#   subtitle          (str)        Accroche courte — la valeur metier en une ligne
#   description       (str)        Corps Markdown — contexte et approche technique
#   stack             (list[str])  Outils et technologies utilises
#   metrics           (list[dict]) KPIs : cles "label", "value", "delta" (optionnel)
#   visuals           (dict)       Chemins media : "architecture" et/ou "preview"
#   github_url        (str|None)   Lien vers le depot
#   status            (str)        "production" | "en-cours" | "archive"
#
# Ajouter un projet = append un dict dans cette liste.
# Le code d'affichage ne change pas.
# ===========================================================================
PROJECTS = [
    {
        "title": "Scraping & Centralisation des Offres d'Emploi",
        "subtitle": "Centraliser en une seule source les offres Data dispersees sur 5 plateformes.",
        "description": """
Script Python planifie via **cron** qui collecte chaque matin les offres d'emploi Data
sur LinkedIn, Indeed et Welcome to the Jungle.

Les donnees sont **dedupliquees par hash d'empreinte** (titre + entreprise + localisation),
puis inserees dans une base **SQLite** locale consultable via une interface Streamlit dediee.

Le pipeline tourne sans intervention manuelle depuis 3 mois.
        """,
        "stack": ["Python", "BeautifulSoup", "Pandas", "SQLite", "Cron"],
        "metrics": [
            {"label": "Plateformes couvertes", "value": "5",      "delta": None},
            {"label": "Offres collectees/jour", "value": "~120",  "delta": None},
            {"label": "Taux de doublons",        "value": "0%",    "delta": "-100%"},
        ],
        # Ajouter les chemins quand les images sont disponibles :
        # "visuals": {"architecture": "images/schema_scraping.png", "preview": "images/ui_scraping.png"}
        "visuals": {},
        "github_url": "https://github.com/arthur-sitcheping/job-scraper",
        "status": "archive",
    },
    {
        "title": "Pipeline de Logs Temps Reel — Kafka + Spark Streaming",
        "subtitle": "Reduire la latence de detection d'anomalies de 4 heures a 10 minutes.",
        "description": """
Remplacement d'une architecture **Lambda** (batch + speed layer) par un pipeline **Kappa**
full streaming, plus simple a maintenir et plus coherent sur la donnee.

Les evenements applicatifs sont produits dans **Kafka** (3 brokers, replication factor 2),
consommes par **Spark Structured Streaming** toutes les 30 secondes, enrichis avec des
regles metier configurables, puis persistes dans **PostgreSQL**.

Un DAG **Airflow** orchestre les jobs de reconciliation quotidienne et envoie des alertes
PagerDuty en cas d'ecart de volume superieur a 5%.
        """,
        "stack": ["Apache Kafka", "Apache Spark", "Python", "PostgreSQL", "Airflow", "Docker"],
        "metrics": [
            {"label": "Latence de traitement", "value": "10 min",  "delta": "-97%"},
            {"label": "Volume journalier",      "value": "12 Go",   "delta": None},
            {"label": "Disponibilite",          "value": "99.94%",  "delta": "+1.2%"},
            {"label": "Alertes manquees",        "value": "0",       "delta": "-100%"},
        ],
        "visuals": {},
        "github_url": "https://github.com/arthur-sitcheping/realtime-log-pipeline",
        "status": "production",
    },
]


# ===========================================================================
# CSS MINIMAL
# Uniquement ce qui ne peut pas etre fait avec les composants natifs Streamlit :
# - Theming de la sidebar (fond sombre, radio stylise)
# - Centrage du titre hero projet
# - Overrides st.metric pour coherence dark theme
# ===========================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a0f;
    border-right: 1px solid #1e1e2e;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    color: #6b7280 !important;
    padding: 0.6rem 1rem !important;
    border-radius: 8px;
    border: 1px solid transparent;
    transition: border-color 0.15s;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    color: #e2e8f0 !important;
    background: rgba(99,102,241,0.08) !important;
    border-color: rgba(99,102,241,0.2) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
    color: #a5b4fc !important;
    background: rgba(99,102,241,0.15) !important;
    border-color: rgba(99,102,241,0.4) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display: none !important; }

/* Fond principal */
[data-testid="stMain"] { background: #07070d; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #f1f5f9 !important; }

/* Titre hero : centrage uniquement */
.hero-title {
    text-align: center;
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 0.25rem;
}

/* st.metric dark overrides */
[data-testid="stMetric"] {
    background: #0e0e1a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.62rem !important;
    color: #6b7280 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.4rem !important;
    color: #f1f5f9 !important;
    font-weight: 800 !important;
}
</style>
"""


# ===========================================================================
# HELPER
# ===========================================================================

def get_project_by_title(title: str) -> dict:
    """Retourne le dict du projet correspondant au titre selectionne."""
    return next(p for p in PROJECTS if p["title"] == title)


# ===========================================================================
# COMPOSANTS D'AFFICHAGE
# ===========================================================================

def render_page_header(config: dict):
    """
    Header de page commun (Accueil, Projets, Competences, Contact).
    Utilise st.markdown + st.caption — pas de HTML complexe.
    """
    # Badge de section
    accent = config["accent"]
    tag    = config["tag"]
    st.markdown(
        f"<span style='font-family:monospace; font-size:0.65rem; "
        f"letter-spacing:0.2em; text-transform:uppercase; "
        f"color:{accent}; border:1px solid {accent}; "
        f"padding:2px 10px; border-radius:20px;'>{tag}</span>",
        unsafe_allow_html=True,
    )

    st.markdown(f"## {config['title']}")
    st.caption(config["subtitle"])
    st.divider()


def render_home_content():
    """Contenu de la page Accueil — composants natifs uniquement."""
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Data Engineer Junior | Specialiste Big Data & Pipelines Scalables")
        st.markdown(
            "**Expertise :** Transformer des flux de donnees brutes en assets strategiques.  \n"
            "Passionne par l'optimisation des architectures et la fiabilite des donnees."
        )

    with col2:
        st.info("Base a Valence (France)\n\nDerniere annee Big Data")


def render_project_hero(project: dict):
    """
    Bandeau titre pleine largeur centre.

    On utilise st.markdown avec unsafe_allow_html uniquement pour le centrage
    du titre (impossible nativement dans Streamlit).
    Le sous-titre et la description utilisent des composants natifs.
    """
    # Couleur du badge selon le statut — mapping simple
    status_colors = {
        "production": "#10b981",
        "en-cours":   "#f59e0b",
        "archive":    "#6b7280",
    }
    color = status_colors.get(project["status"], "#6b7280")

    # Badge statut — centré via HTML minimal
    st.markdown(
        f"<div style='text-align:center; margin-bottom:0.5rem;'>"
        f"<span style='font-family:monospace; font-size:0.6rem; "
        f"letter-spacing:0.15em; text-transform:uppercase; "
        f"color:{color}; border:1px solid {color}; "
        f"padding:2px 12px; border-radius:20px;'>{project['status']}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # Titre H1 centré — seule vraie raison de garder unsafe_allow_html ici
    st.markdown(
        f"<div class='hero-title'>{project['title']}</div>",
        unsafe_allow_html=True,
    )

    # Sous-titre (accroche metier) — st.markdown natif, gras
    st.markdown(
        f"<p style='text-align:center; font-weight:700; color:#cbd5e1; "
        f"font-family:monospace; font-size:0.85rem; margin-top:0.5rem;'>"
        f"{project['subtitle']}</p>",
        unsafe_allow_html=True,
    )

    # Description longue — st.markdown natif (supporte le Markdown complet)
    with st.expander("Voir le detail du projet", expanded=True):
        st.markdown(project["description"])

    st.divider()


def render_stack_col(stack: list, github_url: str = None):
    """
    Colonne gauche (ratio 1) : Stack Technique.

    Utilise st.code() pour chaque outil → rendu "terminal-style" natif.
    Pas de HTML injecte.
    """
    st.caption("STACK TECHNIQUE")

    # Boucle sur la liste : chaque outil = un st.code independant
    # language="" desactive la coloration syntaxique pour un rendu neutre
    for tool in stack:
        st.code(tool, language="")

    # Lien GitHub avec st.link_button (composant natif Streamlit)
    if github_url:
        st.markdown("---")
        st.link_button("Voir sur GitHub", github_url)


def render_showcase_col(metrics: list = None, visuals: dict = None):
    """
    Colonne droite (ratio 3) : KPIs + Media.

    KPIs  : st.columns dynamiques basees sur len(metrics)
            → autant de colonnes que de metriques, zero CSS necessaire

    Media : st.image() pour chaque entree du dict visuals
            → gestion de la largeur automatique avec use_container_width
    """

    # --- Section KPIs ---
    if metrics:
        st.caption("INDICATEURS DE PERFORMANCE")

        # st.columns(n) : n colonnes ajustees automatiquement a la largeur disponible
        # C'est le pattern "data-driven layout" : la donnee pilote le layout
        metric_cols = st.columns(len(metrics))

        for col, metric in zip(metric_cols, metrics):
            with col:
                st.metric(
                    label=metric["label"],
                    value=metric["value"],
                    delta=metric.get("delta"),  # .get() → None si cle absente, pas d'erreur
                )

        st.markdown("---")

    # --- Section Media ---
    st.caption("ARCHITECTURE & VISUELS")

    if visuals:
        # On itere sur le dict visuals — chaque cle est un label, chaque valeur un chemin
        for label, path in visuals.items():
            st.image(path, caption=label, use_container_width=True)
    else:
        # st.info() remplace le placeholder HTML — composant natif, lisible
        st.info(
            "Schemas d'architecture a ajouter.  \n"
            "Renseigner la cle `visuals` dans le dict du projet :  \n"
            '`"visuals": {"architecture": "images/schema.png"}`'
        )


# ===========================================================================
# PAGE PROJETS
# ===========================================================================

def render_projects():
    """
    Orchestration de la page Projets en 4 etapes.

    Le principe "data-driven" applique ici :
    les donnees de PROJECTS pilotent entierement le layout.
    Ajouter un projet = 0 modification du code d'affichage.

    Etape 1 — Router    : selectbox en haut droite
    Etape 2 — Lookup    : recuperation du dict projet (separation donnees/affichage)
    Etape 3 — Hero      : titre + sous-titre + description centres
    Etape 4 — Dashboard : col_stack (1) | col_showcase (3)
    """

    # ------------------------------------------------------------------
    # ETAPE 1 — Selectbox router positionne en haut a droite
    # st.columns([3, 1]) : le spacer vide pousse le widget vers la droite
    # ------------------------------------------------------------------
    spacer, nav_col = st.columns([3, 1])

    with nav_col:
        # Liste des titres extraite dynamiquement depuis PROJECTS
        project_titles = [p["title"] for p in PROJECTS]

        selected_title = st.selectbox(
            label="Choisir un projet",
            options=project_titles,
        )

    # ------------------------------------------------------------------
    # ETAPE 2 — Recuperation des donnees
    # Cette ligne est la seule qui connait la structure de PROJECTS.
    # Si on migrait vers une BDD, seule cette ligne changerait.
    # ------------------------------------------------------------------
    project = get_project_by_title(selected_title)

    # ------------------------------------------------------------------
    # ETAPE 3 — Hero pleine largeur
    # ------------------------------------------------------------------
    render_project_hero(project)

    # ------------------------------------------------------------------
    # ETAPE 4 — Dashboard bicolonne asymetrique (ratio 1 : 3)
    # col_stack   = sidebar interne dedie a la stack
    # col_showcase = zone principale KPIs + media
    # ------------------------------------------------------------------
    col_stack, col_showcase = st.columns([1, 3], gap="large")

    with col_stack:
        render_stack_col(
            stack=project["stack"],
            github_url=project.get("github_url"),
        )

    with col_showcase:
        render_showcase_col(
            metrics=project.get("metrics"),
            visuals=project.get("visuals"),
        )


# ===========================================================================
# POINT D'ENTREE
# ===========================================================================

def main():
    st.set_page_config(page_title="Data Portfolio — Arthur S.", layout="wide")

    # CSS minimal injecte une seule fois
    st.markdown(CSS, unsafe_allow_html=True)

    # --- Sidebar : navigation principale ---
    with st.sidebar:
        st.markdown(
            "<div style='font-family:Syne,sans-serif; font-weight:800; font-size:1rem; "
            "color:#6366f1; letter-spacing:0.18em; text-transform:uppercase; "
            "padding:1.5rem 0.5rem 0.25rem;'>Portfolio</div>"
            "<hr style='border-color:#1e1e2e; margin:0.5rem 0 1rem;'>",
            unsafe_allow_html=True,
        )

        selection = st.radio(
            label="Navigation",
            options=["Accueil", "Projets", "Competences", "Contact"],
            label_visibility="collapsed",
        )

        st.markdown(
            "<div style='font-family:monospace; font-size:0.68rem; color:#374151; "
            "padding:1rem; margin-top:2rem; border-top:1px solid #1e1e2e;'>"
            "v1.0.0 · <span style='color:#6366f1'>Arthur S.</span><br>"
            "Data Engineer Junior</div>",
            unsafe_allow_html=True,
        )

    # --- Config des headers par page ---
    # Dict lookup : O(1), plus lisible qu'une chaine de if/elif
    page_headers = {
        "Accueil": {
            "tag": "Bienvenue",
            "title": "SITCHEPING Arthur",
            "subtitle": "Bienvenue sur mon portfolio · Data Engineer Junior",
            "accent": "#6366f1",
        },
        "Projets": {
            "tag": "Showcase",
            "title": "Mes Projets",
            "subtitle": "Pipelines, architectures Big Data et outils d'analyse.",
            "accent": "#06b6d4",
        },
        "Competences": {
            "tag": "Stack",
            "title": "Competences",
            "subtitle": "Outils et frameworks pour construire des solutions data robustes.",
            "accent": "#10b981",
        },
        "Contact": {
            "tag": "Contact",
            "title": "Me Contacter",
            "subtitle": "Un projet data ? Une opportunite ? Ecrivons-nous.",
            "accent": "#f59e0b",
        },
    }

    # Header dynamique commun a toutes les pages
    render_page_header(page_headers[selection])

    # Routage vers le contenu de la page selectionnee
    if selection == "Accueil":
        render_home_content()
    elif selection == "Projets":
        render_projects()
    elif selection == "Competences":
        st.info("Section a venir.")
    elif selection == "Contact":
        st.info("Section a venir.")


if __name__ == "__main__":
    main()