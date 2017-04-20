import numpy as np
import scipy.cluster.hierarchy as sch
from os import path
from sys import stderr, argv
from glob import glob
from song import Song
from instrument import Instrument


class Learner:

    def __init__(self, files=[]):
        self.pending = [path.abspath(f) for f in files]
        self.prefix = path.commonprefix(self.pending) or path.abspath('.')
        self.learned = []
        self.songs = []
        self.instruments = []

    def make_groups(self,linkage):
        print('\n'.join(('{:4d}, {:4d}, {:4.2f}, {:4d}'.format(int(row[0]), int(row[1]), row[2], int(row[3])) for row in linkage)))
        size = len(linkage) + 1
        print("size: " + str(size))

        clusters = []
        
        # A dictionary that contains where in the clusters list each index maps to
        indices = {}

        # Use the size for a stopping heurstic
        i = size
        for row in linkage:
            if (row[0] < size and row[1] < size):
                # Make a new cluster!
                new_list = [row[0], row[1]]
                indices[i] = len(clusters)
                clusters.append(new_list)
                
            else:
                # This row is adding a new point to an existing cluster.
                if (row[0] < size):
                    # row[1] is an existing cluster
                    # Add row[0] to cluster row[1]
                    clusters[indices[row[1]]].append(row[0])

                    # Update dictionary
                    indices[i] = indices[row[1]]

                elif (row[1] < size):
                    # row[0] is an existing cluster
                    # Add row[1] to cluster row[0]
                    clusters[indices[row[0]]].append(row[1])

                    # Update dictionary
                    indices[i] = indices[row[0]]

                else:                                 
                    clusters[indices[row[0]]].extend(clusters[indices[row[1]]])
                    clusters.pop(indices[row[1]])
                    indices[i] = indices[row[0]]
                    compare_val = indices[row[1]]
                    for key in indices:
                        if indices[key] >=  compare_val:
                            indices[key] -= 1
            i += 1
            
            # develop a stopping heuristic; if (x): break...etc.
            if i - size + 4 > size:
                break

        print(clusters)




    def analyze(self, files=[]):
        self.pending.extend((path.relpath(f, self.prefix) for f in files))

        # Collect all songs (was hoping for less memory consumption)
        # for f in self.pending:
        #     song = Song(filename=f)
        #     self.songs += [song]
        #     self.instruments.extend(filter(None, song.instruments))

        # # Do clustering stuff, group instruments
        # instrument_vecs = np.array([instrument.vector for instrument in
        #                             self.instruments])
        # linkage = sch.linkage(instrument_vecs)
        # linkage is a weird format... gotta think about that
        rand = np.random.random((20,2))
 #        rand = np.array([[ 0.62069072,  0.28716257],
 # [ 0.87386839,  0.80756872],
 # [ 0.58742085, 0.42972388],
 # [ 0.1732603,   0.53816397],
 # [ 0.72567464,  0.45044234],
 # [ 0.00047757,  0.37084419],
 # [ 0.98540316,  0.92339627],
 # [ 0.71150791,  0.56638905],
 # [ 0.63885578,  0.13505908],
 # [ 0.11304982,  0.75322435]])


        print(rand)
        linkage = sch.linkage(rand)
        self.make_groups(linkage)



        # Assemble fomm's in clusters (needs alignment and combination)

        # Find bridging pairs (to construct conditional probs)

    def compose(self):
        # Start with bass or random cluster, select a sample, and make
        # a motif/melody/line

        # Pick another cluster and get the conditional probabilities, and
        # compose that line as well

        # Maybe do once more to get drums or whatever was left out

        # Maybe maybe mess with stuff to make it more song-like (mutate)
        pass


def main(files):
    learner = Learner(files)
    learner.analyze()
    return learner  # TODO: analyze, etc.


if __name__ == '__main__':
    main(argv[1:])
