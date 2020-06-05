import numpy as np
import matplotlib.pyplot as plt


def visualize_problem(problem, solution=None, annotate=True, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    locations = problem['locations']

    if annotate:
        for i, loc in enumerate(locations):
            if len(str(i)) == 1:
                xoff, yoff = 0.5, 0.6
            else:
                xoff, yoff = 0.85, 0.7
            plt.annotate("{}".format(i),
                         (loc[0]-xoff, loc[1]-yoff),
                        size=9,
                        color='white')
    if isinstance(solution, np.ndarray):
        depots_i = list(filter(lambda i: solution[i]==0, range(len(solution))))
        for i, depot in enumerate(depots_i[:-1]):
            locs_i = solution[depots_i[i]:depots_i[i+1]+1].tolist()
            locs = [locations[i] for i in locs_i]
            plt.plot([loc[0] for loc in locs],
                     [loc[1] for loc in locs], '--',
                     label='route ' + str(i+1))
    plt.plot([loc[0] for loc in locations],
             [loc[1] for loc in locations], 'o',
             label='locations',
             color='black',
             markersize=12)
    depot = locations[problem['depot_i']]
    plt.plot(depot[0], depot[1], 'o', label='depot', markersize=13, color='red')
    plt.legend()
    plt.grid()
