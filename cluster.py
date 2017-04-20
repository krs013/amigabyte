import numpy as np
from random import choice
from tables import *


class Cluster:

    def __init__(self, instruments, seed, cluster):

        self.instruments = [instruments[int(c)] for c in cluster]
        self.seed = cluster.index(seed)
        self._sample = self.seed  # Change to sample randomly
        self._fomm_pitch = None
        self._fomm_beats = None
        self._shifted_fomm_pitch = None
        self._shifted_fomm_beats = None
        self.alignment = np.array(len(self.instruments), dtype=int)
        self.tonal = self.seed.unique_pitches > 1

    def combine(self):
        self._fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
        self._fomm_beats = np.zeros((16,)*2)

        for inst in self.instruments:
            correlation = np.correlate(
                self.instruments[self.seed].adjusted_pitch_probs,
                inst.adjusted_pitch_probs, 'same')
            alignment = np.argmax(correlation) - len(correlation)//2
            a, b = self.align_tables(self._fomm_pitch,
                                     inst.fomm_pitch(), alignment)
            a += b
            a, b = self.align_tables(self._fomm_beats,
                                     inst.fomm_beats(), alignment)
            a += b
            self.alignment[inst] = alignment
            
        # Normalize
        sums = np.sum(self.fomm_pitch, 1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        self.fomm_pitch[nonzs,:] /= sums[nonzs,np.newaxis]
        self.fomm_pitch[zeros,:] = 1.0/self.fomm_pitch.shape[1]

        sums = np.sum(self.fomm_beats, 1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        self.fomm_beats[nonzs,:] /= self.sums[nonzs,np.newaxis]
        self.fomm_beats[zeros,0] = 1.0

    @staticmethod
    def align_tables(t1, t2, ofst):
        if ofst == 0:
            return t1, t2
        elif ofst < 0:
            return t1[:ofst,:ofst], t2[-ofst:,-ofst:]
        elif ofst > 0:
            return t1[ofst:,ofst:], t2[:-ofst,:-ofst]
        else:
            raise ValueError('wtf')

    @property
    def sample(self):
        if self._sample is None:
            self.new_sample()
        return self._sample

    def new_sample(self):
        self._sample = choice(range(len(self.instruments)))
        self._shifted_fomm_pitch = None
        self._shifted_fomm_beats = None
        
    @property
    def fomm_pitch(self):
        if self._fomm_pitch is None:
            self.combine()
        if self._shifted_fomm_pitch is None:
            self._shifted_fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
            a, b = self.align_tables(self._fomm_pitch,
                                     self._shifted_fomm_pitch,
                                     self.alignment[self._sample])
            b = a
        return self._shifted_fomm_pitch
        
    @property
    def fomm_beats(self):
        if self._fomm_beats is None:
            self.combine()
        if self._shifted_fomm_beats is None:
            self._shifted_fomm_beats = np.zeros((len(PITCH_LIST),)*2)
            a, b = self.align_tables(self._fomm_pitch,
                                     self._shifted_fomm_pitch,
                                     self.alignment[self._sample])
            b = a
        return self._shifted_fomm_beats
