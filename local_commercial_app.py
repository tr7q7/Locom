import streamlit as st
import matplotlib.pyplot as plt

# --- Configuration de la page ---
st.set_page_config(page_title="CF Local Commercial", page_icon="🏢", layout="centered")

# --- Style CSS personnalisé ---
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-size: 110% !important;
            color: white !important;
        }
        h1 {
            font-size: 2em !important;
        }
        .stSlider > div > div {
            color: white !important;
        }
        .stSlider > div > div > div[role="slider"] {
            background-color: orange !important;
            border: 1px solid white;
            height: 150px !important;
            width: 150px !important;
        }
        input[type=number] {
            font-size: 1em !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("CF Local Commercial (SCI à l'IS)")

st.markdown("#### 🔕 Informations générales")

prix_bien = st.slider("Prix du local", 30000, 1000000, step=10000, value=250000, format="€%d")
travaux = st.slider("Montant des travaux", 0, 300000, step=5000, value=50000, format="€%d")
loyer = st.slider("Loyer mensuel HT", 500, 10000, step=100, value=2500, format="€%d")
taxe_fonciere = st.slider("Taxe foncière annuelle", 500, 10000, step=100, value=1500, format="€%d")
charges = st.slider("Charges annuelles (assurance, entretien...)", 0, 10000, step=100, value=2000, format="€%d")
taux_credit = st.slider("Taux du crédit", 0.0, 5.0, step=0.1, value=2.0, format="%.2f %%")
duree_credit = st.slider("Durée du crédit", 10, 30, step=1, value=20, format="%d ans")

st.markdown("#### 🔢 Calculs")

if st.button("Calculer"):
    duree_credit_mois = duree_credit * 12
    taux_mensuel = taux_credit / 100 / 12
    frais_notaire = prix_bien * 0.08
    montant_emprunte = prix_bien + travaux + frais_notaire

    if taux_mensuel > 0:
        mensualite = montant_emprunte * (taux_mensuel / (1 - (1 + taux_mensuel) ** -duree_credit_mois))
    else:
        mensualite = montant_emprunte / duree_credit_mois

    loyer_annuel = loyer * 12
    interets_annuels = montant_emprunte * taux_credit / 100
    amort_bien = prix_bien / 25
    amort_travaux = travaux / 10
    amort_notaire = frais_notaire / 10

    dotation = amort_bien + amort_travaux + amort_notaire

    resultat_comptable = loyer_annuel - taxe_fonciere - charges - interets_annuels - dotation

    if resultat_comptable <= 42500:
        impot = max(resultat_comptable * 0.15, 0)
    else:
        impot = 42500 * 0.15 + (resultat_comptable - 42500) * 0.25

    credit_annuel = mensualite * 12
    cashflow = loyer_annuel - taxe_fonciere - charges - credit_annuel - impot
    rendement = (cashflow / montant_emprunte) * 100

    st.markdown(f"### 💶 Cashflow annuel : <span style='color:lime'>{cashflow:.2f} €</span>", unsafe_allow_html=True)
    st.markdown(f"### 📈 Rendement : <span style='color:violet'>{rendement:.2f} %</span>", unsafe_allow_html=True)

    with st.expander("Voir les détails"):
        st.write(f"Loyer annuel : {loyer_annuel} €")
        st.write(f"Charges totales : {charges + taxe_fonciere} €")
        st.write(f"Intérêts annuels : {interets_annuels:.0f} €")
        st.write(f"Amortissements : {dotation:.0f} €")
        st.write(f"Impôt sur les sociétés : {impot:.0f} €")
        st.write(f"Mensualité : {mensualite:.2f} €/mois")
        st.write(f"Crédit annuel : {credit_annuel:.0f} €")
        st.write(f"Frais de notaire : {frais_notaire:.0f} €")
