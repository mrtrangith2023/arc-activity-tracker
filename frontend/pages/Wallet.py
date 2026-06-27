import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("👛 Wallet")

wallet = st.text_input(
    "Wallet Address"
)

if wallet:

    # =========================
    # SUMMARY
    # =========================

    summary = requests.get(
        f"{API_URL}/wallets/{wallet}/summary"
    ).json()

    st.subheader(
    "📋 Wallet Overview"
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Score",
            summary["score"]
        )

    with col2:
        st.metric(
            "Grade",
            summary["grade"]
        )

    with col3:
        st.metric(
            "Risk",
            summary["risk"]
        )

    with col4:
        st.metric(
            "Protocols",
            summary["protocol_count"]
        )

    with col5:
        st.metric(
            "Balance",
            round(
                summary["balance"],
                2
            )
        )

    st.subheader(
        "🎯 Wallet Score"
    )

    st.progress(
        min(
            summary["score"] / 500,
            1.0
        )
    )

    if summary["grade"] == "S":
        st.success("🏆 Elite Wallet")

    elif summary["grade"] == "A":
        st.success("🥇 Excellent Wallet")

    elif summary["grade"] == "B":
        st.info("🥈 Good Wallet")

    elif summary["grade"] == "C":
        st.warning("🥉 Average Wallet")

    else:
        st.error("⚠️ Beginner Wallet")

    # =========================
    # SCORE BREAKDOWN
    # =========================

    breakdown = requests.get(
        f"{API_URL}/wallets/{wallet}/score-breakdown"
    ).json()

    st.divider()

    st.subheader(
        "📊 Score Breakdown"
    )

    score_df = pd.DataFrame(
        {
            "Category": [
                "Balance",
                "Activity",
                "Protocols"
            ],
            "Score": [
                breakdown["balance_score"],
                breakdown["activity_score"],
                breakdown["protocol_score"]
            ]
        }
    )

    st.bar_chart(
        score_df.set_index(
            "Category"
        )
    )

    st.divider()

    st.subheader(
        "🌐 Protocols"
    )

    protocols = summary[
        "protocols"
    ]

    if protocols:

        for protocol in protocols:

            st.success(
                protocol
            )

    else:

        st.warning(
            "No protocols detected"
        )

    if summary["risk"] == "Low":

        st.success(
            "🟢 Low Risk Wallet"
        )

    elif summary["risk"] == "Medium":

        st.warning(
            "🟡 Medium Risk Wallet"
        )

    else:

        st.error(
            "🔴 High Risk Wallet"
        )

    st.divider()

    coach = requests.get(
        f"{API_URL}/wallets/{wallet}/coach"
    ).json()


    st.subheader("🤖 AI Wallet Coach")

    st.markdown("### ✅ Strengths")

    if coach["strengths"]:

        for item in coach["strengths"]:

            st.success(item)

    else:

        st.info("No strengths detected yet.")


    st.markdown("### ⚠ Weaknesses")

    if coach["weaknesses"]:

        for item in coach["weaknesses"]:

            st.warning(item)

    else:

        st.success("No weaknesses.")


    st.markdown("### 🚀 Recommendations")

    for item in coach["recommendations"]:

        st.info(item)


    st.metric(
        "Estimated Future Score",
        coach["estimated_score"]
    )