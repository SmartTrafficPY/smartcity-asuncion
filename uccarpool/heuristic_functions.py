"""
THis file contains all functions from the heuristic formula.
All functions return 0.0 to 1.0, being 0.0 not a match and 1.0 full match
"""
from ucusers.models import UcarpoolingProfile


def function_smoker(smokerA, smokerB):
    """ """
    return 1.0 if smokerA == smokerB else 0.0


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

    """If either has no preference in music, then they are full compatible"""
    if (UcarpoolingProfile.MUSIC_GENRE_NO_PREFERENCE in music_tasteA
       or UcarpoolingProfile.MUSIC_GENRE_NO_PREFERENCE in music_tasteB):
        return 1.0

    """If both prefer silence, then they are full compatible"""
    if (UcarpoolingProfile.MUSIC_GENRE_SILENCE in music_tasteA
       and UcarpoolingProfile.MUSIC_GENRE_SILENCE in music_tasteB):
        return 1.0

    """If one prefer silence and the other not, then they are not compatible"""
    if ((UcarpoolingProfile.MUSIC_GENRE_SILENCE in music_tasteA
       and UcarpoolingProfile.MUSIC_GENRE_SILENCE not in music_tasteB)
       or
       (UcarpoolingProfile.MUSIC_GENRE_SILENCE not in music_tasteA
       and UcarpoolingProfile.MUSIC_GENRE_SILENCE in music_tasteB)):
        return 0

    """
    Calculate the percentage of genres is common.
    Calculate the similarity among lists finding the distinct elements
    and also common elements and computing it’s quotient.
    """
    res = len(set(music_tasteA) & set(music_tasteB)) / float(len(set(music_tasteA) | set(music_tasteB)))

    return res


def function_sex(sexA, sexB):
    """ """
    return 1.0 if sexA == sexB else 0
