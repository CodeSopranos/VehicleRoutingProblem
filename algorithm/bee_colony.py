import random
import numpy as np
from copy import copy
from utils import tools
from random import randint
from itertools import combinations
from tqdm import tqdm, tqdm_notebook

from utils import tools
from algorithm.base import Algorithm


class BeeColony(Algorithm):

    def __init__(self, problem):
        self.problem = problem

    @property
    def name(self):
        return 'ArtificalBeeColony'

    def solve(self):
        pass
