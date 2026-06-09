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
# STYLE PERSONNALISÉ
# =====================================

st.markdown("""
<style>

.stApp {
    background-color: white;
}

h1 {
    text-align: center;
}

.stButton > button {
    background-color: #C62828;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #8A2BE2;
    color: white;
}

div[data-testid="stMetric"] {
    background-color: black;
    padding: 15px;
    border-radius: 10px;
    color: white;
    text-align: center;
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
# TITRE
# =====================================

st.markdown("""
<h1 style='color:#8A2BE2;'>
📦 Gestion de Stock Pro
</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================
# FORMULAIRE
# =====================================

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

# =====================================
# CALCUL DU TOTAL
# =====================================

total = prix * stock

st.markdown("### 📊 Résumé")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Prix", f"{prix:.2f}")

with c2:
    st.metric("Stock", stock)

with c3:
    st.metric("Valeur Totale", f"{total:.2f}")

# =====================================
# AJOUT PRODUIT
# =====================================

if st.button("💾 Ajouter le produit"):

    if nom.strip() == "":
        st.error("Veuillez saisir un nom de produit.")
    else:

        nouvelle_ligne = [
            nom,
            categorie,
            prix,
            stock,
            total
        ]

        sheet.append_row(nouvelle_ligne)

        st.success("✅ Produit ajouté avec succès !")

# =====================================
# RÉCUPÉRATION DES DONNÉES
# =====================================

data = sheet.get_all_records()

df = pd.DataFrame(data)

# =====================================
# TABLEAU DE BORD
# =====================================

st.markdown("---")
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

# =====================================
# RECHERCHE
# =====================================

st.markdown("---")
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

    st.dataframe(
        resultat,
        use_container_width=True
    )

# =====================================
# TABLEAU DES PRODUITS
# =====================================

st.markdown("---")
st.header("📋 Liste des produits")

st.dataframe(
    df,
    use_container_width=True
)