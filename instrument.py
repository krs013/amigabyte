import numpy as np
from collections import defaultdict


class Instrument:

    BEATS = 16  # Length of beat sequences to track (max 64)

    def __init__(self, sample):
        self.sample = sample
        self.base_freq = 0
        self.notes = []
        self.pitches = defaultdict(int)
        self.beats = defaultdict(int)
        self.effects = defaultdict(int)
        self.counts_pitch = defaultdict(lambda: defaultdict(int))
        self.counts_beats = np.zeros((self.BEATS, self.BEATS))
        self.melodic = None
        self.related = []
        self.last_pos, self.last_note = 0, None

    def add_note(self, note, pos):
        # Record data
        self.notes += [(pos, note)]
        self.pitches[note.pitch] += 1
        self.beats[pos] += 1
        self.effects[note.effect] += 1

        # Populate first-order Markov Models
        self.counts_pitch[self.last_note][note.pitch] += 1
        self.counts_beats[self.last_pos][pos%self.BEATS] += 1
        self.last_note = note.pitch
        self.last_pos = pos % self.BEATS

    def fomm_pitch(self):
        pitches = list(self.pitches)
        arrayed = np.array([[self.counts_pitch[p1][p2] for p2 in pitches]
                            for p1 in pitches])
        return pitches, arrayed / np.sum(arrayed, axis=1)[:, np.newaxis]

    def fomm_beats(self):
        normed = self.counts_beats.copy()
        sums = np.sum(normed, axis=1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        normed[zeros,0] = 1.0
        normed[nonzs,:] /= sums[nonzs,np.newaxis]
        return normed

    def analyze_pitch(self):
        if not self.sample or not self.sample._wave:
            raise Exception('No wave to analyze')
        fft = np.fft.rfft(self.wave)
        np.abs(fft, fft)
        np.square(fft, fft)
        np.log(fft, fft)
        dom_freq_dex = np.argmax(fft)
        # Still needs interpretation, check for off-key notes, and turn
        # this into something that can tell us basically what octave
        # the instrument is in.

        # Then save another parameter that's something like the magnitude
        # of the dominant pitch fft[dom_freq_dex] divided by the mean of
        # the rest of it or something, so that a bass drum with a strong
        # but not tonal peak will be distinct from a bass guitar with the
        # same peak location and magnitude (but more prominent, higher SNR)
        raise NotImplementedError('Still have to write analyze_pitch')
        
