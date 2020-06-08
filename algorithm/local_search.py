import random
import numpy as np
from copy import copy
from random import randint
import importlib as imp
from itertools import combinations
from tqdm import tqdm, tqdm_notebook

from utils import tools, common
from algorithm import neighbor_operator
from algorithm.base import Algorithm
neighbor_operator = imp.reload(neighbor_operator)


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


    def solve(self, only_feasible=True, verbose=False):
        self.cur_cost = common.compute_solution(self.problem, self.solution)
        if verbose:
            print('Start cost: {}'.format(self.cur_cost))

        feasible_saving = copy(self.solution)
        operator = neighbor_operator.NeighborOperator()

        for _ in tqdm(range(self.n_iter), disable=(not verbose)):
            tmp_sol = operator.random_operator(self.solution)
            cost = common.compute_solution(self.problem, tmp_sol)
            if self.cur_cost >= cost:
                self.cur_cost = cost
                self.solution = tmp_sol
                if common.check_solution(self.problem, self.solution):
                    feasible_saving = copy(self.solution)

        if ((only_feasible) and
            (not common.check_solution(self.problem, self.solution))):
            self.solution = feasible_saving
            self.cur_cost = common.compute_solution(self.problem,
                                                    self.solution)
        return self.solution, self.cur_cost
