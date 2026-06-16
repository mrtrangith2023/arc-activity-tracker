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

wallets = requests.get(
    f"{API_URL}/wallets/watchlist"
).json()

st.write(
    f"Total Wallets: {len(wallets)}"
)

df = pd.DataFrame(
    wallets,
    columns=["Wallet"]
)

st.dataframe(
    df,
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