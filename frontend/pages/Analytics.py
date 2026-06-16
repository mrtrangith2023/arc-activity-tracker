import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("📈 Analytics")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    try:

        data = requests.get(
            f"{API_URL}/wallets/{wallet}/summary"
        ).json()

        activity = data["activity"]

        txs = int(
            activity.get(
                "transactions_count",
                0
            )
        )

        transfers = int(
            activity.get(
                "token_transfers_count",
                0
            )
        )

        gas = round(
            int(
                activity.get(
                    "gas_usage_count",
                    0
                )
            ) / 1_000_000,
            2
        )
        df = pd.DataFrame(
            {
                "Metric": [
                    "Transactions",
                    "Transfers",
                    "Gas Usage"
                ],
                "Value": [
                    txs,
                    transfers,
                    gas
                ]
            }
        )

        st.bar_chart(
            df.set_index("Metric")
        )

    except Exception as e:

        st.error(str(e))