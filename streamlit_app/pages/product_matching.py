import streamlit as st
import pandas as pd
from db_utils import fetch_products

st.title("Product Matching Across Stores")
st.info("This page will compare products with similar names across multiple stores.")

# Example: load all stores
pointm = fetch_products("pointm")
fatales = fetch_products("fatales")
beautystore = fetch_products("beautystore")

# Combine into one DataFrame
all_df = pd.concat([pointm, fatales, beautystore], ignore_index=True)

st.write("Matching logic will be implemented here.")
st.dataframe(all_df.head(20))
