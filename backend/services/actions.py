def detect_action(protocol):

    mapping = {

        "PredictMarket": "Bet",

        "UnitFlow": "Swap",

        "XyloStablePool": "Deposit",

        "XyloVault": "Deposit"

    }

    return mapping.get(
        protocol,
        "Interaction"
    )