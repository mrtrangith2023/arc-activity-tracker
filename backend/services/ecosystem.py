def detect_protocols(items):

    protocols = set()

    for tx in items:

        to_data = tx.get("to", {})

        name = to_data.get("name")

        if not name:
            continue

        if "XyloVault" in name:
            protocols.add("XyloVault")

        elif "XyloStablePool" in name:
            protocols.add("XyloStablePool")

        elif "UnitFlowLendingPool" in name:
            protocols.add("UnitFlow")

        elif "PredictMarket" in name:
            protocols.add("PredictMarket")

    return sorted(list(protocols))