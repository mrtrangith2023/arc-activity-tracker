import pandas as pd
import requests
import streamlit as st

from requests.exceptions import RequestException


API_URL = "http://127.0.0.1:8000"


def short_wallet(wallet):
    wallet = str(wallet)

    if len(wallet) <= 14 or "..." in wallet:
        return wallet

    return f"{wallet[:6]}...{wallet[-4:]}"


def fetch_leaderboard():
    response = requests.get(
        f"{API_URL}/wallets/leaderboard",
        timeout=20
    )
    response.raise_for_status()
    return response.json()


st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Arc Leaderboard")

try:
    data = fetch_leaderboard()

except RequestException as error:
    st.error(f"Unable to load leaderboard: {error}")
    st.stop()

if not data:
    st.warning("No ranked wallets found. Add active wallets to the watchlist first.")
    st.stop()

df = pd.DataFrame(data)

if "score" not in df.columns:
    st.warning("Leaderboard data is missing score values.")
    st.dataframe(df, use_container_width=True)
    st.stop()

df = df.sort_values(
    by="score",
    ascending=False
).reset_index(drop=True)

df.insert(0, "Rank", df.index + 1)
df["Wallet"] = df["wallet"].apply(short_wallet)

top_wallet = df.iloc[0]
avg_score = round(df["score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Top wallet", top_wallet["Wallet"])

with col2:
    st.metric("Top score", top_wallet["score"])

with col3:
    st.metric("Average score", avg_score)

with col4:
    st.metric("Ranked wallets", len(df))

st.divider()

chart_df = df.head(10).copy()
chart_df["Label"] = chart_df["Rank"].astype(str) + ". " + chart_df["Wallet"]

st.subheader("Top Scores")
st.bar_chart(
    chart_df.set_index("Label")["score"]
)

st.subheader("Leaderboard")

display_columns = [
    column
    for column in [
        "Rank",
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
            max_value=max(int(df["score"].max()), 1),
            format="%d"
        ),
        "balance": st.column_config.NumberColumn(
            "Balance",
            format="%.4f"
        ),
        "protocols": st.column_config.NumberColumn(
            "Protocols",
            format="%d"
        )
    }
)
