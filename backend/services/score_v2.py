def calculate_score(activity, protocols):

    txs = int(
        activity.get(
            "transactions_count",
            0
        )
    )

    transfers = int(
        activity.get(
            "token_transfers_count",
            0
        )
    )

    protocol_count = len(protocols)

    score = (
        txs // 10
        + transfers // 20
        + protocol_count * 100
    )

    return score


def get_badge(score):

    if score >= 500:
        return "Legend"

    elif score >= 300:
        return "Master"

    elif score >= 150:
        return "Explorer"

    return "Newbie"