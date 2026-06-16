def get_grade(score):

    if score >= 800:
        return "S"

    if score >= 600:
        return "A"

    if score >= 400:
        return "B"

    if score >= 200:
        return "C"

    return "D"