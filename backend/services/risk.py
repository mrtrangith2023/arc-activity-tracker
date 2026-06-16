def calculate_risk(
    activity,
    protocols
):
    risk = 0

    if int(
        activity["transactions_count"]
    ) < 20:
        risk += 50

    if len(protocols) == 0:
        risk += 30

    if risk >= 70:
        return "High"

    if risk >= 30:
        return "Medium"

    return "Low"