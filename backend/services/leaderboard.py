import json

from backend.services.arc_rpc import get_balance

from backend.services.arcscan import (
    get_counters,
    get_transactions
)

from backend.services.ecosystem import (
    detect_protocols
)

from backend.services.score import (
    calculate_score,
    get_badge
)


def get_leaderboard():

    with open(
        "data/watchlist.json",
        "r",
        encoding="utf-8"
    ) as f:

        wallets = json.load(f)

    results = []

    for wallet in wallets:

        try:

            balance = get_balance(wallet)

            activity = get_counters(wallet)

            txs = get_transactions(wallet)

            protocols = detect_protocols(txs)

            score = calculate_score(
                activity,
                protocols
            )

            badge = get_badge(score)

            if score > 0:

                results.append(
                    {
                        "wallet":
                            wallet[:6]
                            + "..."
                            + wallet[-4:],

                        "score": score,

                        "badge": badge,

                        "protocols":
                            len(protocols),

                        "balance": round(
                            balance,
                            4
                        )
                    }
                )

        except Exception as e:

            results.append(
                {
                    "wallet":
                        wallet[:6]
                        + "..."
                        + wallet[-4:],

                    "error": str(e)
                }
            )
    # Lọc ví có điểm > 0
    results = [
        r for r in results
        if r["score"] > 0
    ]

    # Loại 1
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # Loại 2
    # results.sort(
    #     key=lambda x: x.get(
    #         "score",
    #         -1
    #     ),
    #     reverse=True
    # )

    return results