import streamlit as st
from db_utils import fetch_products

st.title("Fatales Promotions")
df = fetch_products("fatales")

for _, row in df.iterrows():
    st.markdown(f"### {row['brand']} - {row['name']}")
    cols = st.columns([1,2])
    with cols[0]:
        if row['image']:
            st.image(row['image'], width=150)
        else:
            st.text("No image")
    with cols[1]:
        st.markdown(f"**Price:** {row['price']} DT")
        if row['old_price']:
            st.markdown(f"**Old Price:** {row['old_price']} DT")
        if row['discount']:
            st.markdown(f"**Discount:** {row['discount']} %")
        st.markdown(f"[Product Link]({row['link']})")
    st.markdown("---")
