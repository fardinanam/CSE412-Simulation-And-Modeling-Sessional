import pmmlcg
import math

def expon(mean : float) -> float:
    return -mean * math.log(pmmlcg.lcgrand(1))

def uniform(a : float, b : float) -> float:
    """
    Return a uniform random value between a and b inclusive.
    """
    return a + (b - a) * pmmlcg.lcgrand(1)

def random_integer(prob_distrib : list) -> int:
    """
    Return a random integer between 1 and num_values inclusive, with the
    probability of each value i (i = 1, ..., num_values) being equal to
    prob_distrib[i - 1].
    """
    u = pmmlcg.lcgrand(1)

    i = 1
    while u > prob_distrib[i - 1] and i < len(prob_distrib):
        i += 1

    return i