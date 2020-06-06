import random
import numpy as np
from copy import copy
from utils import tools
from random import randint
from itertools import combinations


class NeighborOperator:

    def __init__(self):
        self.operators = {1: self.random_swap,
                          2: self.random_insert,
                          3: self.random_reversing}
        pass


    def random_operator(self, _solution, verbose=False):
        operators = list(self.operators)
        # p = [p / sum(operators) for p in operators]
        p = None
        rand_choice = np.random.choice(operators, p=p)
        random_oper = self.operators[rand_choice]
        return random_oper(_solution, verbose=verbose)

    @staticmethod
    def random_swap(_solution, patience = 100, verbose=False):
        if verbose:
            print('random swap')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(range(1, sol_len-1), 2)
            if i != j and solution[i] != 0 and solution[j] != 0:
                solution[i], solution[j] = copy(solution[j]), copy(solution[i])
                break
            patience -= 1
        return solution

    @staticmethod
    def random_insert(_solution, patience = 100, verbose=False):
        if verbose:
            print('random insertion')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(range(1, sol_len-1), 2)
            if i != j and solution[i] != 0 and solution[j] != 0:
                i, j = copy(min(i, j)), copy(max(i, j))
                solution[:i] = _solution[:i]
                solution[i]  = _solution[j]
                solution[i+1:j+1] = _solution[i:j]
                solution[j+1:]    = _solution[j+1:]
                break
            patience -= 1
        return solution

    @staticmethod
    def random_reversing(_solution, patience = 100, verbose=False):
        if verbose:
            print('random reversing a subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(range(1, sol_len-1), 2)
            if i != j:
                i, j = copy(min(i, j)), copy(max(i, j))
                solution[i:j] = solution[i:j][::-1]
                break
            patience -= 1
        return solution
