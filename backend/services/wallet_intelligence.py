def build_wallet_insights(
    activity,
    protocols,
    score,
    txs=None
):
    txs = txs or []

    tx_count = int(
        activity.get(
            "transactions_count",
            0
        )
    )

    protocol_count = len(protocols)
    protocol_set = set(protocols)
    activity_flags = _detect_activity_flags(txs)

    strengths = _build_strengths(
        protocol_count,
        score,
        tx_count
    )

    weaknesses = _build_weaknesses(
        protocol_set,
        activity_flags,
        protocol_count,
        tx_count,
        score
    )

    recommendations = _build_recommendations(
        protocol_set,
        activity_flags,
        protocol_count,
        tx_count
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }


def _build_strengths(
    protocol_count,
    score,
    tx_count
):
    strengths = []

    if protocol_count >= 3:
        strengths.append(
            "Active across multiple Arc protocols"
        )
    elif protocol_count > 0:
        strengths.append(
            "Has started using Arc ecosystem protocols"
        )

    if score >= 500:
        strengths.append(
            "High wallet score shows strong ecosystem activity"
        )
    elif score >= 150:
        strengths.append(
            "Wallet score shows meaningful on-chain progress"
        )

    if tx_count >= 100:
        strengths.append(
            "High transaction count indicates consistent usage"
        )
    elif tx_count >= 20:
        strengths.append(
            "Healthy transaction history"
        )

    if not strengths:
        strengths.append(
            "Wallet is ready to build an activity profile"
        )

    return strengths


def _build_weaknesses(
    protocol_set,
    activity_flags,
    protocol_count,
    tx_count,
    score
):
    weaknesses = []

    if tx_count == 0:
        weaknesses.append(
            "No transaction activity detected"
        )
    elif tx_count < 20:
        weaknesses.append(
            "Low transaction count limits wallet history"
        )

    if protocol_count == 0:
        weaknesses.append(
            "No Arc protocol activity detected"
        )
    elif protocol_count < 3:
        weaknesses.append(
            "Limited protocol diversity"
        )

    if "UnitFlow" not in protocol_set:
        weaknesses.append(
            "Missing UnitFlow activity"
        )
    elif not activity_flags["unitflow_swap"]:
        weaknesses.append(
            "Missing UnitFlow swap activity"
        )

    if not activity_flags["liquidity"]:
        weaknesses.append(
            "Missing liquidity activity"
        )

    if "PredictMarket" not in protocol_set:
        weaknesses.append(
            "Missing PredictMarket activity"
        )

    if score < 150:
        weaknesses.append(
            "Wallet score is still early-stage"
        )

    return weaknesses


def _build_recommendations(
    protocol_set,
    activity_flags,
    protocol_count,
    tx_count
):
    recommendations = []

    if "UnitFlow" not in protocol_set or not activity_flags["unitflow_swap"]:
        recommendations.append(
            "Make a UnitFlow swap"
        )

    if not activity_flags["liquidity"]:
        recommendations.append(
            "Provide liquidity on UnitFlow"
        )

    if "PredictMarket" not in protocol_set:
        recommendations.append(
            "Use PredictMarket"
        )

    if protocol_count < 3 or tx_count < 20:
        recommendations.append(
            "Add more Arc ecosystem interactions"
        )

    if not recommendations:
        recommendations.append(
            "Keep interacting across the Arc ecosystem to maintain momentum"
        )

    return recommendations


def _detect_activity_flags(txs):
    unitflow_swap = False
    liquidity = False

    for tx in txs:
        to_data = tx.get(
            "to",
            {}
        )

        protocol_name = str(
            to_data.get(
                "name",
                ""
            )
        )

        raw_input = str(
            tx.get(
                "raw_input",
                ""
            )
        ).lower()

        is_unitflow = "UnitFlow" in protocol_name

        if is_unitflow and "swap" in raw_input:
            unitflow_swap = True

        if (
            "liquidity" in raw_input
            or "deposit" in raw_input
            or "XyloStablePool" in protocol_name
            or "XyloVault" in protocol_name
        ):
            liquidity = True

    return {
        "unitflow_swap": unitflow_swap,
        "liquidity": liquidity
    }
