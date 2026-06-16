# backend/services/actions.py

from backend.services.parser import (
    parse_transaction
)

def detect_actions(txs):

    actions = []

    for tx in txs:

        parsed = parse_transaction(tx)

        actions.append(
            parsed["action"]
        )

    return actions


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