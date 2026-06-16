import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Arc Activity Tracker",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Arc Activity Tracker")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    try:

        response = requests.get(
            f"{API_URL}/wallets/{wallet}/summary"
        )

        data = response.json()

        # ==========================
        # TOP METRICS
        # ==========================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Balance",
                round(data["balance"], 4)
            )

        with col2:
            st.metric(
                "Score",
                data["score"]
            )

        with col3:
            st.metric(
                "Badge",
                data["badge"]
            )

        with col4:
            st.metric(
                "Protocols",
                data["protocol_count"]
            )

        st.divider()

        # ==========================
        # ACTIVITY
        # ==========================

        st.subheader("📊 Activity")

        activity = data["activity"]

        col5, col6, col7 = st.columns(3)

        with col5:
            st.metric(
                "Transactions",
                activity.get(
                    "transactions_count",
                    0
                )
            )

        with col6:
            st.metric(
                "Transfers",
                activity.get(
                    "token_transfers_count",
                    0
                )
            )

        with col7:
            st.metric(
                "Gas Usage",
                activity.get(
                    "gas_usage_count",
                    0
                )
            )

        st.divider()

        # ==========================
        # PROTOCOLS
        # ==========================

        st.subheader("🌐 Protocols Used")

        for protocol in data["protocols"]:

            st.success(protocol)

        timeline = requests.get(
            f"{API_URL}/wallets/{wallet}/timeline"
        ).json()

        st.divider()

        st.subheader("📜 Recent Activity")

        if len(timeline) == 0:

            st.info(
                "No recent activity found"
            )

        else:

            for item in timeline:

                st.success(
                    f"{item['protocol']} → {item['action']}"
                )

        # ==========================
        # RAW DATA
        # ==========================

        with st.expander(
            "Raw API Response"
        ):
            st.json(data)

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )