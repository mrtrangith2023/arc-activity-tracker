from backend.services.arc_rpc import get_balance
from backend.services.arcscan import (
    get_counters,
    get_transactions
)
from backend.services.ecosystem import detect_protocols
from backend.services.score import (
    calculate_score,
    get_badge
)
from backend.services.grade import get_grade
from backend.services.risk import calculate_risk
from backend.services.wallet_intelligence import (
    build_wallet_insights
)

def build_wallet_summary(address: str):

    balance = get_balance(address)

    activity = get_counters(address)

    txs = get_transactions(address)

    protocols = detect_protocols(txs)

    score = calculate_score(
        activity,
        protocols
    )

    badge = get_badge(score)

    grade = get_grade(score)

    risk = calculate_risk(
        activity,
        protocols
    )

    insights = build_wallet_insights(
        activity,
        protocols,
        score,
        txs
    )

    return {
        "address": address,
        "balance": balance,
        "score": score,
        "badge": badge,
        "grade": grade,
        "risk": risk,
        "protocol_count": len(protocols),
        "protocols": protocols,
        "activity": activity,
        "insights": insights
    }