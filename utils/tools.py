import random
import numpy as np
import pandas as pd

from copy import copy
from datetime import datetime
from itertools import combinations
from tqdm import tqdm, tqdm_notebook


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
    dists = np.ones((n, n), dtype=np.float32)
    dists *= -1
    for comb in combinations(np.arange(n, dtype=np.int32), 2):
        i, j = comb
        if i != j and dists[i,j] == -1:
            d = np.linalg.norm([x - y for x, y in
                                zip(locations[i] , locations[j])])
            dists[i, j] = d
            dists[j, i] = d
    problem_dct['dists'] = dists

    return problem_dct

def write_solution(solution, cost, filename):
    
    depots = list(filter(lambda i: solution[i]==0, range(len(solution))))
    with open('output/'+filename, 'w') as f:
        for i, d in  enumerate(depots[:-1]):
            route = solution[depots[i]+1:depots[i+1]]
            f.writelines('Route #{}: '.format(i+1)+' '.join(map(repr, route))+'\n')
        f.writelines('cost {}'.format(cost))
    f.close()
    return
