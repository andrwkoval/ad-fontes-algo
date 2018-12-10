import pickle
from itertools import chain, combinations
import tracemalloc


def all_subsets(ss):
    return tuple(chain(*map(lambda x: combinations(ss, x), range(1, len(ss)//2+1))))


def set_diff(key1, key2):
    return tuple(sorted(set(key1).difference(set(key2))))


def dp_csg(data):
    tracemalloc.start()
    func1 = dict()
    func2 = dict()
    agents = data.keys()
    splittings = 0

    # Step 1
    for i in agents:
        if len(i) == 1:
            func1[i] = i
            func2[i] = data[i]

    # Step 2
    for s in range(2, len(agents) + 1):
        for parts in agents:
            if len(parts) != s:
                continue
            best_coal = parts
            maximum = data[parts]
            subsets = all_subsets(parts)
            splittings += len(subsets)
            for ss in subsets:
                # if 1 <= len(ss) <= len(parts):
                if func2[ss] + func2[set_diff(parts, ss)] > maximum:
                    maximum = func2[ss] + func2[set_diff(parts, ss)]
                    best_coal = (ss, set_diff(parts, ss))
            func1[parts] = best_coal
            func2[parts] = maximum

    # steps 3-4
    coalition_structure = []
    print(splittings)

    def find_best(struct):
        if func1[struct] == struct:
            coalition_structure.append(struct)
            return
        find_best(func1[struct][0])
        find_best(func1[struct][1])

    subset = max(agents, key=lambda x: len(x))
    find_best(subset)
    return coalition_structure, func2[subset]


if __name__ == '__main__':
    with open("datasets/{}_dataset0".format(12), "rb") as f:
        data1 = pickle.load(f)

    tracemalloc.start()
    print(dp_csg(data1))
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('filename')

    for stat in top_stats:
        print(stat)
