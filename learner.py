import numpy as np
import scipy.cluster.hierarchy as sch
import copy
from os import path
from sys import stderr, argv
from glob import glob
from song import Song
from instrument import Instrument
from listen import Listen
from cluster import Cluster
from generate import generator
from numpy.random import choice



class Learner:

    ideals = []

    def __init__(self, files=[]):
        self.pending = [path.abspath(f) for f in files]
        self.prefix = path.commonprefix(self.pending) or path.abspath('.')
        self.learned = []
        self.songs = []
        self.instruments = []
        self.ideal_sample_indexes = []

        self.ideal_treble = -1
        self.ideal_bass = -1
        self.ideal_pad = -1
        self.ideal_bassdrum = -1
        self.ideal_hihat = -1

        self.collected_song_samples = []
        self.basstreble_parings = None
        self.bass_cluster = None
        self.treb_cluster = None
        self.bassdrum_cluster = None
        self.snare_cluster = None


    def make_groups(self,linkage):
        size = len(linkage) + 1
        #print("size: " + str(size))
        #print("ideal list is " + str(self.ideal_sample_indexes))

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
        ######################################################################################## 

        clusters = temp

        self.bass_cluster = next(filter(lambda x: self.ideal_bass in x,
                                        clusters))
        self.treb_cluster = next(filter(lambda x: self.ideal_treble in x,
                                        clusters))
        self.bassdrum_cluster = next(filter(lambda x: self.ideal_bassdrum in x,
                                        clusters))
        self.snare_cluster = next(filter(lambda x: self.ideal_hihat in x,
                                        clusters))

        # listen = Listen()
        # listen.play_instrument(self.instruments[ideal_hihat])

        # print("*************************Bassdrum Row**********************")
        # for sample in bassdrum_row:
        #     listen.play_instrument(self.instruments[int(sample)])

        # print("*************************Snare Row************************")
        # for sample in snare_row:
        #     listen.play_instrument(self.instruments[int(sample)])

        # print("*************************Bass Row************************")
        # for sample in bass_row:
        #     listen.play_instrument(self.instruments[int(sample)])

        # print("*************************Treble Row************************")
        # for sample in treb_row:
        #     listen.play_instrument(self.instruments[int(sample)])


        #print(bass_row)
        #print(treb_row)

        # Find pairings 
        # for s in bass_row:
        #     for slist in self.collected_song_samples:
        #         for s2 in slist:

        basstreble_parings = []

        for slist in self.collected_song_samples:
            snb = [i for i in slist if i in self.bass_cluster]
            snt = [i for i in slist if i in self.treb_cluster]
            if snb and snt:
                #print(slist)
                for a in snb:
                    for b in snt:
                        #print(str(a) + ": " + str(b))
                        basstreble_parings.append([a, b])

        self.basstreble_parings = basstreble_parings
        #print(basstreble_parings)

    def analyze(self, files=[]):
        self.pending.extend((path.relpath(f, self.prefix) for f in files))

        # Collect all songs (was hoping for less memory consumption)

        i = 0

        ideal_treble = -1
        ideal_bass = -1
        ideal_pad = -1
        ideal_bassdrum = -1
        ideal_hihat = -1

        collected_song_samples = []

        while self.pending:
            f = self.pending.pop()
            # print("Add file:", f)
            song = Song(filename=f)

            if path.split(f)[-1] == "song24.mod":
                ideal_treble = len(self.instruments) + len(list(filter(
                    None, song.instruments[:5])))
                ideal_bass = len(self.instruments) + len(list(filter(
                    None, song.instruments[:2])))
                # ideal_pad = -1

                #ideal_bassdrum = len(self.instruments) + len(list(filter(
                #    None, song.instruments[:3])))
                #ideal_hihat = len(self.instruments) + len(list(filter(
                #    None, song.instruments[:4])))


            if path.split(f)[-1] == "bs1.mod":
                ideal_bassdrum = i + 5 - 1
                ideal_hihat = i + 8 - 1

            if path.split(f)[-1] == "fucking_disco.mod":
                idea_pad = i + 5 - 1

            # Idea: Add a bunch of pad samples, so that they don't get mixed in with the other clusters...?
            # if path.split(f)[-1] == "cardiaxx_1.mod":
            #     self.ideal_sample_indexes.append(i + 2 - 1)
            # for j in range(32):
            #     if song.instruments[j] is None:
            #         print(str(j) + " is none")
            self.songs += [song]
            self.instruments.extend(filter(None, song.instruments))
            self.learned += [f]
            collected_song_samples.append(list(range(i, i+len(list(
                filter(None, song.instruments))))))
            # What about a list of dictionaries?
            i += len(list(filter(None, song.instruments)))
            # print(collected_song_samples[len(collected_song_samples)-1])
            # print("....................")


        self.ideal_sample_indexes.append(ideal_treble)
        self.ideal_sample_indexes.append(ideal_bass)
        self.ideal_sample_indexes.append(ideal_pad)
        self.ideal_sample_indexes.append(ideal_bassdrum)
        self.ideal_sample_indexes.append(ideal_hihat)


        self.ideal_treble = ideal_treble
        self.ideal_bass = ideal_bass
        self.ideal_pad = ideal_pad
        self.ideal_bassdrum = ideal_bassdrum
        self.ideal_hihat = ideal_hihat

        self.collected_song_samples = collected_song_samples

        

        # test_list = [1,2,3,4,1,5,6,7,8,9]
        # print(test_list.count(1))
        # print(test_list.count(2,3))

        # Assemble vectors
        instrument_vecs = np.array([instrument.vector for instrument in
                                    self.instruments])

        # Standardize axes
        instrument_vecs /= np.std(instrument_vecs, 0)[np.newaxis, :]
        instrument_vecs -= np.mean(instrument_vecs, 0)[np.newaxis, :]

        instrument_vecs *= np.array([1.0,1.0,1.0])[np.newaxis, :]

        # Do clustering stuff, group instruments        
        linkage = sch.linkage(instrument_vecs, method='ward')
        groups = self.make_groups(linkage)

        ########################################################
        # Assemble the Samples

        # basspick = choice(self.bass_cluster)
        # bass_sample = self.instruments[int(basspick)].sample

        # trebpick = choice(self.treb_cluster)
        # treb_sample = self.instruments[int(trebpick)].sample

        # lopick = choice(self.bassdrum_cluster)
        # bassdrum_sample = self.instruments[int(lopick)].sample
        # bdpitch = self.instruments[int(lopick)]._rounded_pitch_num

        # hipick = choice(self.snare_cluster)
        # snare_sample = self.instruments[int(hipick)].sample
        # snpitch = self.instruments[int(hipick)]._rounded_pitch_num

        ########################################################

        # Assemble fomm's in clusters
        self.bass_cluster = Cluster(self.instruments, self.ideal_bass,
                                    self.bass_cluster)
        self.treb_cluster = Cluster(self.instruments, self.ideal_treble,
                                    self.treb_cluster)
        self.bassdrum_cluster = Cluster(self.instruments, self.ideal_bassdrum,
                                        self.bassdrum_cluster)
        self.snare_cluster = Cluster(self.instruments, self.ideal_hihat,
                                     self.snare_cluster)

        arrayprint = lambda x: print('\n'.join(('{:4.2f} '*len(y)).format(
            *y) for y in x))
        print('===')
        arrayprint(self.bass_cluster.fomm_pitch)
        print('===')
        arrayprint(self.bass_cluster.fomm_beats)
        
        # Find bridging pairs (to construct conditional probs)
        #self.bass_cluster.new_sample()
        bass_sample = self.bass_cluster.sample.sample
        #self.treb_cluster.new_sample()
        treb_sample = self.treb_cluster.sample.sample

        bassdrum_sample = self.bassdrum_cluster.sample.sample
        bdpitch = self.bassdrum_cluster.sample.rounded_pitch_num

        snare_pitch = self.snare_cluster.sample.sample
        snpitch = self.snare_cluster.sample.rounded_pitch_num

        generator(self.bass_cluster.fomm_pitch, 
            self.bass_cluster.fomm_beats, 
            self.treb_cluster.fomm_pitch, 
            self.treb_cluster.fomm_beats,
            bass_sample,
            treb_sample,
            bassdrum_sample,
            bdpitch,
            self.bassdrum_cluster.fomm_beats,
            snare_sample,
            snpitch,
            self.snare_cluster.fomm_beats
            )

        return linkage

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
    main(argv[1:] or glob('SimpleMods/*.mod'))
