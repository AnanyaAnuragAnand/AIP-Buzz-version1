import streamlit as st

st.title("🆘 Help & Usage Instructions")

st.markdown("""
### 👣 Step-by-Step: How to Use AIPID

1️⃣ **Paste your peptide sequence** using single-letter amino acid codes  
  (e.g. `KKLLDERVAKL`)  
2️⃣ **Click "Predict"** to classify the peptide using our trained model  
3️⃣ **Check the result** displayed on the screen  
4️⃣ **Use the sidebar** to navigate between app pages  

---

### 📖 Feature Guide

#### 🔍 AIP Prediction
- Go to the **"App"** page from the sidebar.
- Enter your peptide sequence (minimum 10 amino acids).
- Click on **"Predict"** to see if it's likely to be anti-inflammatory.

#### 🧬 AIP Feature Explorer
- Go to the **"AIP Features"** page to browse curated peptides.
- Use filters:
  - **Organism** (e.g., *Homo sapiens*, *Staphylococcus aureus*)
  - **SwissProt Status** (Reviewed or Unreviewed)
  - **Search by Peptide ID**
- Scroll through or download the filtered data.

---
### 👁️ **To view full peptide sequence** or to view full content of a cell
- Double click on the cell.

### 📋 Copy Cell Content (such as, sequences)
- Triple click and copy.

### 📊 Visual Tools for Statistics (On the 'AIP Features' Page)

- **Peptide Length Distribution**: Bar chart showing peptide size variation
- **Net Charge Distribution**: Distribution of charges at pH 7.0
- **Hydrophobicity vs pI**: Interactive scatter plot with SwissProt status
- **Amino Acid Frequency**: See the most common residues visually

---

### 💡 Tips & Troubleshooting

- Only use **valid amino acid single-letter codes** (e.g., `ACDEFGHIKLMNPQRSTVWY`)
- Sequence should be at least **10 amino acids** to ensure valid and meaningful feature extraction by ProtParam and ProPy3 descriptors.
- Avoid special characters or spaces in sequences

---

### 📥 Downloading Data
Click the **📥 "Download Filtered Table"** button on the AIP Features page to export a CSV of selected peptides.


---

### 📫 Need Help?
For bug reports, feedback, or collaboration queries, contact:

📧 `ananyaanurag12@gmail.com or rss2022501@iiita.ac.in`  
🧪 *Built with love, especially for the research community.*

---
""")
