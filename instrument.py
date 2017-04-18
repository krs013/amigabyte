import numpy as np
from collections import defaultdict


class Instrument:

    BEATS = 16  # Length of beat sequences to track (max 64)

    def __init__(self, sample):
        self.sample = sample
        self.base_freq = 0
        self.notes = [(-1, None)]  # Not a fan of -1...
        self.pitches = defaultdict(int)
        self.beats = defaultdict(int)
        self.effects = defaultdict(int)
        self.counts_pitch = defaultdict(lambda: defaultdict(int))
        self.counts_beats = np.zeros((self.BEATS, self.BEATS))
        self.melodic = None
        self.related = []
        self.last_pos, self.last_note = self.notes[0]

    def add_note(self, note, pos):
        # Record data
        self.notes += [(pos, note)]
        self.pitches[note.pitch] += 1
        self.beats[pos] += 1
        self.effects[note.effect] += 1

        # Populate first-order Markov Models
        self.counts_pitch[self.last_note][note.pitch] += 1
        self.counts_beats[self.last_pos+1][pos%self.BEATS] += 1
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
        raise NotImplementedError('Still have to write analyze_pitch')
        
