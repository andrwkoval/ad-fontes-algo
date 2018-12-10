from itertools import chain, combinations
from random import randint
import pickle


def all_subsets(ss):
    return tuple(chain(*map(lambda x: combinations(ss, x), range(1, len(ss)))))


def generate_datasets(min_agents, max_agents):
    filename_spec = "_dataset"
    for i in range(min_agents, max_agents + 1):
        for j in range(3):
            with open(str(i) + filename_spec + str(j)) as agents:
                all_coals = tuple(j for j in range(1, i + 1))
                subsets = all_subsets(all_coals)
                dataset = {c: randint(10, 40) * len(c) for c in all_coals}
                dataset[subsets] = randint(10, 40) * len(subsets)
                pickle.dump(dataset, agents)
