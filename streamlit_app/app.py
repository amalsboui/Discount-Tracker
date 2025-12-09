import streamlit as st

st.set_page_config(page_title="Promotions Dashboard", layout="wide")
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", [
    "Point M",
    "Fatales",
    "BeautyStore",
    "Product Matching"
])

if page == "Point M":
    import pages.pointm
elif page == "Fatales":
    import pages.fatales
elif page == "BeautyStore":
    import pages.beautystore
elif page == "Product Matching":
    import pages.product_matching
