import streamlit as st
import pandas as pd
import altair as alt
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from propy import PyPro
from collections import Counter

# Title
st.title("🧬 Anti-Inflammatory Peptides (AIPs)")
st.markdown("Explore the list of anti-inflammatory peptides and analyze their properties interactively.")

# Load Excel
@st.cache_data
def load_data():
    return pd.read_excel("protein_info_with_review_status.xlsx")

df = load_data()

# Calculate ProtParam + ProPy3 features
@st.cache_data
def compute_features(seq):
    result = {}
    try:
        analysed_seq = ProteinAnalysis(seq)
        result["Length"] = len(seq)
        result["MW"] = analysed_seq.molecular_weight()
        result["pI"] = analysed_seq.isoelectric_point()
        result["Aromaticity"] = analysed_seq.aromaticity()
        result["Instability"] = analysed_seq.instability_index()
        result["Hydrophobicity"] = analysed_seq.gravy()
        result["Net_Charge"] = analysed_seq.charge_at_pH(7.0)

        # Custom Aliphatic Index calculation
        aa_percent = analysed_seq.get_amino_acids_percent()
        ai = 100 * (aa_percent.get("A", 0) + aa_percent.get("V", 0) + aa_percent.get("I", 0) + aa_percent.get("L", 0))
        result["AliphaticIndex"] = ai

        # ProPy3 – Amino acid composition
        DesObject = PyPro.GetProDes(seq)
        aac = DesObject.GetAAComp()
        for aa, val in aac.items():
            result[f"AAC_{aa}"] = val

    except Exception as e:
        result["Length"] = len(seq)
        result["Error"] = str(e)

    return result

# Apply feature extraction
feature_dicts = df["Sequence"].apply(compute_features)
features_df = pd.json_normalize(feature_dicts)
df = pd.concat([df, features_df], axis=1)

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

organism_options = ["All"] + sorted(df["Source"].dropna().unique().tolist())
selected_org = st.sidebar.selectbox("Filter by Organism", organism_options)

review_options = ["All"] + sorted(df["Reviewed_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Filter by Review Status", review_options)

search_id = st.sidebar.text_input("Search by Peptide ID")

# Apply filters
filtered_df = df.copy()

if selected_org != "All":
    filtered_df = filtered_df[filtered_df["Source"] == selected_org]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Reviewed_Status"] == selected_status]

if search_id:
    filtered_df = filtered_df[filtered_df["ID"].str.contains(search_id, case=False, na=False)]

# Allow full sequence display
pd.set_option("display.max_colwidth", None)

# Display table
st.subheader(f"📋 Showing {len(filtered_df)} peptide(s)")
st.dataframe(filtered_df, use_container_width=True)

# Download filtered table
st.download_button(
    "📥 Download Filtered Table",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_AIP_table.csv",
    mime="text/csv"
)

# Length Distribution Plot
st.subheader("📊 Peptide Length Distribution")
length_chart = alt.Chart(filtered_df).mark_bar(color="teal").encode(
    x=alt.X("Length:Q", bin=alt.Bin(maxbins=30), title="Peptide Length"),
    y=alt.Y("count():Q", title="Count")
).properties(width=600, height=300)
st.altair_chart(length_chart, use_container_width=True)

# Net Charge Distribution
if "Net_Charge" in filtered_df.columns:
    st.subheader("⚡ Net Charge Distribution")
    charge_chart = alt.Chart(filtered_df).mark_bar(color="orange").encode(
        x=alt.X("Net_Charge:Q", bin=alt.Bin(maxbins=20), title="Net Charge (pH 7.0)"),
        y=alt.Y("count():Q", title="Count")
    ).properties(width=600, height=300)
    st.altair_chart(charge_chart, use_container_width=True)

# Hydrophobicity vs pI Scatter
if "Hydrophobicity" in filtered_df.columns and "pI" in filtered_df.columns:
    st.subheader("🧪 Hydrophobicity vs Isoelectric Point (pI)")
    scatter = alt.Chart(filtered_df).mark_circle(size=80).encode(
        x=alt.X("Hydrophobicity:Q", title="Hydrophobicity"),
        y=alt.Y("pI:Q", title="Isoelectric Point (pI)"),
        color=alt.Color("Reviewed_Status:N", title="SwissProt Review Status"),  # Legend label
        tooltip=["ID", "Hydrophobicity", "pI", "Name", "Reviewed_Status"]
    ).interactive().properties(width=600, height=400)

    st.altair_chart(scatter, use_container_width=True)

# Amino Acid Frequency Plot
aa_string = "".join(filtered_df["Sequence"].dropna())
aa_counts = dict(Counter(aa_string))
aa_df = pd.DataFrame(list(aa_counts.items()), columns=["AminoAcid", "Count"])

st.subheader("🔡 Amino Acid Frequency")
aa_bar = alt.Chart(aa_df).mark_bar().encode(
    x="AminoAcid:N",
    y="Count:Q"
    color="AminoAcid:N"
).properties(width=600)
st.altair_chart(aa_bar, use_container_width=True)

# Footer
st.caption("Built with ❤️ using Streamlit + Biopython + ProPy3")
