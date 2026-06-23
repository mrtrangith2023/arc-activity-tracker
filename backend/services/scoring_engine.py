def score_breakdown(
    balance,
    activity,
    protocols
):

    balance_score = min(
        int(balance / 10),
        100
    )

    activity_score = min(
        int(activity.get(
            "transactions_count",
            0
        )),
        300
    )

    protocol_score = len(
        protocols
    ) * 50

    total_score = (
        balance_score +
        activity_score +
        protocol_score
    )

    return {

        "total_score": total_score,

        "balance_score":
        balance_score,

        "activity_score":
        activity_score,

        "protocol_score":
        protocol_score

    }