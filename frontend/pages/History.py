import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Wallet History",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Wallet History")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    try:

        response = requests.get(
            f"{API_URL}/wallets/{wallet}/history"
        )

        response.raise_for_status()

        history = response.json()

        if len(history) == 0:

            st.warning(
                "No history found."
            )

            st.stop()

        df = pd.DataFrame(history)

        st.subheader(
            "📜 History Records"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==========================
        # SCORE HISTORY
        # ==========================

        if "score" in df.columns:

            score_df = df[[
                "created_at",
                "score"
            ]].copy()

            score_df = score_df.rename(
                columns={
                    "created_at": "Date",
                    "score": "Score"
                }
            )

            st.subheader(
                "📊 Score History"
            )

            st.line_chart(
                score_df.set_index(
                    "Date"
                )
            )

        # ==========================
        # BALANCE HISTORY
        # ==========================

        if "balance" in df.columns:

            balance_df = df[[
                "created_at",
                "balance"
            ]].copy()

            balance_df = balance_df.rename(
                columns={
                    "created_at": "Date",
                    "balance": "Balance"
                }
            )

            st.subheader(
                "💰 Balance History"
            )

            st.line_chart(
                balance_df.set_index(
                    "Date"
                )
            )

        # ==========================
        # GROWTH ANALYSIS
        # ==========================

        if len(df) >= 2:

            first_score = float(
                df.iloc[0]["score"]
            )

            last_score = float(
                df.iloc[-1]["score"]
            )

            growth = round(
                last_score -
                first_score,
                2
            )

            if first_score > 0:

                growth_percent = round(
                    (
                        growth
                        /
                        first_score
                    )
                    * 100,
                    2
                )

            else:

                growth_percent = 0

            st.subheader(
                "🚀 Wallet Growth"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Score Growth",
                    growth
                )

            with col2:

                st.metric(
                    "Growth %",
                    f"{growth_percent}%"
                )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )