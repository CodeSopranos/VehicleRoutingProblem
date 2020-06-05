import random
import numpy as np
from copy import copy
from utils import tools
from random import randint
from itertools import combinations


class NeighborOperator:

    def __init__(self):
        operators =
            {0: self.random_swap}
        pass

    @staticmethod
    def random_swap(_solution, patience = 100):
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(np.arange(1, sol_len-1), 2)
            if i != j and solution[i] != 0 and solution[j] != 0:
                solution[i],
                solution[j] = copy(solution[j]),
                              copy(solution[i])
                break
            patience -= 1
        return solution
