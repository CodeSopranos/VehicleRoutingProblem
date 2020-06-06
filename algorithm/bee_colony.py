import random
import numpy as np
import importlib as imp

from copy import copy
from utils import tools
from random import randint
from itertools import combinations
from tqdm import tqdm, tqdm_notebook

from utils import tools, common
from algorithm import neighbor_operator, local_search
from algorithm.base import Algorithm

neighbor_operator = imp.reload(neighbor_operator)
local_search = imp.reload(local_search)


class BeeColony(Algorithm):

    def __init__(self, problem):
        self.problem = problem

    @property
    def name(self):
        return 'ArtificalBeeColony'

    def set_params(self,
                   n_epoch=1000,
                   n_initials=20,
                   n_onlookers=10,
                   search_limit=50):

        self.history = []
        self.n_epoch = n_epoch
        self.n_initials = n_initials
        self.n_onlookers = n_onlookers
        self.search_limit = search_limit


    @staticmethod
    def fitness(problem, solution, alpha=0.5):
        c = common.compute_solution(problem, solution)
        q = common.check_capacity_criteria(problem, solution)
        return 1 / (c + alpha * q)


    def solve(self):

        solutions = [common.generate_solution(self.problem)
                     for _ in range(self.n_initials)]
        fitnesses = [self.fitness(self.problem, solution)
                     for solution in solutions]
        counters  = np.zeros(self.n_initials, dtype=np.int32)

        alg = local_search.LocalSearch(self.problem)
        for _ in tqdm_notebook(range(self.n_epoch), total=self.n_epoch):

            # for each food source apply neighbor operator
            for i, solution in enumerate(solutions):
                alg.set_params(solution, n_iter=100)
                neighbor, _ = alg.solve()
                nfitness = self.fitness(self.problem, neighbor)
                if nfitness > fitnesses[i]:
                    solutions[i] = neighbor
                    fitnesses[i] = nfitness
                    counters[i]  = 0
                else:
                    counters[i] += 1

            # for each onlooker select food source
            neighborhood = [[] for _ in range(self.n_initials)]
            nn_operator  = neighbor_operator.NeighborOperator()
            probs        = [f / sum(fitnesses) for f in fitnesses]
            for _ in range(self.n_onlookers):
                roulette = np.random.choice(range(len(probs)), p=probs)
                solution = solutions[roulette]
                neighbor = nn_operator.random_operator(solution)
                neighborhood[roulette].append(neighbor)

            for i, neighbors in enumerate(neighborhood):
                if neighbors:
                    fits = [self.fitness(self.problem, neighbor)
                            for neighbor in neighbors]
                    if max(fits) > fitnesses[i]:
                        solutions[i] = neighbors[np.argmax(fits)]
                        fitnesses[i] = max(fits)
                        counters[i]  = 0
                    else:
                        counters[i] += 1

            # for each food source check limit
            # if counter = limit then replace with random solution
            for i, solution in enumerate(solutions):
                if counters[i] == self.search_limit:
                    # solutions[i] = common.generate_solution(self.problem)
                    solutions[i] = nn_operator.random_operator(solution)

            self.history.append(1 / np.max(fitnesses))
        return solutions[np.argmax(fitnesses)]
