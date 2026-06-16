from backend.services.arcscan import (
    get_transactions
)

from backend.services.ecosystem import (
    detect_protocols
)

from backend.services.actions import (
    detect_action
)


def build_timeline(address):

    txs = get_transactions(address)

    protocols = detect_protocols(txs)

    timeline = []

    for protocol in protocols:

        timeline.append(
            {
                "protocol": protocol,
                "action": detect_action(protocol)
            }
        )

    return timeline