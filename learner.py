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
        for f in self.pending:
            song = Song(filename=f)
            self.songs += [song]
            self.instruments.extend(filter(None, song.instruments))

        # Do clustering stuff, group instruments
        instrument_vecs = np.array([instrument.vector for instrument in
                                    self.instruments])
        linkage = sch.linkage(instrument_vecs)
        # linkage is a weird format... gotta think about that

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
    return learner  # TODO: analyze, etc.


if __name__ == '__main__':
    main(argv[1:])
