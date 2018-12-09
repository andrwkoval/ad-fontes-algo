import pickle
from itertools import chain, combinations
from datasets import dataset_6n_diff as dataset
import tracemalloc

tracemalloc.start()


def all_subsets(ss):
    return tuple(chain(*map(lambda x: combinations(ss, x), range(1, len(ss)))))


def dp_csg(data):
    func1, func2 = dict(), dict()
    agents = data.keys()

    # Step 1
    for i in agents:
        if len(i) == 1:
            func1[i] = i
            func2[i] = data[i]

    # Step 2
    for s in range(2, len(agents) + 1):
        for key in agents:
            if len(key) != s:
                continue

            temp = []
            for c in all_subsets(key):
                if 1 <= len(c) <= len(key):
                    temp.append(func2[c] + func2[tuple(sorted(set(key).difference(set(c))))])
            func2[key] = max(temp)

            if func2[key] >= data[key]:
                temp_coal = all_subsets(key)[temp.index(func2[key])]
                func1[key] = (temp_coal, tuple(sorted(set(key).difference(set(temp_coal)))))
            else:
                func1[key] = key
                func2[key] = data[key]

    # step 3-4
    coal_struct = []

    def find_best(struct):
        if func1[struct] == struct:
            coal_struct.append(struct)
            return
        find_best(func1[struct][0])
        find_best(func1[struct][1])

    subset = max(agents, key=lambda x: len(x))
    find_best(subset)
    return coal_struct, func2[subset]


if __name__ == '__main__':
    with open("17_0_sample", "rb") as f:
        data1 = pickle.load(f)
    print(dp_csg(data1))

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('filename')

    for stat in top_stats:
        print(stat)
