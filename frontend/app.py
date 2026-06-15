# import streamlit as st
# import requests

# st.title("Arc Activity Tracker")

# wallet = st.text_input(
#     "Wallet Address"
# )

# if wallet:

#     data = requests.get(
#         f"http://127.0.0.1:8000/wallet/{wallet}"
#     ).json()

#     st.json(data)
import streamlit as st
import requests

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
            f"http://127.0.0.1:8000/wallets/{wallet}/summary"
        )

        data = response.json()

        col1, col2, col3 = st.columns(3)

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

        st.subheader("Wallet")

        st.code(
            data["address"]
        )

        st.metric(
            "Protocols",
            len(data["protocols"])
        )

        with st.expander("Protocols Used"):

            for protocol in data["protocols"]:

                st.success(protocol)

        st.json(data)

    except Exception as e:

        st.error(str(e))