import streamlit as st
import pandas as pd
import altair as alt

# Title
st.title("🧬 Anti-Inflammatory Peptides (AIPs)")
st.markdown("Explore the list of anti-inflammatory peptides and analyze their properties interactively.")

# Load Excel
@st.cache_data
def load_data():
    return pd.read_excel("protein_info_with_review_status.xlsx")

df = load_data()

# Calculate sequence length and net charge (optional)
df["Length"] = df["Sequence"].apply(len)

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Organism filter
organism_options = ["All"] + sorted(df["Source"].dropna().unique().tolist())
selected_org = st.sidebar.selectbox("Filter by Organism", organism_options)

# Review status filter
review_options = ["All"] + sorted(df["Reviewed_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Filter by Review Status", review_options)

# Peptide ID search
search_id = st.sidebar.text_input("Search by Peptide ID")

# Apply filters
filtered_df = df.copy()

if selected_org != "All":
    filtered_df = filtered_df[filtered_df["Source"] == selected_org]

if selected_status != "All":
    filtered_df = filtered_df[filtered_df["Reviewed_Status"] == selected_status]

if search_id:
    filtered_df = filtered_df[filtered_df["ID"].str.contains(search_id, case=False, na=False)]

# Display filtered table
st.subheader(f"📋 Showing {len(filtered_df)} peptide(s)")
st.dataframe(filtered_df, use_container_width=True)

# Download filtered table
st.download_button(
    "📥 Download Filtered Table",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_AIP_table.csv",
    mime="text/csv"
)

# Plot: Length Distribution
st.subheader("📊 Peptide Length Distribution")
length_chart = alt.Chart(filtered_df).mark_bar(color="teal").encode(
    x=alt.X("Length:Q", bin=alt.Bin(maxbins=30), title="Peptide Length"),
    y=alt.Y("count():Q", title="Count")
).properties(width=600, height=300)

st.altair_chart(length_chart, use_container_width=True)

# Plot: Charge Distribution (if present)
if "Net_Charge" in df.columns:
    st.subheader("⚡ Charge Distribution")
    charge_chart = alt.Chart(filtered_df).mark_bar(color="orange").encode(
        x=alt.X("Net_Charge:Q", bin=alt.Bin(maxbins=20), title="Net Charge"),
        y=alt.Y("count():Q", title="Count")
    ).properties(width=600, height=300)
    st.altair_chart(charge_chart, use_container_width=True)
else:
    st.info("🔋 No 'Net_Charge' column found. Add it from PortParam or ProPy3 to enable charge distribution plot.")

# Footer note
st.caption("Built with ❤️ using Streamlit. Data from anti-inflammatory peptide prediction pipeline.")
