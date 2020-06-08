import random
import numpy as np
import importlib as imp

from copy import copy
from utils import tools
from random import randint
from datetime import datetime
from itertools import combinations
from tqdm import tqdm, tqdm_notebook

from utils import tools, common
from algorithm import neighbor_operator, local_search
from algorithm.base import Algorithm


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
        self.history_alpha = []
        self.history_betta = []
        self.n_epoch = n_epoch
        self.n_initials = n_initials
        self.n_onlookers = n_onlookers
        self.search_limit = search_limit


    @staticmethod
    def fitness(problem, solution, alpha=0.5, betta=0.5):
        c = common.compute_solution(problem, solution)
        demands = common.get_routes_demand(problem, solution)
        q =  max(demands) - problem['capacity']
        t =  0 # max(map(len, common.get_routes(solution)))
        return 1 / (c + alpha * q + betta * t)


    def solve(self, alpha=0.2, betta=0.2, delta=0.01, gen_alpha=1, gen_betta=0.5):

        solutions = [common.generate_solution(self.problem,
                                              alpha=gen_alpha,
                                              betta=gen_betta,
                                              patience=100)
                     for _ in range(self.n_initials)]
        # print('depots',sum([common.check_depots_sanity(x) for x in solutions]))
        # print('capacity',sum([common.check_capacity_criteria(self.problem, x)
        #                       for x in solutions]))

        fitnesses = [self.fitness(self.problem, solution, alpha=alpha, betta=betta)
                     for solution in solutions]
        counters  = np.zeros(self.n_initials, dtype=np.int32)

        alg = local_search.LocalSearch(self.problem)
        operator  = neighbor_operator.NeighborOperator()
        for _ in tqdm_notebook(range(self.n_epoch), total=self.n_epoch):

            # for each food source apply neighbor operator
            # *enhanced with local search based on neighbors operators
            for i, solution in enumerate(solutions):
                alg.set_params(solution, n_iter=12)
                neighbor, _ = alg.solve(only_feasible=True)
                nfitness    = self.fitness(self.problem, neighbor, alpha=alpha, betta=betta)
                if nfitness > fitnesses[i]:
                    solutions[i] = neighbor
                    fitnesses[i] = nfitness
                    counters[i]  = 0
                else:
                    counters[i] += 1

            # for each onlooker select food source
            # *based on roulette wheel choice
            neighborhood = [[] for _ in range(self.n_initials)]
            nn_operator  = neighbor_operator.NeighborOperator()
            f_sum  = sum(fitnesses)
            probs  = [f / f_sum  for f in fitnesses]
            for _ in range(self.n_onlookers):
                roulette = np.random.choice(range(len(probs)), p=probs)
                solution = solutions[roulette]
                neighbor = nn_operator.random_operator(solution, patience=20)
                neighborhood[roulette].append(neighbor)
                # enhanced version
                for i, neighs in enumerate(neighborhood):
                    # if i != roulette and common.check_depots_sanity(neighbor):
                    if common.check_capacity_criteria(self.problem, neighbor):
                        neighs.append(neighbor)

            for i, neighbors in enumerate(neighborhood):
                if neighbors:
                    fits = [self.fitness(self.problem, neighbor, alpha=alpha, betta=betta)
                            for neighbor in neighbors]
                    if max(fits) > fitnesses[i]:
                        solutions[i] = neighbors[np.argmax(fits)]
                        fitnesses[i] = max(fits)
                        counters[i]  = 0
                    else:
                        counters[i] += 1

            # for each food source check limit
            # if counter = limit then replace with neighbor
            for i, solution in enumerate(solutions):
                if counters[i] == self.search_limit:
                    solutions[i] = nn_operator.random_operator(solution, patience=10)

            # check capacity criteria and adjust fitness parameters
            criteria = [common.check_capacity_criteria(self.problem, solution)
                        for solution in solutions]
            if sum(criteria) > (len(criteria) / 2):
                alpha -= delta#alpha / (1 + delta)
            else:
                alpha += delta

            self.history.append(1 / np.mean(fitnesses))
            self.history_alpha.append(alpha)

        # print('depots', sum([common.check_depots_sanity(x) for x in solutions]))
        # print('capacity', sum([common.check_capacity_criteria(self.problem, x)
        #                       for x in solutions]))

        # return the best feasible solution
        for i in range(self.n_initials):
            solution = solutions[np.argmax(fitnesses)]
            if not common.check_solution(self.problem, solution):
                del(solutions[np.argmax(fitnesses)])
                del(fitnesses[np.argmax(fitnesses)])
            else:
                print('Tries: ', i)
                break
        return solution
