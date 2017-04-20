import numpy as np
import scipy.cluster.hierarchy as sch
import copy
from os import path
from sys import stderr, argv
from glob import glob
from song import Song
from instrument import Instrument
from listen import Listen


class Learner:

    ideals = []

    def __init__(self, files=[]):
        self.pending = [path.abspath(f) for f in files]
        self.prefix = path.commonprefix(self.pending) or path.abspath('.')
        self.learned = []
        self.songs = []
        self.instruments = []
        self.ideal_sample_indexes = []

    def make_groups(self,linkage):
        size = len(linkage) + 1
        print("size: " + str(size))
        print("ideal list is " + str(self.ideal_sample_indexes))

        clusters = []
        temp = clusters

        # A dictionary that contains where in the clusters list each index maps to
        indices = {}

        # Use the size for a stopping heurstic
        i = size
        for row in linkage:

            temp = copy.deepcopy(clusters)

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

            flag = 0

            # New break heuristic: Run until two ideal_sample_indexes are in the same cluster
            for cluster in clusters:
                count = 0
                for j in self.ideal_sample_indexes:
                    find = cluster.count(j)
                    if find > 1:
                        print("WARNING")
                        break
                    count += find
                if count > 1:
                    print("collision between clusters")
                    flag = 1
                    break

            if flag == 1:
                break
            

        clusters = temp

        for row in clusters:
            print([int(x) for x in row])
            print("======================")




    def analyze(self, files=[]):
        self.pending.extend((path.relpath(f, self.prefix) for f in files))

        # Collect all songs (was hoping for less memory consumption)

        i = 0

        ideal_treble = -1
        ideal_bass = -1
        ideal_pad = -1
        ideal_bassdrum = -1
        ideal_hihat = -1

        while self.pending:
            f = self.pending.pop()
            #print("Add file:", f)
            song = Song(filename=f)

            # But how can you count if there are empty samles?
            if f == "/home/adam/CS673/amigabyte/mods/mods/SimpleMods/coldbeer.mod":
                print("coldbeer treble sample num is " + str(i + 1 - 1))
                ideal_treble = i + 1 - 1

            elif f == "/home/adam/CS673/amigabyte/mods/mods/SimpleMods/aladinhampun_henki.mod":
                print("aladinhampun_henki bass sample num is " + str(i + 2))
                ideal_bass = i + 2

            elif f == "/home/adam/CS673/amigabyte/mods/mods/SimpleMods/cardiaxx_1.mod":
                print("cardiaxx_1 pad sample num is " + str(i + 2 - 1))
                ideal_pad = i + 2 - 1

            elif f == "/home/adam/CS673/amigabyte/mods/mods/SimpleMods/simppagoespoing.mod":
                print("simppagoespoing bassdrum sample num is " + str(i + 1 - 1))
                ideal_bassdrum = i + 1 - 1

            elif f == "/home/adam/CS673/amigabyte/mods/mods/SimpleMods/irontear.mod":
                print("song24 hihat sample num is " + str(i + 5 - 1))
                ideal_hihat = i + 5 - 1

            self.songs += [song]
            self.instruments.extend(filter(None, song.instruments))
            self.learned += [f]
            i += len(list(filter(None, song.instruments)))


        self.ideal_sample_indexes.append(ideal_treble)
        self.ideal_sample_indexes.append(ideal_bass)
        self.ideal_sample_indexes.append(ideal_pad)
        self.ideal_sample_indexes.append(ideal_bassdrum)
        self.ideal_sample_indexes.append(ideal_hihat)

        # listen = Listen()
        # listen.play_instrument(self.instruments[ideal_hihat])

        # test_list = [1,2,3,4,1,5,6,7,8,9]
        # print(test_list.count(1))
        # print(test_list.count(2,3))

        # Assemble vectors
        instrument_vecs = np.array([instrument.vector for instrument in
                                    self.instruments])

        # Standardize axes
        instrument_vecs /= np.std(instrument_vecs, 0)[np.newaxis, :]
        instrument_vecs -= np.std(instrument_vecs, 0)[np.newaxis, :]

        # Do clustering stuff, group instruments        
        linkage = sch.linkage(instrument_vecs, method='ward')
        # linkage is a weird format... gotta think about that

        self.make_groups(linkage)

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
    # print('\n'.join(('{:4.0f}, {:4.0f}, {:5.2f}, {:4.0f}'.format(*row)
    #                 for row in linkage)))
    return learner, linkage  # TODO: analyze, etc.


if __name__ == '__main__':
    main(argv[1:])
