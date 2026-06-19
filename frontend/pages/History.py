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

        df["created_at"] = pd.to_datetime(
            df["created_at"]
        )

        df["time"] = df["created_at"].dt.strftime(
            "%H:%M:%S"
        )

        st.subheader(
            "📜 History Records"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # ==========================
        # GRADE TIMELINE
        # ==========================

        if "grade" in df.columns:

            st.subheader(
                "🎓 Grade Timeline"
            )

            grade_df = df[[

                "created_at",
                "grade"

            ]].copy()

            st.dataframe(
                grade_df,
                use_container_width=True
            )

        # ==========================
        # SCORE HISTORY
        # ==========================

        if "score" in df.columns:

            score_df = df[[
                "time",
                "score"
            ]].copy()

            score_df = score_df.rename(
                columns={
                    "time": "Time",
                    "score": "Score"
                }
            )

            st.subheader(
                "📊 Score History"
            )

            st.line_chart(
                score_df.set_index(
                    "Time"
                )
            )

        # ==========================
        # BALANCE HISTORY
        # ==========================

        if "balance" in df.columns:

            balance_df = df[[
                "time",
                "balance"
            ]].copy()

            balance_df = balance_df.rename(
                columns={
                    "time": "Time",
                    "balance": "Balance"
                }
            )

            st.subheader(
                "💰 Balance History"
            )

            st.line_chart(
                balance_df.set_index(
                    "Time"
                )
            )

        # ==========================
        # HISTORICAL ANALYTICS
        # ==========================

        st.subheader(
            "📊 Historical Analytics"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Snapshots",
                len(df)
            )

        with col2:

            st.metric(
                "Average Score",
                round(
                    df["score"].mean(),
                    2
                )
            )

        with col3:

            st.metric(
                "Average Balance",
                round(
                    df["balance"].mean(),
                    4
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

            # ==========================
            # BALANCE GROWTH
            # ==========================

            df = df.sort_values(
                by="created_at",
                ascending=True
            )

            first_balance = float(
                df.iloc[0]["balance"]
            )

            last_balance = float(
                df.iloc[-1]["balance"]
            )

            balance_growth = round(
                last_balance - first_balance,
                4
            )

            if first_balance > 0:

                balance_growth_percent = round(
                    (
                        balance_growth
                        /
                        first_balance
                    ) * 100,
                    4
                )

            else:

                balance_growth_percent = 0

            # ==========================
            # WALLET GROWTH METRICS
            # ==========================

            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:

                st.metric(
                    "Score Growth",
                    growth
                )

            with col2:

                st.metric(
                    "Score %",
                    f"{growth_percent}%"
                )

            with col3:

                st.metric(
                    "Balance Growth",
                    balance_growth
                )

            with col4:

                st.metric(
                    "Balance %",
                    f"{balance_growth_percent}%"
                )

            with col5:

                st.metric(
                    "Current Score",
                    last_score
                )

            with col6:

                st.metric(
                    "Highest Score",
                    df["score"].max()
                )

            col7, col8 = st.columns(2)

            with col7:
                st.metric(
                    "Current Grade",
                    df.iloc[-1]["grade"]
                )

            grade_rank = {
                "D":1,
                "C":2,
                "B":3,
                "A":4,
                "S":5
            }

            best_grade = max(
                df["grade"],
                key=lambda x: grade_rank.get(x, 0)
            )

            with col8:
                st.metric(
                    "Best Grade",
                    best_grade
                )

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )