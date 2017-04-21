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
        self._pitch_probs = None
        self._shifted_fomm_pitch = None
        self._shifted_fomm_beats = None
        self.alignment = np.zeros(len(self.instruments), dtype=int)
        self.tonal = self.instruments[self.seed].unique_pitches > 1

    def combine(self):
        self._fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
        self._fomm_beats = np.zeros((BEATS_WINDOW+1,)*2)

        for n, inst in enumerate(self.instruments):
            correlation = np.correlate(
                self.instruments[self.seed].adjusted_pitch_probs,
                inst.adjusted_pitch_probs, 'same')
            alignment = np.argmax(correlation) - len(correlation)//2
            a, b = self.align_slices(alignment)
            self._fomm_pitch[a,a] += inst.fomm_pitch()[b,b]
            self._fomm_beats[a,a] += inst.fomm_beats()[b,b]
            self.alignment[n] = alignment
            
        # Normalize
        sums = np.sum(self.fomm_pitch, 1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        self.fomm_pitch[nonzs,:] /= sums[nonzs,np.newaxis]
        self.fomm_pitch[zeros,:] = self.pitch_probs

        sums = np.sum(self.fomm_beats, 1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        self.fomm_beats[nonzs,:] /= sums[nonzs,np.newaxis]
        self.fomm_beats[zeros,-1] = 1.0

    @staticmethod
    def align_slices(offset):
        if offset == 0:
            return slice(None), slice(None)
        elif offset < 0:
            return slice(None, offset), slice(-offset, None)
        elif offset > 0:
            return slice(offset, None), slice(None, -offset)
        else:
            raise ValueError('wtf')

    @property
    def sample(self):
        if self._sample is None:
            self.new_sample()
        return self.instruments[self._sample]

    def new_sample(self):
        self._sample = choice(range(len(self.instruments)))
        self._shifted_fomm_pitch = None
        self._shifted_fomm_beats = None
        self._pitch_probs = None
        
    @property
    def fomm_pitch(self):
        if self._fomm_pitch is None:
            self.combine()
        if self._shifted_fomm_pitch is None:
            self._shifted_fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
            a, b = self.align_slices(self.alignment[self._sample])
            self._shifted_fomm_pitch[b,b] = self._fomm_pitch[a,a]
        return self._shifted_fomm_pitch
        
    @property
    def fomm_beats(self):
        if self._fomm_beats is None:
            self.combine()
        if self._shifted_fomm_beats is None:
            self._shifted_fomm_beats = np.zeros((BEATS_WINDOW+1,)*2)
            a, b = self.align_slices(self.alignment[self._sample])
            self._shifted_fomm_beats[b,b] = self._fomm_beats[a,a]
        return self._shifted_fomm_beats

    @property
    def pitch_probs(self):
        if self._pitch_probs is None:
            self._pitch_probs = np.zeros(len(PITCH_LIST))
            for n, inst in enumerate(self.instruments):
                a, b = self.align_slices(self.alignment[n])
                self._pitch_probs[a] += inst.pitch_probs[b]
            self._pitch_probs /= np.sum(self._pitch_probs)
        return self._pitch_probs
