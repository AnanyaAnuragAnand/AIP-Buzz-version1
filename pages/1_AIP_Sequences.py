import streamlit as st
import pandas as pd

st.title("🧬 Anti-Inflammatory Peptides (AIPs)")

# Load Excel
try:
    df = pd.read_excel("protein_info_with_review_status.xlsx")
    st.success("Excel file loaded successfully!")

    st.dataframe(df, use_container_width=True)

    # Optional download
    st.download_button(
        label="📥 Download AIP Table",
        data=df.to_csv(index=False),
        file_name="AIP_sequences.csv",
        mime="text/csv"
    )
except Exception as e:
    st.error(f"Failed to load Excel file: {e}")
