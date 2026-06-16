import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("📊 Dashboard")

try:

    leaderboard = requests.get(
        f"{API_URL}/wallets/leaderboard"
    ).json()

    if not leaderboard:

        st.warning(
            "No wallets found"
        )

        st.stop()

    df = pd.DataFrame(
        leaderboard
    )

    # =====================
    # Metrics
    # =====================

    total_wallets = len(df)

    top_score = df["score"].max()

    avg_score = round(
        df["score"].mean(),
        2
    )

    top_badge = (
        df.iloc[0]["badge"]
        if len(df) > 0
        else "-"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Wallets",
            total_wallets
        )

    with col2:
        st.metric(
            "Top Score",
            top_score
        )

    with col3:
        st.metric(
            "Average Score",
            avg_score
        )

    with col4:
        st.metric(
            "Top Badge",
            top_badge
        )

    st.divider()

    # =====================
    # Score Ranking
    # =====================

    st.subheader(
        "🏆 Score Ranking"
    )

    chart_df = df[
        [
            "wallet",
            "score"
        ]
    ]

    chart_df = chart_df.set_index(
        "wallet"
    )

    st.bar_chart(
        chart_df
    )

    st.divider()

    # =====================
    # Risk Distribution
    # =====================

    if "risk" in df.columns:

        st.subheader(
            "⚠️ Risk Distribution"
        )

        risk_df = (
            df["risk"]
            .value_counts()
        )

        st.bar_chart(
            risk_df
        )

except Exception as e:

    st.error(
        str(e)
    )