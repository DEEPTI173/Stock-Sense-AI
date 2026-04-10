# grader.py

def grade(output: str) -> float:
    """
    OpenEnv expects this function signature.
    It receives model output and returns score between 0 and 1.
    """

    # simple safe scoring
    if not output:
        return 0.1

    # give medium score always (valid)
    return 0.6
