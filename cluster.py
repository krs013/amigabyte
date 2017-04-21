import numpy as np
from random import choice
from tables import *


class Cluster:

    def __init__(self, instruments, seed, cluster):

        self.instruments = [instruments[int(c)] for c in cluster]
        self.dex_map = {int(v): n for n, v in enumerate(cluster)}
        self.seed = cluster.index(seed)
        self._sample = None #self.seed  # Change to sample randomly
        self._fomm_pitch = None
        self._fomm_beats = None
        self._pitch_probs = None
        self._shifted_fomm_pitch = None
        self.alignment = np.zeros(len(self.instruments), dtype=int)
        self.tonal = self.instruments[self.seed].unique_pitches > 1

    def pitch_correlation(self, other, pairs):
        correlation = np.zeros((len(PITCH_LIST),)*2)
        for pair in pairs:
            dex1 = self.dex_map[pair[0]]
            dex2 = other.dex_map[pair[1]]
            song = self.instruments[dex1].song
            if not song == other.instruments[dex2].song:
                raise Exception('Songs don\'t match')
            sdex1 = self.instruments[dex1].notes[0][1].sample
            sdex2 = other.instruments[dex2].notes[0][1].sample
            a, b = self.align_slices(self.alignment[dex1])
            c, d = other.align_slices(other.alignment[dex2])
            correlation[a,c] += song.pitch_correlation(sdex2, sdex1)[b,d]
        sums = np.sum(correlation, 1)
        zeros = np.where(sums == 0)
        nonzs = np.where(sums != 0)
        correlation[nonzs,:] /= sums[nonzs,np.newaxis]
        correlation[zeros,:] = 1.0/correlation.shape[1]
        return correlation

    def beats_correlation(self, other, pairs):
        correlation = np.zeros((BEATS_WINDOW,)*2)
        for pair in pairs:
            dex1 = self.dex_map[pair[0]]
            dex2 = other.dex_map[pair[1]]
            song = self.instruments[dex1].song
            if not song == other.instruments[dex2].song:
                raise Exception('Songs don\'t match')
            sdex1 = self.instruments[dex1].notes[0][1].sample
            sdex2 = other.instruments[dex2].notes[0][1].sample
            correlation += song.beats_correlation(sdex2, sdex1)
        sums = np.sum(correlation, 1)
        zeros = np.where(sums == 0)
        nonzs = np.where(sums != 0)
        correlation[nonzs,:] /= sums[nonzs,np.newaxis]
        correlation[zeros,:] = 1.0/correlation.shape[1]
        return correlation

    def combine(self):
        self._fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
        self._fomm_beats = np.zeros((BEATS_WINDOW+1,)*2)
        arrayprint = lambda x: print('\n'.join(('{:4.2f} '*len(y)).format(
            *y) for y in x))

        for n, inst in enumerate(self.instruments):
            correlation = np.correlate(
                self.instruments[self.seed].adjusted_pitch_probs,
                inst.adjusted_pitch_probs, 'same')
            alignment = np.argmax(correlation) - len(correlation)//2
            a, b = self.align_slices(alignment)
            self._fomm_pitch[a,a] += inst.fomm_pitch()[b,b]
            self._fomm_beats += inst.fomm_beats()
            # arrayprint(inst.fomm_beats())
            # print('=========')
            # print()
            self.alignment[n] = alignment
            
        # Normalize
        for n in range(BEATS_WINDOW):
            self.fomm_beats[n,:n] = 0.0
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
        self._fomm_beats = None
        self._pitch_probs = None
        
    @property
    def fomm_pitch(self):
        if self._sample is None:
            self.new_sample()
        if self._fomm_pitch is None:
            self.combine()
        if self._shifted_fomm_pitch is None:
            self._shifted_fomm_pitch = np.zeros((len(PITCH_LIST),)*2)
            a, b = self.align_slices(self.alignment[self._sample])
            self._shifted_fomm_pitch[b,b] = self._fomm_pitch[a,a]
        return self._shifted_fomm_pitch
        
    @property
    def fomm_beats(self):
        if self._sample is None:
            self.new_sample()
        if self._fomm_beats is None:
            self.combine()
        return self._fomm_beats

    @property
    def pitch_probs(self):
        if self._pitch_probs is None:
            self._pitch_probs = np.zeros(len(PITCH_LIST))
            for n, inst in enumerate(self.instruments):
                a, b = self.align_slices(self.alignment[n])
                self._pitch_probs[a] += inst.pitch_probs[b]
            self._pitch_probs /= np.sum(self._pitch_probs)
        return self._pitch_probs
