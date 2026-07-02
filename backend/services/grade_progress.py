GRADE_TABLE = [
    ("D", 0),
    ("C", 150),
    ("B", 400),
    ("A", 700),
    ("S", 1000)
]


def get_grade_progress(score):

    current = "D"
    next_grade = "C"

    current_min = 0
    next_min = 150

    for i in range(len(GRADE_TABLE)-1):

        grade, minimum = GRADE_TABLE[i]
        n_grade, n_minimum = GRADE_TABLE[i+1]

        if minimum <= score < n_minimum:

            current = grade
            next_grade = n_grade

            current_min = minimum
            next_min = n_minimum

            break

    if score >= 1000:

        return {

            "current_grade":"S",

            "next_grade":"MAX",

            "progress":100,

            "need":0,

            "current_score":score,

            "target_score":1000

        }

    progress = (

        score-current_min

    )/(next_min-current_min)

    return {

        "current_grade":current,

        "next_grade":next_grade,

        "progress":round(progress*100,1),

        "need":next_min-score,

        "current_score":score,

        "target_score":next_min

    }