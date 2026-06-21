# import streamlit as st
# import requests
# import pandas as pd

# API_URL = "http://127.0.0.1:8000"

# st.title(
#     "⭐ Watchlist Manager"
# )

# wallet = st.text_input(
#     "Wallet Address"
# )

# if st.button(
#     "Add Wallet"
# ):

#     requests.post(
#         f"{API_URL}/wallets/watchlist/{wallet}"
#     )

#     st.success(
#         "Wallet Added"
#     )

# wallets = requests.get(
#     f"{API_URL}/wallets/watchlist"
# ).json()

# st.write(
#     f"Total Wallets: {len(wallets)}"
# )

# df = pd.DataFrame(
#     {
#         "Wallet": wallets
#     }
# )

# st.dataframe(
#     df,
#     use_container_width=True
# )

# wallets = requests.get(
#     f"{API_URL}/wallets/watchlist"
# ).json()

# if wallets:

#     remove_wallet = st.selectbox(
#         "Select Wallet",
#         wallets
#     )

#     if st.button(
#         "Remove Wallet"
#     ):

#         requests.delete(
#             f"{API_URL}/wallets/watchlist/{remove_wallet}"
#         )

#         st.success(
#             "Wallet Removed"
#         )

#         st.rerun()

# else:

#     st.info(
#         "Watchlist is empty"
#     )
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"


def format_delta(delta):

    if delta > 0:

        return f"+{delta:g}"

    return f"{delta:g}"


def score_indicator(delta):

    if delta > 0:

        return "Increase"

    if delta < 0:

        return "Decrease"

    return "Unchanged"

st.title(
    "⭐ Watchlist Manager"
)

# ====================
# ADD WALLET
# ====================

wallet = st.text_input(
    "Wallet Address"
)

if st.button(
    "Add Wallet"
):

    r = requests.post(
        f"{API_URL}/wallets/watchlist/{wallet}"
    )

    if r.status_code == 200:

        st.success(
            "Wallet Added"
        )

        st.rerun()

    else:

        st.error(
            r.text
        )

# ====================
# LOAD WATCHLIST
# ====================

status_response = requests.get(
    f"{API_URL}/wallets/watchlist-status"
)

if status_response.status_code == 200:

    watchlist_status = status_response.json()

else:

    st.error(
        status_response.text
    )

    st.stop()

wallets = [
    item.get(
        "wallet"
    )
    for item in watchlist_status
]

st.write(
    f"Total Wallets: {len(wallets)}"
)

df = pd.DataFrame(watchlist_status)

if not df.empty:

    df["Indicator"] = df["delta"].apply(score_indicator)

    df["Delta"] = df["delta"].apply(format_delta)

    df = df.rename(
        columns={
            "wallet": "Wallet",
            "current_score": "Current Score",
            "previous_score": "Previous Score"
        }
    )

    display_columns = [
        "Wallet",
        "Current Score",
        "Previous Score",
        "Delta",
        "Indicator"
    ]

else:

    display_columns = []

st.dataframe(
    df[display_columns] if display_columns else df,
    use_container_width=True
)

# ====================
# REMOVE WALLET
# ====================

if wallets:

    remove_wallet = st.selectbox(
        "Select Wallet",
        wallets
    )

    if st.button(
        "Remove Wallet"
    ):

        requests.delete(
            f"{API_URL}/wallets/watchlist/{remove_wallet}"
        )

        st.success(
            "Wallet Removed"
        )

        st.rerun()

else:

    st.info(
        "Watchlist is empty"
    )
