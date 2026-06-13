import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# =====================================
# CONFIGURATION DE LA PAGE
# =====================================

st.set_page_config(
    page_title="Gestion de Stock Pro",
    page_icon="📦",
    layout="wide"
)

# =====================================
# MENU LATÉRAL
# =====================================

st.sidebar.title("📦 Gestion Stock Pro")

menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Tableau de bord",
        "➕ Ajouter un produit",
        "🔍 Rechercher un produit",
        "📋 Liste des produits",
        "✏️ Modifier un produit",
        "🗑️ Supprimer un produit"
    ]
)

# =====================================
# STYLE PERSONNALISÉ
# =====================================

st.markdown("""
<style>

/* ====== GLOBAL ====== */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white !important;
    font-family: 'Segoe UI';
}

/* ====== TITRES ====== */
h1, h2, h3 {
    color: white !important;
}

/* ====== SIDEBAR ====== */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 500;
}

/* ====== BOUTONS ====== */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

/* ====== METRICS GLOBAL FIX (TOUTES PAGES) ====== */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

/* FORCE TOUT DANS LES METRICS (IMPORTANT) */
div[data-testid="stMetric"] * {
    color: white !important;
}

/* LABEL */
div[data-testid="stMetricLabel"] {
    color: white !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* VALUE */
div[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 28px !important;
    font-weight: bold !important;
}

/* DELTA */
div[data-testid="stMetricDelta"] {
    color: white !important;
}
                        
/* ====== DATAFRAME ====== */
div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# CONNEXION GOOGLE SHEETS
# =====================================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("GestionStock").worksheet("Feuille 1")

# =====================================
# RÉCUPÉRATION DES DONNÉES
# =====================================

data = sheet.get_all_records()

df = pd.DataFrame(data)

# =====================================
# TITRE
# =====================================

st.markdown("""
<h1 style='color:#8A2BE2;'>
📦 Gestion de Stock Pro
</h1>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("📊 Application de gestion de stock moderne et intuitive")

# =====================================
# AFFICHAGE DES MESSAGES
# =====================================

if "message" in st.session_state:
    if st.session_state["type"] == "success":
        st.success(st.session_state["message"])
    elif st.session_state["type"] == "error":
        st.error(st.session_state["message"])
    elif st.session_state["type"] == "warning":
        st.warning(st.session_state["message"])

    del st.session_state["message"]
    del st.session_state["type"]
# =====================================
# TABLEAU DE BORD
# =====================================

if menu == "📊 Tableau de bord":

    st.header("📈 Tableau de bord")

    if not df.empty:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Nombre de produits",
                len(df)
            )

        with col2:
            st.metric(
                "Stock total",
                int(df["Stock"].sum())
            )

        with col3:
            st.metric(
                "Valeur totale du stock",
                f"{df['Total'].sum():.2f}"
            )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("Aucun produit enregistré.")

# =====================================
# AJOUT PRODUIT
# =====================================

elif menu == "➕ Ajouter un produit":

    st.subheader("➕ Ajouter un produit")

    col1, col2 = st.columns(2)

    with col1:
        nom = st.text_input("Nom du produit")

    with col2:
        categorie = st.selectbox(
            "Catégorie",
            [
                "Chaussures",
                "Vêtements",
                "Accessoires"
            ]
        )

    col3, col4 = st.columns(2)

    with col3:
        prix = st.number_input(
            "Prix",
            min_value=0.0,
            format="%.2f"
        )

    with col4:
        stock = st.number_input(
            "Stock",
            min_value=0,
            step=1
        )

    total = prix * stock

    st.markdown("### 📊 Résumé")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Prix", f"{prix:.2f}")

    with c2:
        st.metric("Stock", stock)

    with c3:
        st.metric(
            "Valeur Totale",
            f"{total:.2f}"
        )

    if st.button("💾 Ajouter le produit"):

        if nom.strip() == "":
            st.error(
                "Veuillez saisir un nom de produit."
            )

        else:

            nouvelle_ligne = [
                nom,
                categorie,
                prix,
                stock,
                total
            ]

            sheet.append_row(
                nouvelle_ligne
            )

            st.success(
                "✅ Produit ajouté avec succès !"
            )

# =====================================
# RECHERCHER UN PRODUIT
# =====================================

elif menu == "🔍 Rechercher un produit":

    st.header("🔍 Rechercher un produit")

    recherche = st.text_input(
        "Tapez le nom d'un produit"
    )

    if recherche:

        resultat = df[
            df["Nom_du_produit"]
            .astype(str)
            .str.contains(
                recherche,
                case=False,
                na=False
            )
        ]

        if resultat.empty:

            st.warning(
                "Aucun produit trouvé."
            )

        else:

            st.success(
                f"{len(resultat)} résultat(s) trouvé(s)"
            )

            st.dataframe(
                resultat,
                use_container_width=True
            )

# =====================================
# LISTE DES PRODUITS
# =====================================

elif menu == "📋 Liste des produits":

    st.header("📋 Liste des produits")

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.warning(
            "Aucun produit enregistré."
        )

# =====================================
# MODIFIER UN PRODUIT
# =====================================

elif menu == "✏️ Modifier un produit":

    st.header("✏️ Modifier un produit")

    if not df.empty:

        produit = st.selectbox(
            "Choisissez un produit",
            df["Nom_du_produit"]
        )

        ligne = df[
            df["Nom_du_produit"] == produit
        ].iloc[0]

        nouveau_nom = st.text_input(
            "Nom du produit",
            value=ligne["Nom_du_produit"]
        )

        nouvelle_categorie = st.selectbox(
            "Catégorie",
            [
                "Chaussures",
                "Vêtements",
                "Accessoires"
            ],
            index=[
                "Chaussures",
                "Vêtements",
                "Accessoires"
            ].index(ligne["Catégorie"])
            if ligne["Catégorie"] in ["Chaussures", "Vêtements", "Accessoires"]
            else 0
        )

        nouveau_prix = st.number_input(
            "Prix",
            value=float(ligne["Prix"])
        )

        nouveau_stock = st.number_input(
            "Stock",
            value=int(ligne["Stock"])
        )

        nouveau_total = nouveau_prix * nouveau_stock

        st.metric(
            "Nouveau Total",
            f"{nouveau_total:.2f}"
        )

        if st.button("💾 Mettre à jour"):

            lignes = sheet.get_all_values()

            for i, row in enumerate(lignes):

                if i > 0 and row[0] == produit:

                    sheet.update(
                        f"A{i+1}:E{i+1}",
                        [[
                            nouveau_nom,
                            nouvelle_categorie,
                            nouveau_prix,
                            nouveau_stock,
                            nouveau_total
                        ]]
                    )

                    st.session_state["message"] = "Produit modifié avec succès."
                    st.session_state["type"] = "success"
                    st.rerun()

    else:
        st.warning("Aucun produit disponible.")


# =====================================
# SUPPRIMER UN PRODUIT
# =====================================

elif menu == "🗑️ Supprimer un produit":

    st.header("🗑️ Supprimer un produit")

    if not df.empty:

        produit = st.selectbox(
            "Choisissez un produit à supprimer",
            df["Nom_du_produit"]
        )

        st.warning(
            f"Vous êtes sur le point de supprimer : {produit}"
        )

        if st.button("❌ Supprimer définitivement"):

            lignes = sheet.get_all_values()

            for i, ligne in enumerate(lignes):

                if i > 0 and ligne[0] == produit:

                    sheet.delete_rows(i + 1)

                    st.session_state["message"] = f"{produit} supprimé avec succès."
                    st.session_state["type"] = "success"
                    st.rerun()

    else:
        st.warning("Aucun produit disponible.")

