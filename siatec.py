import numpy as np
from itertools import chain, combinations
from functools import reduce
from collections import defaultdict


class SIATEC:

    def __init__(self, data, nmtps=100):
        self.data = list(sorted(data))
        self.nmtps = nmtps
        self.array = np.array(self.data)
        self.num_points, self.dimensions = self.array.shape
        self.adjacency = None
        self.patterns = None
        self.occurences = None

    def analyze(self):
        self.make_adjacency()
        self.sia_mtps()
        self.siatec_mtps()

    def make_adjacency(self):
        self.adjacency = np.zeros((self.num_points, self.num_points,
                                   self.dimensions), dtype=np.int32)
        self.adjacency -= self.data
        self.adjacency = self.adjacency.transpose(1,0,2)
        self.adjacency += self.data

    def sia_mtps(self):
        translations = defaultdict(list)
        for n in range(self.num_points):
            for m in range(n+1, self.num_points):
                translations[tuple(self.adjacency[n, m])] += [self.data[n]]
        cutoff = sorted(map(len, translations.values()))[self.nmtps]
        self.patterns = sorted(filter(lambda v: len(v) > cutoff,
                                      translations.values()),
                               key=lambda v: len(v),
                               reverse=True)

    
