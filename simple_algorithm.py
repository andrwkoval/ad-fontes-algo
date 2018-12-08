from datasets import DATASET_4N_diff as dataset
from itertools import chain, combinations

AGENTS = {i for i in dataset.keys() if len(i) == 1}
N = len(AGENTS)  # number of agents
func_1 = dict()
func_2 = dict()


def setup_global_func_2():
    """setups our function with 1 and 2 length items"""

    # setups 1 len items
    for element in dataset.keys():
        if len(element) == 1:
            func_2[element] = dataset[element]
    global_with_1 = len(func_2)
    # for now setups all 2 len items in n**2 will be optimised later
    for i in range(1, global_with_1 + 1):
        for g in range(1, global_with_1 + 1):
            if i < g:
                func_2[(i, g)] = dataset[(i,)] + \
                                 dataset[(g,)]

    return func_2


# setup starting set
setup_global_func_2()


def compute_f2(dict_values):
    try:
        return func_2[dict_values]
    except:
        pass
    # variable for finding optimal max solution
    max_counter = 0
    elements = None
    for g in all_subsets(dict_values):
        for d in all_subsets(dict_values):
            if d != g:
                if len(d + g) == len(dict_values) and (
                        len(g) != 0 and len(d) != 0) and len(
                    set(d + g)) == len(d + g):
                    sum = 0
                    # going through 2 sides of subset and finding the best
                    # solution either from exciting
                    # dict or by calculating func_2
                    for element in (d, g):

                        if dataset[tuple(sorted(element))] > \
                                func_2[tuple(sorted(element))]:
                            sum += dataset[tuple(sorted(element))]
                        else:
                            sum += dataset[tuple(sorted(element))]

                    if sum > max_counter:
                        elements = g + d
                        max_counter = sum
    if elements is not None:
        func_2[tuple(sorted(elements))] = max_counter
    return max_counter


def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss) + 1)))


# Step 1
for i in dataset.keys():
    if len(i) == 1:
        func_1[i] = i
        func_2[i] = dataset[i]

# Step 2
for s in range(1, N + 1):
    for key in dataset.keys():
        if len(key) != s:
            continue

        temp = []
        # max([(compute_f2(coal) +
        #              compute_f2(set(key).difference(coal)),
        #              [coal] + [set(key).difference(set(coal))])
        #             for coal in all_subsets(key)
        #             if len(coal) <= len(key)], key=lambda x: x[0])
        for coal in all_subsets(key):
            if len(coal) <= len(key) / 2:
                f2 = compute_f2(coal) + \
                     compute_f2(set(key).difference(set(coal)))
                f1 = [coal] + [set(key).difference(set(coal))]
                temp.append((f2, f1))

        maximum = max(temp, key=lambda x: x[0])
        func_2[key] = maximum[0]
        if func_2[key] >= dataset[key]:
            func_1[key] = maximum[1]
        else:
            func_1[key] = key
            func_2[key] = dataset[key]

print(func_1)
print(func_2)
