import streamlit as st

st.set_page_config(
    page_title="Arc Activity Tracker",
    layout="wide"
)

st.title("Arc Activity Tracker")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:
    st.success(wallet)