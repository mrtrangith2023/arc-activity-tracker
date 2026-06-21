import pandas as pd
import requests
import streamlit as st

from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout


API_URL = "http://127.0.0.1:8000"


def is_valid_wallet(address):
    return address.startswith("0x") and len(address) == 42


def short_wallet(wallet):
    wallet = str(wallet)
    return f"{wallet[:6]}...{wallet[-4:]}"


def number(value, default=0):
    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def fetch_summary(wallet):
    response = requests.get(
        f"{API_URL}/wallets/{wallet}/summary",
        timeout=20
    )
    response.raise_for_status()
    return response.json()


def winner_label(value_a, value_b, higher_is_better=True):
    if value_a == value_b:
        return "Tie"

    if higher_is_better:
        return "Wallet A" if value_a > value_b else "Wallet B"

    return "Wallet A" if value_a < value_b else "Wallet B"


def risk_score(risk):
    return {
        "low": 1,
        "medium": 2,
        "high": 3
    }.get(
        str(risk).lower(),
        0
    )


st.set_page_config(
    page_title="Wallet Comparison",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Wallet Comparison")

col1, col2 = st.columns(2)

with col1:
    wallet_a = st.text_input(
        "Wallet A",
        placeholder="0x..."
    ).strip()

with col2:
    wallet_b = st.text_input(
        "Wallet B",
        placeholder="0x..."
    ).strip()

if not wallet_a or not wallet_b:
    st.info("Enter two Arc wallet addresses to compare score, activity, protocols, and risk.")
    st.stop()

if wallet_a.lower() == wallet_b.lower():
    st.warning("Choose two different wallets for a meaningful comparison.")
    st.stop()

if not is_valid_wallet(wallet_a):
    st.error("Wallet A is invalid. Use a 42-character 0x address.")
    st.stop()

if not is_valid_wallet(wallet_b):
    st.error("Wallet B is invalid. Use a 42-character 0x address.")
    st.stop()

try:
    with st.spinner("Loading wallet summaries..."):
        data_a = fetch_summary(wallet_a)
        data_b = fetch_summary(wallet_b)

except Timeout:
    st.error("Arc API timed out. Try again in a moment.")
    st.stop()

except ConnectionError:
    st.error("Unable to connect to the Arc API. Check that the backend is running.")
    st.stop()

except HTTPError as error:
    status_code = error.response.status_code if error.response is not None else None

    if status_code == 400:
        st.warning("One of these wallets has no Arc Testnet activity yet.")

    else:
        st.error(f"API error: {error}")

    st.stop()

except RequestException as error:
    st.error(f"Request failed: {error}")
    st.stop()

activity_a = data_a.get("activity", {})
activity_b = data_b.get("activity", {})
protocols_a = sorted(data_a.get("protocols", []))
protocols_b = sorted(data_b.get("protocols", []))

score_a = int(number(data_a.get("score")))
score_b = int(number(data_b.get("score")))
balance_a = number(data_a.get("balance"))
balance_b = number(data_b.get("balance"))
tx_a = int(number(activity_a.get("transactions_count")))
tx_b = int(number(activity_b.get("transactions_count")))
transfers_a = int(number(activity_a.get("token_transfers_count")))
transfers_b = int(number(activity_b.get("token_transfers_count")))
risk_a = risk_score(data_a.get("risk"))
risk_b = risk_score(data_b.get("risk"))

if tx_a == 0 or tx_b == 0:
    st.warning("One of these wallets has no recorded on-chain activity.")
    st.stop()

wallet_a_label = short_wallet(wallet_a)
wallet_b_label = short_wallet(wallet_b)

summary_df = pd.DataFrame(
    [
        {
            "Metric": "Score",
            "Wallet A": score_a,
            "Wallet B": score_b,
            "Difference": score_a - score_b,
            "Leader": winner_label(score_a, score_b)
        },
        {
            "Metric": "Balance",
            "Wallet A": round(balance_a, 4),
            "Wallet B": round(balance_b, 4),
            "Difference": round(balance_a - balance_b, 4),
            "Leader": winner_label(balance_a, balance_b)
        },
        {
            "Metric": "Transactions",
            "Wallet A": tx_a,
            "Wallet B": tx_b,
            "Difference": tx_a - tx_b,
            "Leader": winner_label(tx_a, tx_b)
        },
        {
            "Metric": "Transfers",
            "Wallet A": transfers_a,
            "Wallet B": transfers_b,
            "Difference": transfers_a - transfers_b,
            "Leader": winner_label(transfers_a, transfers_b)
        },
        {
            "Metric": "Protocols",
            "Wallet A": len(protocols_a),
            "Wallet B": len(protocols_b),
            "Difference": len(protocols_a) - len(protocols_b),
            "Leader": winner_label(len(protocols_a), len(protocols_b))
        },
        {
            "Metric": "Risk",
            "Wallet A": data_a.get("risk", "Unknown"),
            "Wallet B": data_b.get("risk", "Unknown"),
            "Difference": risk_a - risk_b,
            "Leader": winner_label(risk_a, risk_b, higher_is_better=False)
        }
    ]
)

score_diff = abs(score_a - score_b)
score_winner = winner_label(score_a, score_b)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Wallet A", wallet_a_label)

with col2:
    st.metric("Wallet B", wallet_b_label)

with col3:
    st.metric("Score leader", score_winner)

with col4:
    st.metric("Score gap", score_diff)

st.divider()

st.subheader("Comparison Summary")
st.dataframe(
    summary_df,
    hide_index=True,
    use_container_width=True
)

chart_df = pd.DataFrame(
    [
        {
            "Wallet": "Wallet A",
            "Score": score_a,
            "Balance": balance_a,
            "Transactions": tx_a,
            "Transfers": transfers_a,
            "Protocols": len(protocols_a)
        },
        {
            "Wallet": "Wallet B",
            "Score": score_b,
            "Balance": balance_b,
            "Transactions": tx_b,
            "Transfers": transfers_b,
            "Protocols": len(protocols_b)
        }
    ]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Score")
    st.bar_chart(
        chart_df.set_index("Wallet")["Score"]
    )

with col2:
    st.subheader("Balance")
    st.bar_chart(
        chart_df.set_index("Wallet")["Balance"]
    )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Activity")
    activity_df = chart_df[
        [
            "Wallet",
            "Transactions",
            "Transfers"
        ]
    ].set_index("Wallet")
    st.bar_chart(activity_df)

with col2:
    st.subheader("Protocol Count")
    st.bar_chart(
        chart_df.set_index("Wallet")["Protocols"]
    )

st.divider()

st.subheader("Protocol Overlap")

shared_protocols = sorted(set(protocols_a) & set(protocols_b))
unique_a = sorted(set(protocols_a) - set(protocols_b))
unique_b = sorted(set(protocols_b) - set(protocols_a))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Shared", len(shared_protocols))

with col2:
    st.metric("Only Wallet A", len(unique_a))

with col3:
    st.metric("Only Wallet B", len(unique_b))

protocol_df = pd.DataFrame(
    {
        "Shared": pd.Series(shared_protocols),
        "Only Wallet A": pd.Series(unique_a),
        "Only Wallet B": pd.Series(unique_b)
    }
)

if protocol_df.empty:
    st.info("Neither wallet has supported protocol interactions yet.")

else:
    st.dataframe(
        protocol_df.fillna(""),
        hide_index=True,
        use_container_width=True
    )

st.divider()

st.subheader("Profile")

profile_df = pd.DataFrame(
    [
        {
            "Wallet": "Wallet A",
            "Address": wallet_a_label,
            "Grade": data_a.get("grade", "-"),
            "Badge": data_a.get("badge", "-"),
            "Risk": data_a.get("risk", "Unknown")
        },
        {
            "Wallet": "Wallet B",
            "Address": wallet_b_label,
            "Grade": data_b.get("grade", "-"),
            "Badge": data_b.get("badge", "-"),
            "Risk": data_b.get("risk", "Unknown")
        }
    ]
)

st.dataframe(
    profile_df,
    hide_index=True,
    use_container_width=True
)
