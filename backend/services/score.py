def calculate_score(balance):

    score = 0

    if balance > 10:
        score += 10

    if balance > 50:
        score += 20

    if balance > 100:
        score += 30

    return score

def get_badge(score):

    if score >= 100:
        return "Power User"

    if score >= 50:
        return "Explorer"

    return "Beginner"