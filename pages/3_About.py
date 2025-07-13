import streamlit as st

st.title("📖 About AIPID")

st.write("""
**AIPID** is your one-stop platform for exploring and predicting anti-inflammatory peptides (AIPs). This web-based tool allows you to browse curated AIPs, visualize their physicochemical profiles, and predict novel sequences.

---

### 🔬 Core Capabilities

- 🧠 **AIP Prediction using AIPID's MAD-ML Model:**  
  Predict anti-inflammatory potential of peptide sequences using a Random Forest classifier trained on features extracted via Biopython and ProPy3, and datasets that were picked after motif analysis.

- 🧬 **Feature Extraction:**  
  Compute physiochemical properties of peptides including:
  - Molecular weight, pI, hydrophobicity, net charge, aromaticity
  - Aliphatic index, instability index
  - Amino acid composition (AAC)

- 📊 **Interactive Visualizations:**  
  Analyze AIP datasets using intuitive charts like:
  - Length distribution
  - Net charge distribution
  - Hydrophobicity vs pI
  - Amino acid frequency barplots

- 📚 **AIP Repository:**  
  Browse a curated table of AIPs from both natural and synthetic sources.  
  Filter by organism, review status (SwissProt/TrEMBL), or search by ID.

---

### ⚙️ Backend Technologies

- **Framework:** Streamlit  
- **Descriptors:** Biopython, ProPy3  
- **Model:** Scikit-learn (Random Forest)  
- **Visualization:** Altair  

---

### 📜 App Details

- **Version:** 1.0  
- **License:** Free for academic and non-commercial use  
- **Developed by:** *Ananya Anurag Anand/ Biochemistry & Bioinformatics Laboratory/ Indian Institute of Information Technology, Allahabad, Uttar Pradesh 211015, India. All rights reserved.*

---
Built with ❤️ for researchers, by researchers.
""")
