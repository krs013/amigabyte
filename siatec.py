import numpy as np
from itertools import chain, combinations
from functools import reduce


class SIATEC:

    def __init__(self, data):
        self.data = np.array(sorted(data))
        self.num_points, self.dimensions = self.data.shape
        self.mtps = self.find_mtps()

    def find_mtps(self):
        vectors = [set(map(tuple, col)) for col in self.vector_table()]
        patterns = {}
        for combo in pairs_plus(range(self.num_points)):
            pattern = reduce(set.intersection, (vectors[n] for n in combo))
            if len(pattern) > 1:
                patterns[combo] = len(pattern) 
        return patterns

    def vector_table(self):
        vector_table = np.zeros((self.num_points, self.num_points,
                                 self.dimensions), dtype=np.int32)
        vector_table -= self.data
        vector_table = vector_table.transpose(1,0,2)
        vector_table += self.data
        return vector_table


def pairs_plus(items):
    return chain(*(combinations(items, x) for x in range(2, len(items))))
    
