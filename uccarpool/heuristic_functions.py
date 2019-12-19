"""
THis file contains all functions from the heuristic formula.
All functions return 0.0 to 1.0, being 0.0 not a match and 1.0 full match
"""


def function_smoker(smokerA, smokerB):
    """ """
    return 1.0 if smokerA == smokerB else 0.0


def function_sex(sexA, sexB):
    """ """
    return 1.0 if sexA == sexB else 0.0


def function_eloquence_level(eloquence_levelA, eloquence_levelB):
    """
    Calculates the difference between eloquence levels.
    The farther apart they are, less match.
    Full match occurs when they are the same level.
    """

    difference_eloquence_level = abs(eloquence_levelA - eloquence_levelB)

    if difference_eloquence_level == 0:
        """They are the same level"""
        return 1.0
    elif difference_eloquence_level == 1:
        return 0.5
    else:
        return 0


def function_music_taste(music_tasteA, music_tasteB):
    """Count how many matches occur in music taste proportionally to the number of similiar genres"""
    # TODO
    return 1.0
