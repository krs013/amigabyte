from collections import defaultdict
from sample import Sample


class Instrument:

    def __init__(self, sample):
        self.sample = sample
        self.base_freq = 0
        self.pitches = defaultdict(int)
        self.beats = defaultdict(int)
        self.effects = defaultdict(int)
        self.melodic = None
        self.related = []

    def add_note(self, note, pos):
        self.pitches[note.pitch] += 1
        self.beats[pos] += 1
        self.effects[note.effect] += 1
