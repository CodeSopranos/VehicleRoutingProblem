import random
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


def get_problem(path):
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
    return problem_dct


def generate_solution(problem):
    sol_len  = problem['n_trucks']+problem['n_locations']
    solution = np.zeros(sol_len, dtype=np.int32)
    indexes  = np.arange(1,sol_len-1, dtype=np.int32)

    random_assignee = random.sample(indexes.tolist(), problem['n_locations'])
    for i, place in enumerate(random_assignee):
        solution[place] = i

    return solution


def visualize_problem(problem, solution=None):
    plt.figure(figsize=(10, 6))
    locations = problem['locations']
    plt.plot([loc[0] for loc in locations],
             [loc[1] for loc in locations], 'o', label='locations')
    depot = locations[problem['depot_i']]
    plt.plot(depot[0], depot[1], 'o', label='depot', markersize=13)
    if isinstance(solution, np.ndarray):
        depots_i = list(filter(lambda i: solution[i]==0, range(len(solution))))
        for i, depot in enumerate(depots_i[:-1]):
            locs_i = solution[depots_i[i]:depots_i[i+1]+1].tolist()
            locs = [locations[i] for i in locs_i]
            plt.plot([loc[0] for loc in locs],
                     [loc[1] for loc in locs], '--',
                     label='route ' + str(i+1))
    plt.legend()
    plt.grid()
