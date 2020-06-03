import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from itertools import combinations


def get_problem(path) -> dict:

    with open(path, 'r') as f:
        file = f.read()
        file = file.split('\n')

    problem_dct = {}
    for i, row in enumerate(file):
        if 'COMMENT' in row:

            pat = 'No of trucks:'
            ind = row.find(pat)+len(pat)
            end = ind + row[ind:].index(',')
            problem_dct['n_trucks'] = int(row[ind+1:end])

            pat = 'Optimal value:'
            ind = row.find(pat)+len(pat)
            end = ind + row[ind:].index(')')
            problem_dct['optimal'] = int(row[ind+1:end])

        if 'CAPACITY' in row:
            pat = 'CAPACITY :'
            ind = row.find(pat)+len(pat)
            problem_dct['capacity'] = int(row[ind+1:])

        if 'NODE_COORD_SECTION' in row:
            locations = []
            for j, location in enumerate(file[i+1:]):
                if 'DEMAND_SECTION ' in location:
                    break
                _, x, y = location[1:].split(' ')
                locations.append((float(x), float(y)))
            problem_dct['locations'] = locations
            problem_dct['n_locations'] = len(locations)

        if 'DEMAND_SECTION' in row:
            demands = []
            for k, demand in enumerate(file[i+1:]):
                if 'DEPOT_SECTION' in demand:
                    break
                i, demand = demand[:-1].split(' ')
                if float(demand) == 0:
                    problem_dct['depot_i'] = int(i) - 1
                demands.append((float(demand)))

            assert problem_dct['n_locations'] == len(demands)
            problem_dct['demands'] = demands
            break

    locations = problem_dct['locations']
    n = problem_dct['n_locations']
    cost = np.ones((n, n), dtype=np.float32)
    cost *= -1
    for comb in combinations(np.arange(n, dtype=np.int32), 2):
        i, j = comb
        if i != j and cost[i,j] == -1:
            c = np.linalg.norm([x - y for x, y in
                                zip(locations[i] , locations[j])])
            cost[i, j] = c
            cost[j, i] = c
    problem_dct['cost'] = cost

    return problem_dct


def generate_solution(problem, patience=10) -> np.ndarray:

    sol_len  = problem['n_trucks']+problem['n_locations']
    while patience > 0:
        patience -= 1
        solution = np.zeros(sol_len, dtype=np.int32)
        indexes  = np.arange(1,sol_len-1, dtype=np.int32)
        random_assignee = random.sample(indexes.tolist(), problem['n_locations'])
        for i, place in enumerate(random_assignee):
            solution[place] = i
        if check_solution(problem, solution):
            break
        elif patience == 0:
            raise ValueError('Patience left up')
    return solution


def compute_solution(problem, solution) -> np.float32:
    # compute solution cost
    # cost = Sum DijXij
    n = problem['n_locations']
    x = np.zeros((n, n), dtype=np.int32)
    for i, loc in enumerate(solution[:-1]):
        x[solution[i], solution[i+1]] = 1
    if not check_solution(problem, solution, x):
        return 10**100
    return problem['cost'][x == 1].sum()


def check_solution(problem, solution, x=None) -> bool:

    # sanity check №1
    # len(solution) == n_locations + n_trucks
    sol_len = len(solution)
    if not sol_len == problem['n_trucks'] + problem['n_locations']:
        print('Solution len {} but should be {}' \
              .format(sol_len, prolem['n_trucks'] + problem['n_locations']))
        return False

    # sanity check №2
    # The end and the start of the solution should be depot
    depots = list(filter(lambda i: solution[i]==0, range(sol_len)))
    if depots[0] != 0 or depots[-1] != sol_len-1:
        print('The end and the start of the solution should be depot', sol_len)
        print(depots)
        return False

    # sanity check №3
    # there shouldn`t be several depots in a row for example [0, 0,.. ]
    for i in range(len(depots)-1):
        if depots[i+1] - depots[i] <= 1:
            print('Several depots in a row: {}'.format(depots))
            return False

    # cruteria check №1
    # Sum Xi0 = M For all i in V
    # Sum X0j = M For all j in V and
    # where M is the number of trucks
    if  not isinstance(x, np.ndarray):
        n = problem['n_locations']
        x = np.zeros((n, n), dtype=np.int32)
        for i, loc in enumerate(solution[:-1]):
            x[solution[i], solution[i+1]] = 1
    try:
        assert x[0, :].sum() == problem['n_trucks']
        assert x[:, 0].sum() == problem['n_trucks']
    except Exception as e:
        print(e)
        print('n_trucks =', problem['n_trucks'])
        print('Sum Xi0 = ', x[:, 0].sum())
        print('Sum X0j = ', x[0, :].sum())
        print(solution)
        return False

    # criteria check №2
    # Sum Xij = 1 For all j in V\{0} and
    # Sum Xij = 1 For all i in V\{0}
    try:
        assert x.sum(axis=1)[1: ].sum() == problem['n_locations'] - 1
        assert x.sum(axis=0)[1: ].sum() == problem['n_locations'] - 1
    except Exception as e:
        print(e)
        print('Sum Xij for j = ', x.sum(axis=1)[1: ])
        print('Sum Xij for j= ', x.sum(axis=0)[1: ])
        return False

    # criteria check №3
    # route  demand  <= truck capacity
    demands  = problem['demands']
    capacity = problem['capacity']
    for i, d in  enumerate(depots[:-1]):
        route = solution[depots[i]+1:depots[i+1]]
        route_demand = np.sum([demands[place] for place in route])
        if route_demand > capacity:
            print('Route demand {} exeeds capacity {}' \
                    .format(route_demand, capacity))
            print('Route ', route)
            return False
    return True


def visualize_problem(problem, solution=None, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    locations = problem['locations']
    plt.plot([loc[0] for loc in locations],
             [loc[1] for loc in locations], 'o', label='locations')
    depot = locations[problem['depot_i']]
    plt.plot(depot[0], depot[1], 'o', label='depot', markersize=13)
    if isinstance(solution, np.ndarray):
        counter = 1
        plt.annotate("0".format(counter),
                      locations[solution[0]],
                      size=18)

        for i in solution:
            if i != 0:
                plt.annotate("{}".format(counter),
                              locations[i],
                              size=16)
                counter += 1
            else:
                counter = 1

        depots_i = list(filter(lambda i: solution[i]==0, range(len(solution))))
        for i, depot in enumerate(depots_i[:-1]):
            locs_i = solution[depots_i[i]:depots_i[i+1]+1].tolist()
            locs = [locations[i] for i in locs_i]
            plt.plot([loc[0] for loc in locs],
                     [loc[1] for loc in locs], '--',
                     label='route ' + str(i+1))
    plt.legend()
    plt.grid()
