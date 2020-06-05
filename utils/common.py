import random
import numpy as np
import pandas as pd

from copy import copy
from datetime import datetime
from itertools import combinations
from tqdm import tqdm, tqdm_notebook


def generate_solution(problem,
                      patience=10,
                      verbose=False) -> np.ndarray:

    dists   = problem['dists']
    demands = problem['demands']
    i_loc   = [i for i in range(1, problem['n_locations'])]
    routes  = [[0] for _ in range(problem['n_trucks'])]

    for i in range(len(i_loc)):
        route_dists = []
        random_loc  = random.choice(i_loc)
        for route in routes:
            dist_to_loc  = dists[route[-1]][random_loc]
            route_demand = sum([demands[i] for i in route])
            alpha = (route_demand + 0.5*dist_to_loc)
            route_dists.append(alpha)
        routes[np.argmin(route_dists)].append(random_loc)
        i_loc.remove(random_loc)

    solution = [loc for route in routes for loc in route]
    solution.append(0)
    solution = np.array(solution, dtype=np.int32)

    return solution


def compute_solution(problem, solution) -> np.float32:
    # compute solution cost
    # cost = Sum DijXij
    n = problem['n_locations']
    x = np.zeros((n, n), dtype=np.int32)
    for i, loc in enumerate(solution[:-1]):
        x[solution[i], solution[i+1]] = 1
    cost = problem['dists'][x == 1].sum()
    return cost


def check_solution(problem,
                   solution,
                   x=None,
                   verbose=False) -> bool:
    # sanity check №1
    # len(solution) == n_locations + n_trucks
    sol_len  = len(solution)
    plan_len = problem['n_trucks'] + problem['n_locations']
    if not sol_len == plan_len:
        if verbose:
            print('Solution len {} but should be {}' \
                  .format(sol_len, plan_len))
        return False

    # sanity check №2
    # The end and the start of the solution should be depot
    depots = list(filter(lambda i: solution[i]==0, range(sol_len)))
    if depots[0] != 0 or depots[-1] != sol_len-1:
        if verbose:
            print('The end and the start of the solution should be depots')
            print(depots)
        return False

    # sanity check №3
    # there shouldn`t be several depots in a row for example [0, 0,.. ]
    for i in range(len(depots)-1):
        if depots[i+1] - depots[i] <= 1:
            if verbose:
                print('Several depots in a row: {}'.format(depots))
            return False

    if  not isinstance(x, np.ndarray):
        n = problem['n_locations']
        x = np.zeros((n, n), dtype=np.int32)
        for i, loc in enumerate(solution[:-1]):
            x[solution[i], solution[i+1]] = 1

    # cruteria check №1
    # Sum Xi0 = M For all i in V
    # Sum X0j = M For all j in V and
    # where M is the number of trucks
    if not check_M_criteria(problem,
                            solution,
                            x=x,
                            verbose=verbose):
        return False

    # criteria check №2
    # Sum Xij = 1 For all j in V\{0} and
    # Sum Xij = 1 For all i in V\{0}
    if not check_One_criteria(problem,
                              solution,
                              x=x,
                              verbose=verbose):
        return False

    # criteria check №3
    # route  demand  <= truck capacity
    if not check_capacity_criteria(problem,
                                   solution,
                                   verbose=verbose):
        return False

    return True


def check_One_criteria(problem,
                       solution,
                       x=None,
                       verbose=False) -> bool:
    if not ((x.sum(axis=1)[1: ].sum() == problem['n_locations'] - 1) and
            (x.sum(axis=0)[1: ].sum() == problem['n_locations'] - 1)):
            if verbose:
                print('Sum Xij for j = ', x.sum(axis=1)[1: ])
                print('Sum Xij for j = ', x.sum(axis=0)[1: ])
            return False

    return True


def check_M_criteria(problem,
                     solution,
                     x=None,
                     verbose=False) -> bool:

    if  not isinstance(x, np.ndarray):
        n = problem['n_locations']
        x = np.zeros((n, n), dtype=np.int32)
        for i, loc in enumerate(solution[:-1]):
            x[solution[i], solution[i+1]] = 1

    if  not ((x[0, :].sum() == problem['n_trucks']) and
              x[:, 0].sum() == problem['n_trucks']):
        if verbose:
            print('n_trucks =', problem['n_trucks'])
            print('Sum Xi0 = ', x[:, 0].sum())
            print('Sum X0j = ', x[0, :].sum())
            print(solution)
        return False

    return True


def check_capacity_criteria(problem,
                            solution,
                            verbose=False) -> bool:
    capacity = problem['capacity']
    routes_demand = get_routes_demand(problem, solution)
    for route_demand in routes_demand:
        if route_demand > capacity:
            if verbose:
                print('Route demand {} exeeds capacity {}' \
                        .format(route_demand, capacity))
                print('Route ', routes_demand)
            return False
    return True


def get_routes_demand(problem, solution):
    sol_len = len(solution)
    demands = problem['demands']
    depots = list(filter(lambda i: solution[i]==0, range(sol_len)))
    routes = []
    for i, d in  enumerate(depots[:-1]):
        route = solution[depots[i]+1:depots[i+1]]
        route_demand = np.sum([demands[place] for place in route])
        routes.append(route_demand)
    return routes
