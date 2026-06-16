# backend/services/parser.py

def parse_transaction(tx):

    raw_input = str(
        tx.get(
            "raw_input",
            ""
        )
    ).lower()

    tx_hash = tx.get("hash")

    # Swap
    if "swap" in raw_input:

        return {
            "hash": tx_hash,
            "action": "Swap"
        }

    # Deposit
    if "deposit" in raw_input:

        return {
            "hash": tx_hash,
            "action": "Deposit"
        }

    # Stake
    if "stake" in raw_input:

        return {
            "hash": tx_hash,
            "action": "Stake"
        }

    # Borrow
    if "borrow" in raw_input:

        return {
            "hash": tx_hash,
            "action": "Borrow"
        }

    # Bet
    if "bet" in raw_input:

        return {
            "hash": tx_hash,
            "action": "Bet"
        }

    return {
        "hash": tx_hash,
        "action": "Interaction"
    }