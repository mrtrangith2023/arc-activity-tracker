import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Wallet Comparison",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Wallet Comparison")

wallet1 = st.text_input(
    "Wallet A"
)

wallet2 = st.text_input(
    "Wallet B"
)

if wallet1 and wallet2:

    try:

        # ==========================
        # FETCH DATA
        # ==========================

        response1 = requests.get(
            f"{API_URL}/wallets/{wallet1}/summary"
        )

        response1.raise_for_status()

        data1 = response1.json()

        response2 = requests.get(
            f"{API_URL}/wallets/{wallet2}/summary"
        )

        response2.raise_for_status()

        data2 = response2.json()

        # ==========================
        # SAFE DEFAULTS
        # ==========================

        activity1 = data1.get(
            "activity",
            {}
        )

        activity2 = data2.get(
            "activity",
            {}
        )

        protocols1 = data1.get(
            "protocols",
            []
        )

        protocols2 = data2.get(
            "protocols",
            []
        )

        # ==========================
        # SHARED PROTOCOLS
        # ==========================

        common_protocols = sorted(

            list(

                set(protocols1)

                &

                set(protocols2)

            )

        )

        # ==========================
        # MAIN TABLE
        # ==========================

        df = pd.DataFrame({

            "Metric": [

                "Balance",
                "Score",
                "Risk",
                "Grade",
                "Badge",
                "Protocols",
                "Transactions"

            ],

            "Wallet A": [

                round(
                    float(
                        data1.get(
                            "balance",
                            0
                        )
                    ),
                    4
                ),

                data1.get(
                    "score",
                    0
                ),

                data1.get(
                    "risk",
                    "-"
                ),

                data1.get(
                    "grade",
                    "-"
                ),

                data1.get(
                    "badge",
                    "-"
                ),

                data1.get(
                    "protocol_count",
                    0
                ),

                activity1.get(
                    "transactions_count",
                    0
                )

            ],

            "Wallet B": [

                round(
                    float(
                        data2.get(
                            "balance",
                            0
                        )
                    ),
                    4
                ),

                data2.get(
                    "score",
                    0
                ),

                data2.get(
                    "risk",
                    "-"
                ),

                data2.get(
                    "grade",
                    "-"
                ),

                data2.get(
                    "badge",
                    "-"
                ),

                data2.get(
                    "protocol_count",
                    0
                ),

                activity2.get(
                    "transactions_count",
                    0
                )

            ]

        })

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==========================
        # SCORE CHART
        # ==========================

        score_df = pd.DataFrame({

            "Wallet": [
                "Wallet A",
                "Wallet B"
            ],

            "Score": [
                data1.get("score", 0),
                data2.get("score", 0)
            ]

        })

        st.subheader(
            "📊 Score Comparison"
        )

        st.bar_chart(
            score_df.set_index(
                "Wallet"
            )
        )

        # ==========================
        # WINNER
        # ==========================

        st.subheader(
            "🏆 Winner"
        )

        score1 = data1.get(
            "score",
            0
        )

        score2 = data2.get(
            "score",
            0
        )

        if score1 > score2:

            st.success(
                f"Wallet A wins with score {score1}"
            )

        elif score2 > score1:

            st.success(
                f"Wallet B wins with score {score2}"
            )

        else:

            st.info(
                "Tie"
            )

        # ==========================
        # SCORE DIFFERENCE
        # ==========================

        st.subheader(
            "🎯 Comparison Result"
        )

        score_diff = abs(
            score1 - score2
        )

        st.info(
            f"Score Difference: {score_diff}"
        )

        # ==========================
        # BALANCE COMPARISON
        # ==========================

        balance1 = float(
            data1.get(
                "balance",
                0
            )
        )

        balance2 = float(
            data2.get(
                "balance",
                0
            )
        )

        balance_df = pd.DataFrame({

            "Wallet": [
                "Wallet A",
                "Wallet B"
            ],

            "Balance": [
                balance1,
                balance2
            ]

        })

        st.subheader(
            "💰 Balance Comparison"
        )

        st.bar_chart(
            balance_df.set_index(
                "Wallet"
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Wallet A Balance",
                round(
                    balance1,
                    4
                )
            )

        with col2:

            st.metric(
                "Wallet B Balance",
                round(
                    balance2,
                    4
                )
            )

        with col3:

            st.metric(
                "Balance Difference",
                round(
                    abs(
                        balance1
                        -
                        balance2
                    ),
                    4
                )
            )

        # ==========================
        # ACTIVITY COMPARISON
        # ==========================

        activity_df = pd.DataFrame({

            "Metric": [

                "Transactions",
                "Transfers"

            ],

            "Wallet A": [

                activity1.get(
                    "transactions_count",
                    0
                ),

                activity1.get(
                    "token_transfers_count",
                    0
                )

            ],

            "Wallet B": [

                activity2.get(
                    "transactions_count",
                    0
                ),

                activity2.get(
                    "token_transfers_count",
                    0
                )

            ]

        })

        st.subheader(
            "📈 Activity Comparison"
        )

        st.dataframe(
            activity_df,
            use_container_width=True
        )

        # ==========================
        # GRADE COMPARISON
        # ==========================

        st.subheader(
            "🎓 Grade Comparison"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Wallet A Grade",
                data1.get(
                    "grade",
                    "-"
                )
            )

        with col2:

            st.metric(
                "Wallet B Grade",
                data2.get(
                    "grade",
                    "-"
                )
            )

        # ==========================
        # PROTOCOL SUMMARY
        # ==========================

        st.subheader(
            "🌐 Protocol Comparison"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Wallet A Protocols",
                len(protocols1)
            )

        with col2:

            st.metric(
                "Wallet B Protocols",
                len(protocols2)
            )

        with col3:

            st.metric(
                "Shared",
                len(common_protocols)
            )

        # ==========================
        # PROTOCOL LIST
        # ==========================

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "Wallet A"
            )

            for protocol in protocols1:

                st.success(
                    protocol
                )

        with col2:

            st.write(
                "Wallet B"
            )

            for protocol in protocols2:

                st.success(
                    protocol
                )

        # ==========================
        # SHARED PROTOCOLS
        # ==========================

        st.subheader(
            "🤝 Shared Protocols"
        )

        if common_protocols:

            for protocol in common_protocols:

                st.info(
                    protocol
                )

        else:

            st.warning(
                "No shared protocols"
            )

        # ==========================
        # RISK COMPARISON
        # ==========================
        
        risk_map = {

            "low": 1,
            "medium": 2,
            "high": 3

        }

        risk_a = risk_map.get(
            data1["risk"],
            0
        )

        risk_b = risk_map.get(
            data2["risk"],
            0
        )

        risk_df = pd.DataFrame({

            "Wallet": [
                "Wallet A",
                "Wallet B"
            ],

            "Risk": [

                risk_map.get(
                    str(
                        data1.get(
                            "risk",
                            ""
                        )
                    ).lower(),
                    0
                ),

                risk_map.get(
                    str(
                        data2.get(
                            "risk",
                            ""
                        )
                    ).lower(),
                    0
                )

            ]

        })

        st.subheader(
            "⚠️ Risk Comparison"
        )

        # ==========================
        # NEW
        # ==========================
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Wallet A Risk",
                data1["risk"]
            )

        with col2:
            st.metric(
                "Wallet B Risk",
                data2["risk"]
            )

        with col3:

            if risk_a < risk_b:

                st.success(
                    "🟢 Wallet A Safer"
                )

            elif risk_b < risk_a:

                st.success(
                    "🟢 Wallet B Safer"
                )

            else:

                st.info(
                    "🤝 Same Risk Level"
                )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )