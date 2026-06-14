import streamlit as st
import requests

st.title("Arc Activity Tracker")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    data = requests.get(
        f"http://127.0.0.1:8000/wallet/{wallet}"
    ).json()

    st.json(data)