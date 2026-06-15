import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Arc Leaderboard")

response = requests.get(
    f"{API_URL}/wallets/leaderboard"
)

data = response.json()

if len(data) == 0:

    st.warning("No wallets found")

else:

    df = pd.DataFrame(data)

    df.index = df.index + 1

    df.index.name = "Rank"

    st.dataframe(
        df,
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🥇 Leader",
            data[0]["score"]
        )

    with col2:
        st.metric(
            "👑 Badge",
            data[0]["badge"]
        )

    with col3:
        st.metric(
            "📊 Wallets",
            len(data)
        )