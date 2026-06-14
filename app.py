import streamlit as st

st.set_page_config(
    page_title="Arc Activity Tracker",
    layout="wide"
)

st.title("Arc Activity Tracker")

wallet = st.text_input(
    "Enter Wallet Address"
)

if wallet:
    st.success(f"Tracking: {wallet}")

    st.metric("Transactions", "0")
    st.metric("Arc Score", "0")