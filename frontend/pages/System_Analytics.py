import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="System Analytics",
    page_icon="📊",
    layout="wide"
)

st.title(
    "📊 System Analytics"
)

# ==================================
# OVERVIEW
# ==================================

overview = requests.get(
    f"{API_URL}/wallets/analytics"
).json()

st.subheader(
    "📈 Ecosystem Overview"
)

health = requests.get(
    f"{API_URL}/wallets/health-score"
).json()

# st.metric(
#     "Ecosystem Health",
#     f"{health['health_score']}%"
# )
health_score = health[
    "health_score"
]

health_score = float(
    health["health_score"]
)
if health_score >= 70:

    st.success(
        "🟢 Ecosystem Status: Healthy"
    )

elif health_score >= 40:

    st.warning(
        "🟡 Ecosystem Status: Growing"
    )

else:

    st.error(
        "🔴 Ecosystem Status: Early Stage"
    )

st.metric(
    "Ecosystem Health",
    f"{health_score}%"
)

st.progress(
    min(
        health_score / 100,
        1.0
    )
)

# ==================================
# ECOSYSTEM TREND
# ==================================

st.divider()

st.subheader(
    "📈 Ecosystem Trend"
)

trend = requests.get(
    f"{API_URL}/wallets/ecosystem-trend"
).json()

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Wallet Growth",
        trend["wallet_growth"]
    )

with col2:

    st.metric(
        "Snapshot Growth",
        trend["snapshot_growth"]
    )

with col3:

    st.metric(
        "Average Score",
        trend["avg_score_growth"]
    )

# ==================================
# GRADE DISTRIBUTION
# ==================================

st.divider()

st.subheader(
    "🎓 Grade Distribution"
)

grades = requests.get(
    f"{API_URL}/wallets/grade-distribution"
).json()

grade_df = pd.DataFrame(
    [
        [k, v]
        for k, v in grades.items()
        if v > 0
    ],
    columns=[
        "Grade",
        "Wallets"
    ]
)

st.bar_chart(
    grade_df.set_index(
        "Grade"
    )
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Wallets",
        overview["wallets"]
    )

with col2:

    st.metric(
        "Snapshots",
        overview["snapshots"]
    )

with col3:

    st.metric(
        "Average Score",
        overview["avg_score"]
    )

with col4:

    st.metric(
        "Average Balance",
        overview["avg_balance"]
    )

# ==================================
# TOP PROTOCOLS
# ==================================
st.divider()

st.subheader(
    "🌐 Top Protocols"
)

protocols = requests.get(
    f"{API_URL}/wallets/top-protocols"
).json()

protocol_df = pd.DataFrame(
    {
        "Protocol": protocols,
        "Usage": [1] * len(protocols)
    }
)

st.bar_chart(
    protocol_df.set_index(
        "Protocol"
    )
)

# ==================================
# TOP WALLETS
# ==================================

# st.divider()

# st.subheader(
#     "🏆 Top Wallets"
# )

# top_wallets = requests.get(
#     f"{API_URL}/wallets/top-wallets"
# ).json()

# df = pd.DataFrame(
#     top_wallets
# )

# if len(df) > 0:

#     st.dataframe(
#         df,
#         use_container_width=True
#     )

# ==================================
# WALLETS RANKING
# ==================================
st.divider()

st.subheader(
    "🏆 Wallet Ranking"
)

ranking = requests.get(
    f"{API_URL}/wallets/ranking"
).json()

ranking_df = pd.DataFrame(
    ranking
)

# ranking_df = ranking_df[
#     [
#         "wallet",
#         "score",
#         "grade",
#         "balance"
#     ]
# ]
ranking_df["wallet"] = ranking_df[
    "wallet"
].apply(
    lambda x:
    f"{x[:8]}...{x[-6:]}"
)

st.dataframe(
    ranking_df,
    use_container_width=True
)

# ==================================
# PROTOCOL RANKING
# ==================================

st.divider()

st.subheader(
    "🏆 Protocol Ranking"
)

protocol_rank = requests.get(
    f"{API_URL}/wallets/protocol-ranking"
).json()

if protocol_rank:

    protocol_rank_df = pd.DataFrame(
        protocol_rank
    )

    protocol_rank_df = protocol_rank_df.sort_values(
        by="users",
        ascending=False
    )

    st.dataframe(
        protocol_rank_df,
        use_container_width=True
    )

else:

    st.info(
        "No protocol ranking data available."
    )

# ==================================
# RISK DISTRIBUTION
# ==================================

st.divider()

st.subheader(
    "⚠️ Risk Distribution"
)

risk = requests.get(
    f"{API_URL}/wallets/risk-distribution"
).json()

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
    risk_df.set_index(
        "Risk"
    )
)