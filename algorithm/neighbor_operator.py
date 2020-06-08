import random
import numpy as np
from copy import copy
from utils import tools
from random import randint
from utils import common
from itertools import combinations


class NeighborOperator:

    def __init__(self):
        self.operators = {
                          1: self.random_swap,
                          2: self.random_swap_sub,
                          # 3: self.random_insert,
                          # 4: self.random_insert_sub,
                          5: self.random_reversing,
                          6: self.random_swap_sub_reverse,
                          7: self.random_insert_sub_reverse
                          }
        pass


    def random_operator(self, _solution, patience=10, verbose=False):
        operators = list(self.operators)
        # p = [p / sum(operators) for p in operators]
        p = None
        rand_choice = np.random.choice(operators, p=p)
        random_oper = self.operators[rand_choice]
        return random_oper(_solution, patience=patience, verbose=verbose)

    @staticmethod
    def random_swap(_solution, patience=10, verbose=False):
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
    def random_swap_sub(_solution, patience=10, verbose=False):
        if verbose:
            print('random swap of subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            k = random.choice(range(2, 7))
            i, j = random.sample(range(1, sol_len-k-1), 2)
            if abs(i-j)>k and solution[i] != 0 and solution[j] != 0:
                if verbose:
                    print('Swap: ', solution[i:i+k], solution[j:j+k])
                solution[i:i+k], solution[j:j+k] = copy(solution[j:j+k]), copy(solution[i:i+k])

                # there shouldn`t be several depots in a row for example [0, 0,.. ]
                if common.check_depots_sanity(solution):
                    break
            patience -= 1

        return solution

    @staticmethod
    def random_insert(_solution, patience=10, verbose=False):
        if verbose:
            print('random insertion')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(range(1, sol_len-1), 2)
            if i != j and solution[i] != 0 and solution[j] != 0:
                i, j = copy(min(i, j)), copy(max(i, j))
                if solution[j+1] != 0 or solution[j-1]!=0:
                    solution[:i] = _solution[:i]
                    solution[i]  = _solution[j]
                    solution[i+1:j+1] = _solution[i:j]
                    solution[j+1:]    = _solution[j+1:]
                    break
            patience -= 1

        return solution

    @staticmethod
    def random_insert_sub(_solution, patience=10, verbose=False):
        if verbose:
            print('random insertion of subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            k = random.choice(range(2, 7))
            i, j = random.sample(range(1, sol_len-k-1), 2)
            if abs(i-j) <= k:
                continue
            i, j = copy(min(i, j)), copy(max(i, j))
            if verbose:
                print('Insert: ',_solution[j:j+k], 'to', i, i+k)
            solution[:i] = _solution[:i]
            solution[i:i+k]  = _solution[j:j+k]
            solution[i+k:j+k] = _solution[i:j]
            solution[j+k:]  = _solution[j+k:]

            # there shouldn`t be several depots in a row for example [0, 0,.. ]
            if common.check_depots_sanity(solution):
                break
            patience -= 1

        return solution

    @staticmethod
    def random_reversing(_solution, patience=10, verbose=False):
        if verbose:
            print('random reversing a subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            i, j = random.sample(range(1, sol_len-1), 2)
            if i != j:
                i, j = copy(min(i, j)), copy(max(i, j))
                if  solution[j+1] != 0  and solution[i-1] != 0:
                    solution[i:j] = solution[i:j][::-1]
                    break
            patience -= 1
        return solution

    @staticmethod
    def random_swap_sub_reverse(_solution, patience=10, verbose=False):
        if verbose:
            print('random swap of reversed subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            k = random.choice(range(2, 7))
            i, j = random.sample(range(1, sol_len-k-1), 2)
            if abs(i-j)>k and solution[i] != 0 and solution[j] != 0:
                if verbose:
                    print('Swap: ', solution[i:i+k], solution[j:j+k])
                solution[i:i+k], solution[j:j+k] = copy(solution[j:j+k][::-1]), copy(solution[i:i+k][::-1])

                # there shouldn`t be several depots in a row for example [0, 0,.. ]
                if common.check_depots_sanity(solution):
                    break
            patience -= 1

        return solution

    @staticmethod
    def random_insert_sub_reverse(_solution, patience=10, verbose=False):
        if verbose:
            print('random insertion of subsequence')
        solution = copy(_solution)
        sol_len  = len(solution)
        while patience > 0:
            k = random.choice(range(2, 7))
            i, j = random.sample(range(1, sol_len-k-1), 2)
            if abs(i-j) <= k:
                continue
            i, j = copy(min(i, j)), copy(max(i, j))
            if verbose:
                print('Insert: ',_solution[j:j+k], 'to', i, i+k)
            solution[:i] = _solution[:i]
            solution[i:i+k]  = _solution[j:j+k][::-1]
            solution[i+k:j+k] = _solution[i:j]
            solution[j+k:]  = _solution[j+k:]

            # there shouldn`t be several depots in a row for example [0, 0,.. ]
            if common.check_depots_sanity(solution):
                break
            patience -= 1

        return solution
