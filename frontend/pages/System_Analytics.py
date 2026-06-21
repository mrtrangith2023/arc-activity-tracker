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


def protocols_count(value):
    if value is None:
        return 0

    if isinstance(value, list):
        return len(value)

    return len(
        [
            item
            for item in str(value).split(",")
            if item.strip()
        ]
    )


def latest_wallet_ranking(rows):
    df = pd.DataFrame(rows)

    if df.empty or "score" not in df.columns:
        return pd.DataFrame()

    df = df.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    df.insert(0, "Rank", df.index + 1)

    if "wallet" in df.columns:
        df["Wallet"] = df["wallet"].apply(short_wallet)

    if "protocols" in df.columns:
        df["Protocol Count"] = df["protocols"].apply(protocols_count)

    return df


def protocol_ranking_table(rows):
    df = pd.DataFrame(rows)

    if df.empty or "protocol" not in df.columns:
        return pd.DataFrame()

    if "users" not in df.columns:
        df["users"] = 0

    df = df.sort_values(
        by="users",
        ascending=False
    ).reset_index(drop=True)

    total_users = max(int(df["users"].sum()), 1)
    df.insert(0, "Rank", df.index + 1)
    df["Share"] = (df["users"] / total_users * 100).round(1)

    return df


st.set_page_config(
    page_title="System Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 System Analytics")

overview = get_json(
    "/wallets/analytics",
    {
        "wallets": 0,
        "snapshots": 0,
        "avg_score": 0,
        "avg_balance": 0
    }
)

health = get_json(
    "/wallets/health-score",
    {
        "health_score": 0
    }
)

health_score = float(
    health.get(
        "health_score",
        0
    )
)

st.subheader("Ecosystem Overview")

if health_score >= 70:
    st.success("Ecosystem status: Healthy")

elif health_score >= 40:
    st.warning("Ecosystem status: Growing")

else:
    st.error("Ecosystem status: Early stage")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Health", f"{health_score}%")

with col2:
    st.metric("Wallets", overview.get("wallets", 0))

with col3:
    st.metric("Snapshots", overview.get("snapshots", 0))

with col4:
    st.metric("Average score", overview.get("avg_score", 0))

with col5:
    st.metric("Average balance", overview.get("avg_balance", 0))

st.progress(
    min(
        health_score / 100,
        1.0
    )
)

st.divider()

st.subheader("Ecosystem Trend")

trend = get_json(
    "/wallets/ecosystem-trend",
    {
        "wallet_growth": 0,
        "snapshot_growth": 0,
        "avg_score_growth": 0
    }
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Wallet growth", trend.get("wallet_growth", 0))

with col2:
    st.metric("Snapshot growth", trend.get("snapshot_growth", 0))

with col3:
    st.metric("Average score", trend.get("avg_score_growth", 0))

st.divider()

st.subheader("Grade Distribution")

grades = get_json(
    "/wallets/grade-distribution",
    {}
)

grade_df = pd.DataFrame(
    [
        {
            "Grade": grade,
            "Wallets": count
        }
        for grade, count in grades.items()
        if count > 0
    ]
)

if grade_df.empty:
    st.info("No grade data available yet.")

else:
    st.bar_chart(
        grade_df.set_index("Grade")["Wallets"]
    )

st.divider()

st.subheader("Leaderboard")

ranking = get_json(
    "/wallets/ranking",
    []
)

ranking_df = latest_wallet_ranking(ranking)

if ranking_df.empty:
    st.info("No wallet ranking data available yet.")

else:
    top_wallet = ranking_df.iloc[0]
    avg_score = round(ranking_df["score"].mean(), 2)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Top wallet", top_wallet.get("Wallet", "-"))

    with col2:
        st.metric("Top score", top_wallet.get("score", 0))

    with col3:
        st.metric("Average ranked score", avg_score)

    chart_df = ranking_df.head(10).copy()

    if "Wallet" not in chart_df.columns:
        chart_df["Wallet"] = chart_df["Rank"].astype(str)

    chart_df["Label"] = (
        chart_df["Rank"].astype(str)
        + ". "
        + chart_df["Wallet"]
    )

    st.bar_chart(
        chart_df.set_index("Label")["score"]
    )

    display_columns = [
        column
        for column in [
            "Rank",
            "Wallet",
            "score",
            "grade",
            "balance",
            "Protocol Count",
            "created_at"
        ]
        if column in ranking_df.columns
    ]

    st.dataframe(
        ranking_df[display_columns],
        hide_index=True,
        use_container_width=True,
        column_config={
            "score": st.column_config.ProgressColumn(
                "Score",
                min_value=0,
                max_value=max(int(ranking_df["score"].max()), 1),
                format="%d"
            ),
            "balance": st.column_config.NumberColumn(
                "Balance",
                format="%.4f"
            )
        }
    )

st.divider()

st.subheader("Protocol Ranking")

protocol_rank = get_json(
    "/wallets/protocol-ranking",
    []
)

protocol_rank_df = protocol_ranking_table(protocol_rank)

if protocol_rank_df.empty:
    st.info("No protocol ranking data available yet.")

else:
    total_protocols = len(protocol_rank_df)
    total_mentions = int(protocol_rank_df["users"].sum())
    top_protocol = protocol_rank_df.iloc[0]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tracked protocols", total_protocols)

    with col2:
        st.metric("Protocol mentions", total_mentions)

    with col3:
        st.metric("Most used", top_protocol["protocol"])

    chart_df = protocol_rank_df.head(10).copy()
    chart_df["Label"] = (
        chart_df["Rank"].astype(str)
        + ". "
        + chart_df["protocol"].astype(str)
    )

    st.bar_chart(
        chart_df.set_index("Label")["users"]
    )

    st.dataframe(
        protocol_rank_df[
            [
                "Rank",
                "protocol",
                "users",
                "Share"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        column_config={
            "users": st.column_config.NumberColumn(
                "Users",
                format="%d"
            ),
            "Share": st.column_config.ProgressColumn(
                "Share",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            )
        }
    )

st.divider()

st.subheader("Supported Protocols")

protocols = get_json(
    "/wallets/top-protocols",
    []
)

if protocols:
    protocol_df = pd.DataFrame(
        {
            "Protocol": protocols
        }
    )

    st.dataframe(
        protocol_df,
        hide_index=True,
        use_container_width=True
    )

else:
    st.info("No supported protocols configured.")

st.divider()

st.subheader("Risk Distribution")

risk = get_json(
    "/wallets/risk-distribution",
    {}
)

risk_df = pd.DataFrame(
    {
        "Risk": [
            "Low",
            "Medium",
            "High"
        ],
        "Wallets": [
            risk.get("Low", 0),
            risk.get("Medium", 0),
            risk.get("High", 0)
        ]
    }
)

st.bar_chart(
    risk_df.set_index("Risk")["Wallets"]
)