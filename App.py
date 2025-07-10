import streamlit as st

st.set_page_config(
    page_title="AIPID - Anti-Inflammatory Peptide Identification",
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

# --- Welcome Box ---
st.markdown("""
<style>
    .intro-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4e7ddc;
        font-size: 16px;
        color: #333333;
    }
</style>
<div class='intro-box'>
    <h3>👋 Welcome to AIPID (Anti-Inflammatory Peptide Identification)</h3>
    <p>
        AIPID is a machine learning tool designed to predict whether a peptide has anti-inflammatory properties 
        based on its amino acid sequence. It uses descriptors from <b>Biopython</b> and <b>Propy3</b> 
        and is trained using a Random Forest model.
    </p>
    <p>
        Enter a peptide sequence (min. <b>10 amino acids</b>) below to get started.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Symbols and Title ---
st.markdown("""
<div style='text-align: center; font-size: 36px;'>🧬 ↬ ∿ 🌀</div>
<h1 style='text-align: center;'>Anti-Inflammatory Peptide Identification (AIPID)</h1>
<p style='text-align: center;'>Paste your peptide sequence below (at least <b>10 amino acids</b>, single-letter codes only):</p>
""", unsafe_allow_html=True)

# --- Input ---
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    user_sequence = st.text_input("➤ Enter Peptide Sequence", key="sequence_input")

    st.info("📌 Example: `KKLLDERVAKL` — use only standard 1-letter amino acid codes.")

# --- Predict Button ---
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([2, 1, 2])
with btn_col2:
    predict_clicked = st.button("🔍 Predict")

# --- Feature Extraction ---
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

# --- Prediction ---
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
