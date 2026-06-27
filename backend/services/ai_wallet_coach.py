def wallet_coach(summary):

    advice = []

    strengths = []

    weaknesses = []

    score = summary["score"]

    balance = summary["balance"]

    protocols = summary["protocols"]

    activity = summary["activity"]

    tx_count = int(
        activity.get(
            "transactions_count",
            0
        )
    )

    # --------------------
    # Strength
    # --------------------

    if balance > 1000:
        strengths.append("High Balance")

    if tx_count > 300:
        strengths.append("Active Wallet")

    if len(protocols) >= 3:
        strengths.append("Protocol Diversity")

    # --------------------
    # Weakness
    # --------------------

    if len(protocols) < 2:
        weaknesses.append("Very few protocols")

    if tx_count < 100:
        weaknesses.append("Low transaction history")

    # --------------------
    # Recommendation
    # --------------------

    if "UnitFlow" not in protocols:
        advice.append("Swap on UnitFlow")

    if "PredictMarket" not in protocols:
        advice.append("Use PredictMarket")

    if "XyloVault" not in protocols:
        advice.append("Deposit to XyloVault")

    if "XyloStablePool" not in protocols:
        advice.append("Provide Stable Liquidity")

    estimated = score + len(advice) * 40

    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": advice,

        "estimated_score": estimated

    }