import numpy as np
from random import choice
from tables import *


class Cluster:

    def __init__(self, instruments, seed, cluster):

        self.instruments = [instruments[c] for c in cluster]
        self.seed = instruments[seed]
        self._sample = None
        self._fomm_pitch = None
        self._fomm_beats = None
        self._shifted_fomm_pitch = None
        self._shifted_fomm_beats = None
        self.alignment = np.zeros(len(self.instruments))
        self.tonal = self.seed.unique_pitches > 1

    def combine(self):
        self._fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
        self._fomm_beats = np.zeros((len(PITCH_LIST),)*2)

        for n, inst in enumerate(self.instruments):
            correlation = np.correlate(seed.adjusted_pitch_probs,
                                       inst.adjusted_pitch_probs, 'same')
            alignment = np.argmax(correlation) - len(correlation)//2
            a, b = align_tables(self._fomm_pitch,
                                instrument.fomm_pitch(), alignment)
            a += b
            a, b = align_tables(self._fomm_beats,
                                instrument.fomm_beats(), alignment)
            a += b
            self.alignment[n] = alignment
            
        # Normalize
        sums = np.sum(self.fomm_pitch, 1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        self.fomm_pitch[nonzs,:] /= self.sums[nonzs,np.newaxis]
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
        if not self._sample:
            self.new_sample()
        return self._sample

    def new_sample(self):
        self._shifted_fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
        self._shifted_fomm_beats = np.zeros((len(PITCH_LIST),)*2)
        n = choice(range(len(self.instruments)))
        self._sample = self.instruments[n]
        a, b = self.align_tables(self._fomm_pitch, self._shifted_fomm_pitch,
                                 self.alignment[n])
        b = a
        a, b = self.align_tables(self._fomm_pitch, self._shifted_fomm_pitch,
                                 self.alignment[n])
        b = a
        
    @property
    def fomm_pitch(self):
        if not self._fomm_pitch:
            self.combine()
        if not self._shifted_fomm_pitch:
            self.new_sample()
        return self._shifted_fomm_pitch
        
    @property
    def fomm_beats(self):
        if not self._fomm_beats:
            self.combine()
        if not self._shifted_fomm_beats:
            self.new_sample()
        return self._shifted_fomm_beats
