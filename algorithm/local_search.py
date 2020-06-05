import random
import numpy as np
from copy import copy
from random import randint
from itertools import combinations
from tqdm import tqdm, tqdm_notebook

from utils import tools, common
from algorithm.base import Algorithm


class LocalSearch(Algorithm):

    def __init__(self, problem):
        self.problem = problem

    @property
    def name(self):
        return 'LocalSearch'


    def set_params(self, solution, n_iter, **params):
        self.solution = copy(solution)
        self.n_iter   = n_iter
        self.params   = params


    def solve(self, verbose=False, k=3):
        self.cur_cost = common.compute_solution(self.problem, self.solution)
        if verbose:
            print('Start cost: {}'.format(self.cur_cost))
        for comb in tqdm(combinations(np.arange(1, len(self.solution)-k,
                                                dtype=np.int32), 2)):
            tmp_sol = copy(self.solution)
            i, j = comb
            if abs(i-j) > k:
                tmp_sol[i:i+k], tmp_sol[j:j+k] = copy(tmp_sol[j:j+k]), copy(tmp_sol[i:i+k])
            else:
                continue
            cost = common.compute_solution(self.problem, tmp_sol)
            if self.cur_cost > cost:
                self.cur_cost = cost
                self.solution = tmp_sol

            if self.n_iter == 0:
                break
            self.n_iter -= 1


        return self.solution, self.cur_cost
