def calculate_score_v2(
    balance,
    tx_count,
    transfer_count
):

    score = 0

    # balance
    score += min(int(balance / 10), 50)

    # transactions
    score += min(tx_count, 500)

    # transfers
    score += min(transfer_count, 500)

    return score

def get_badge(score):

    if score >= 1000:
        return "Arc Legend"

    elif score >= 700:
        return "Power User"

    elif score >= 300:
        return "Explorer"

    else:
        return "Beginner"