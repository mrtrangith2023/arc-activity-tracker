import pandas as pd
import requests
import streamlit as st

from requests.exceptions import RequestException


API_URL = "http://127.0.0.1:8000"


def get_json(path, fallback):
    try:
        response = requests.get(
            f"{API_URL}{path}",
            timeout=20
        )
        response.raise_for_status()
        return response.json()

    except RequestException as error:
        st.warning(f"Could not load {path}: {error}")
        return fallback


def short_wallet(wallet):
    wallet = str(wallet)

    if len(wallet) <= 14 or "..." in wallet:
        return wallet

    return f"{wallet[:6]}...{wallet[-4:]}"


def activity_level(avg_score):
    if avg_score >= 500:
        return "High"

    if avg_score >= 150:
        return "Medium"

    return "Low"


def sybil_risk_label(risk_distribution):
    total = sum(risk_distribution.values())

    if total == 0:
        return "Unknown"

    high_share = risk_distribution.get(
        "High",
        0
    ) / total

    medium_share = risk_distribution.get(
        "Medium",
        0
    ) / total

    if high_share >= 0.4:
        return "High"

    if high_share + medium_share >= 0.5:
        return "Medium"

    return "Low"


def safe_numeric(series):
    return pd.to_numeric(
        series,
        errors="coerce"
    ).fillna(0)


st.set_page_config(
    page_title="Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("Dashboard")

leaderboard = get_json(
    "/wallets/leaderboard",
    []
)

health = get_json(
    "/wallets/health-score",
    {
        "health_score": 0
    }
)

risk_distribution = get_json(
    "/wallets/risk-distribution",
    {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }
)

df = pd.DataFrame(leaderboard)

if df.empty:
    st.warning("No wallets found")
    st.stop()

if "score" not in df.columns:
    st.warning("Dashboard data is missing score values.")
    st.dataframe(df, use_container_width=True)
    st.stop()

df["score"] = safe_numeric(df["score"])

if "protocols" in df.columns:
    df["protocols"] = safe_numeric(df["protocols"])

else:
    df["protocols"] = 0

df = df.sort_values(
    by="score",
    ascending=False
).reset_index(drop=True)

df["Wallet"] = df["wallet"].apply(short_wallet)

wallet_health = round(
    float(
        health.get(
            "health_score",
            0
        )
    ),
    2
)

avg_score = round(
    float(df["score"].mean()),
    2
)

activity = activity_level(avg_score)
sybil_risk = sybil_risk_label(risk_distribution)
protocol_count = int(df["protocols"].sum())
avg_protocols = round(
    float(df["protocols"].mean()),
    2
)

st.subheader("Score Cards")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Wallet Health",
        f"{wallet_health}%"
    )
    st.progress(
        min(
            wallet_health / 100,
            1.0
        )
    )

with col2:
    st.metric(
        "Sybil Risk",
        sybil_risk
    )

with col3:
    st.metric(
        "Activity Level",
        activity,
        f"Avg score {avg_score:g}"
    )

with col4:
    st.metric(
        "Protocol Count",
        protocol_count,
        f"Avg {avg_protocols:g} per wallet"
    )

st.divider()

st.subheader("Wallet Scores")

score_chart = df[
    [
        "Wallet",
        "score"
    ]
].copy()

st.bar_chart(
    score_chart.set_index("Wallet")
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Sybil Risk Distribution")

    risk_df = pd.DataFrame(
        [
            {
                "Risk": risk,
                "Wallets": count
            }
            for risk, count in risk_distribution.items()
        ]
    )

    st.bar_chart(
        risk_df.set_index("Risk")
    )

with col2:
    st.subheader("Protocol Usage")

    protocol_chart = df[
        [
            "Wallet",
            "protocols"
        ]
    ].copy()

    st.bar_chart(
        protocol_chart.set_index("Wallet")
    )

st.divider()

st.subheader("Wallet Overview")

display_columns = [
    column
    for column in [
        "Wallet",
        "score",
        "badge",
        "protocols",
        "balance"
    ]
    if column in df.columns
]

st.dataframe(
    df[display_columns],
    hide_index=True,
    use_container_width=True,
    column_config={
        "score": st.column_config.ProgressColumn(
            "Score",
            min_value=0,
            max_value=max(
                int(df["score"].max()),
                1
            ),
            format="%d"
        ),
        "protocols": st.column_config.NumberColumn(
            "Protocols",
            format="%d"
        ),
        "balance": st.column_config.NumberColumn(
            "Balance",
            format="%.4f"
        )
    }
)
