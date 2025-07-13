import streamlit as st

st.set_page_config(
    page_title="AIPID: Your Gateway to Anti-Inflammatory Peptide Discovery",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded"
)

import pickle
import numpy as np
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from propy.CTD import CalculateC as calC, CalculateT as calT, CalculateD as calD

# Load model
model = pickle.load(open('aipid_model.pkl', 'rb'))

# --- Custom Styles ---
st.markdown("""
<style>
    .welcome-banner {
        background: linear-gradient(90deg, #e3f2fd 0%, #fce4ec 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        border-left: 8px solid #7b1fa2;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .welcome-banner h2 {
        color: #4a148c;
        font-size: 28px;
        margin-bottom: 10px;
    }
    .welcome-banner p {
        font-size: 16px;
        color: #333;
    }
</style>

<div class='welcome-banner'>
    <h2>👋 Welcome to <b>AIPID: Your Gateway to Anti-Inflammatory Peptide Discovery</b></h2>
    <p>
        AIPID (Anti-Inflammatory Peptide Identification) server allows you to browse curated peptides, explore features,
        and predict novel anti-inflammatory sequences using cutting-edge machine learning.
    </p>
    <p>
        Powered by <b>AIPID's MAD-ML model</b>, a Random Forest-based engine trained on 
        motif-filtered, biologically relevant peptides using descriptors from <b>Biopython</b> and <b>Propy3</b>.
    </p>
    <p>
        Enter a peptide sequence below to get started (minimum <b>10 amino acids</b>).
    </p>
</div>
""", unsafe_allow_html=True)

# --- Symbols and Title ---
st.markdown("""
<div style='text-align: center; font-size: 36px;'>🧬 ↬ ∿ 🌀</div>
<h2 style='text-align: center;'>MAD-ML-Based Anti-Inflammatory Peptide Identification (AIPID) Tool</h2>
<p style='text-align: center;'>Paste your peptide sequence below (at least <b>10 amino acids</b>, single-letter codes only):</p>
""", unsafe_allow_html=True)

# --- Input Box ---
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    user_sequence = st.text_input("➤ Enter Peptide Sequence", key="sequence_input")
    st.info("📌 Example: `KKLLDERVAKL` — use only standard 1-letter amino acid codes.")

# # --- Predict Button ---
# st.markdown("<br>", unsafe_allow_html=True)
# btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 2])
# with btn_col2:
#     predict_clicked = st.button("🔍 Click for Predict")


# --- Predict Button ---
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 2])

with btn_col2:
    inner_col1, inner_col2 = st.columns([1, 1])  # Adjust ratio if needed
    with inner_col1:
        predict_clicked = st.button("🔍 Click for Predict")
    with inner_col2:
        st.markdown("⬇️ **Scroll down for results**", unsafe_allow_html=True)



# --- Feature Extraction Functions ---
def extract_protparam_features(sequence):
    protein_analysis = ProteinAnalysis(sequence)
    features = {
        "Molecular Weight": protein_analysis.molecular_weight(),
        "Isoelectric Point": protein_analysis.isoelectric_point(),
        "Aromaticity": protein_analysis.aromaticity(),
        "GRAVY": protein_analysis.gravy(),
        "Instability Index": protein_analysis.instability_index(),
        "Flexibility Mean": sum(protein_analysis.flexibility()) / len(protein_analysis.flexibility())
    }
    aa_composition = protein_analysis.count_amino_acids()
    features.update(aa_composition)
    return features

def extract_propy_features(sequence):
    dictC = calC(sequence)
    dictT = calT(sequence)
    dictD = calD(sequence)
    features = {}
    features.update(dictC)
    features.update(dictT)
    features.update(dictD)
    return features

# --- Prediction Logic ---
if predict_clicked:
    sequence = user_sequence.strip().upper()

    if not sequence:
        st.error("❗ Please enter a peptide sequence.")
    elif len(sequence) < 10:
        st.warning("⚠️ Sequence must be at least 10 amino acids long.")
    elif any(res not in "ACDEFGHIKLMNPQRSTVWY" for res in sequence):
        st.error("❌ Invalid characters found! Use standard amino acids (A–Z, excluding B, J, O, U, X, Z).")
    else:
        try:
            protparam_feats = extract_protparam_features(sequence)
            propy_feats = extract_propy_features(sequence)

            combined_features = {**propy_feats, **protparam_feats}
            df = pd.DataFrame([combined_features])

            # Fill missing columns if any
            model_features = model.feature_names_in_
            for feature in model_features:
                if feature not in df.columns:
                    df[feature] = 0
            df = df[model_features]

            prediction = model.predict(df)[0]
            prob = model.predict_proba(df)[0][prediction]

            st.markdown("---")
            if prediction == 1:
                st.success(f"🟢 **Predicted: Anti-Inflammatory Peptide**  \n✅ Confidence: `{prob:.2f}`")
            else:
                st.error(f"🔴 **Predicted: Non-Anti-Inflammatory Peptide**  \n❌ Confidence: `{prob:.2f}`")

        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
