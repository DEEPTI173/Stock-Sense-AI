# grader.py

def grade_easy(output: str) -> float:
    if not output:
        return 0.2
    return 0.4   # easy score


def grade_medium(output: str) -> float:
    if not output:
        return 0.3
    return 0.6   # medium score


def grade_hard(output: str) -> float:
    if not output:
        return 0.4
    return 0.8   # hard score
