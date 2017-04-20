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

    def analyze(self, files=[]):
        self.pending.extend((path.relpath(f, self.prefix) for f in files))

        # Collect all songs (was hoping for less memory consumption)
        while self.pending:
            f = self.pending.pop()
            print("Add file:", f)
            song = Song(filename=f)
            self.songs += [song]
            self.instruments.extend(filter(None, song.instruments))
            self.learned += [f]

        # Assemble vectors
        instrument_vecs = np.array([instrument.vector for instrument in
                                    self.instruments])

        # Standardize axes
        instrument_vecs /= np.std(instrument_vecs, 0)[np.newaxis, :]
        instrument_vecs -= np.std(instrument_vecs, 0)[np.newaxis, :]

        # Do clustering stuff, group instruments        
        linkage = sch.linkage(instrument_vecs, method='complete')
        # linkage is a weird format... gotta think about that
        return linkage

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
    linkage = learner.analyze()
    print('\n'.join(('{:4.0f}, {:4.0f}, {:5.2f}, {:4.0f}'.format(*row)
                     for row in linkage)))
    return learner, linkage  # TODO: analyze, etc.


if __name__ == '__main__':
    main(argv[1:])
