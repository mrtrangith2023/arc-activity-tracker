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
    leader = data[0]

    wallet_short = (
        leader["wallet"][:6]
        + "..."
        + leader["wallet"][-4:]
    )

    st.success(
        f"👑 Top Wallet: {wallet_short}"
    )

    df = pd.DataFrame(data)

    df.index = df.index + 1

    df.index.name = "Rank"

    st.dataframe(
        df,
        use_container_width=True
    )

    chart_df = df.copy()

    chart_df["wallet_short"] = chart_df["wallet"].apply(
        lambda x: x[:6] + "..." + x[-4:]
    )

    st.subheader(
        "📈 Score Ranking"
    )

    st.bar_chart(
        chart_df.set_index(
            "wallet_short"
        )["score"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🥇 Top Score",
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