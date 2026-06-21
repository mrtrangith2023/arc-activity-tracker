from collections import Counter


def get_protocol_ranking(rows):

    protocols = []

    for row in rows:

        if not row.protocols:

            continue

        items = row.protocols.split(",")

        protocols.extend(items)

    counter = Counter(protocols)

    result = []

    for protocol, count in counter.items():

        result.append(
            {
                "protocol": protocol,
                "users": count
            }
        )

    result.sort(
        key=lambda x: x["users"],
        reverse=True
    )

    return result