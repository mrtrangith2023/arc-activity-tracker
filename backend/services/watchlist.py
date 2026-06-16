import json

WATCHLIST_FILE = "data/watchlist.json"


def load_watchlist():

    try:

        with open(
            WATCHLIST_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


def save_watchlist(wallets):

    with open(
        WATCHLIST_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            wallets,
            f,
            indent=4
        )


def add_wallet(address):

    wallets = load_watchlist()

    if address not in wallets:

        wallets.append(address)

        save_watchlist(wallets)

    return wallets


def remove_wallet(address):

    wallets = load_watchlist()

    if address in wallets:

        wallets.remove(address)

        save_watchlist(wallets)

    return wallets