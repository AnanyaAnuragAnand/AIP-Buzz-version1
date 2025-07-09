import streamlit as st
import pickle
import numpy as np
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from propy.CTD import CalculateC as calC, CalculateT as calT, CalculateD as calD

# Load your trained model
model = pickle.load(open('aipid_model.pkl', 'rb'))

# ProtParam feature extractor for a single sequence
def extract_protparam_features(sequence):
    protein_analysis = ProteinAnalysis(sequence)
    features = {
        "Molecular Weight": protein_analysis.molecular_weight(),
        "Isoelectric Point": protein_analysis.isoelectric_point(),
        "Aromaticity": protein_analysis.aromaticity(),
        "GRAVY": protein_analysis.gravy(),
        "Instability Index": protein_analysis.instability_index(),
        "Flexibility Mean": sum(protein_analysis.flexibility())/len(protein_analysis.flexibility())
    }
    aa_composition = protein_analysis.count_amino_acids()
    features.update(aa_composition)
    return features

# Propy features extractor for a single sequence
def extract_propy_features(sequence):
    dictC = calC(sequence)
    dictT = calT(sequence)
    dictD = calD(sequence)
    features = {}
    features.update(dictC)
    features.update(dictT)
    features.update(dictD)
    return features

# Streamlit interface
st.title("🧬 Anti-Inflammatory Peptide Identification (AIPID)")

user_sequence = st.text_area("Paste your peptide sequence (sequence to be at least 10 amino acids long) (single-letter amino acid codes only):")

if st.button("Predict"):
    if len(user_sequence.strip()) == 0:
        st.error("Please enter a valid peptide sequence.")
    elif 'X' in user_sequence:
        st.error("Invalid sequence: contains unknown amino acid 'X'.")
    else:
        try:
            protparam_feats = extract_protparam_features(user_sequence)
            propy_feats = extract_propy_features(user_sequence)

            combined_features = {**propy_feats, **protparam_feats}
            df = pd.DataFrame([combined_features])

            # Handle missing features by adding zero columns for any missing model features
            model_features = model.feature_names_in_
            for feature in model_features:
                if feature not in df.columns:
                    df[feature] = 0

            df = df[model_features]

            prediction = model.predict(df)[0]
            prob = model.predict_proba(df)[0][prediction]

            if prediction == 1:
                st.success(f"🟢 Predicted: Anti-Inflammatory Peptide (Confidence: {prob:.2f})")
            else:
                st.error(f"🔴 Predicted: Non-Anti-Inflammatory Peptide (Confidence: {prob:.2f})")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
