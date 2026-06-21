import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    try:

        response = requests.get(
            f"{API_URL}/wallets/{wallet}/summary"
        )

        response.raise_for_status()

        data = response.json()

        activity = data["activity"]

        # =====================================
        # ACTIVITY METRICS
        # =====================================

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

        st.subheader(
            "📊 Activity Analytics"
        )

        activity_df = pd.DataFrame(
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
            activity_df.set_index(
                "Metric"
            )
        )

        # =====================================
        # SCORE ANALYTICS
        # =====================================

        st.divider()

        st.subheader(
            "🏆 Wallet Score Analytics"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Score",
                data["score"]
            )

        with col2:

            st.metric(
                "Grade",
                data["grade"]
            )

        with col3:

            st.metric(
                "Risk",
                data["risk"]
            )

        with col4:

            st.metric(
                "Balance",
                round(
                    float(
                        data["balance"]
                    ),
                    4
                )
            )

        # =====================================
        # PROTOCOL ANALYTICS
        # =====================================

        st.divider()

        st.subheader(
            "🌐 Protocol Analytics"
        )

        protocols = data.get(
            "protocols",
            []
        )

        if len(protocols) == 0:

            st.warning(
                "No protocols detected."
            )

        else:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Protocols Used",
                    len(protocols)
                )

            with col2:

                st.metric(
                    "Protocol Count",
                    len(protocols)
                )

            for protocol in protocols:

                st.success(protocol)

        # =====================================
        # WALLET OVERVIEW
        # =====================================

        st.divider()

        st.subheader(
            "🚀 Wallet Overview"
        )

        overview_df = pd.DataFrame(
            {
                "Metric": [
                    "Protocols",
                    "Transactions",
                    "Transfers"
                ],
                "Value": [
                    len(protocols),
                    txs,
                    transfers
                ]
            }
        )

        # st.bar_chart(
        #     overview_df.set_index(
        #         "Metric"
        #     )
        # )
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Protocols",
                len(protocols)
            )

        with col2:
            st.metric(
                "Transactions",
                txs
            )

        with col3:
            st.metric(
                "Transfers",
                transfers
            )

        # =====================================
        # SUMMARY
        # =====================================

        st.divider()

        st.subheader(
            "📋 Summary"
        )

        st.info(
            f"""
            Grade: {data['grade']}

            Score: {data['score']}

            Risk Level: {data['risk']}

            Protocols Used: {len(protocols)}

            Transactions: {txs}

            Transfers: {transfers}
            """
        )

    # =====================================
    # HTTP ERRORS
    # =====================================

    except requests.exceptions.HTTPError:

        if response.status_code == 404:

            st.warning(
                "Wallet not found."
            )

        elif response.status_code == 400:

            st.warning(
                """
                ⚠️ No On-Chain Activity Found

                This wallet has no recorded activity on Arc Testnet.
                """
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    # =====================================
    # UNEXPECTED ERROR
    # =====================================

    except Exception as e:

        st.error(
            f"Unexpected Error: {e}"
        )