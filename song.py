import weakref
import numpy as np
from os.path import expanduser
from itertools import chain, product
from sample import Sample
from pattern import Pattern
from instrument import Instrument


class Song:

    def __init__(self, *, name='untitled', filename=None):
        self.name = name
        self.vanity = ''
        self.samples = [None]
        self._instruments = None
        self.patterns = []
        self.positions = []
        self.mk = b'M.K.'
        if filename:
            self.read_file(filename)
        
    def read_file(self, filename):
        with open(expanduser(filename), 'rb') as file:
            data = file.read()
            self.read_bytes(data)
            self.fill_missing_samples()

    def read_bytes(self, data):
        self.name = data[0:20].rstrip(b'\0').decode()
        for offset in range(20, 950, 30):
            sample = Sample(data[offset:offset+30])
            self.samples.append(sample)
            if sample.name:
                self.vanity += '\n' + sample.name
        length = data[950]
        self.positions = [byte for byte in data[952:1080]][:length]
        self.mk = data[1080:1084]
        num_patterns = max(self.positions) + 1
        dex = 1024 * num_patterns + 1084
        for offset in range(1084, dex, 1024):
            self.patterns.append(Pattern(data[offset:offset+1024]))
        for sample in self.samples[1:]:
            dex2 = dex + sample.length
            sample.wave = data[dex:dex2]
            dex = dex2

    def to_bytes(self):
        name = self.name.encode().ljust(20, b'\0')
        samples = b''.join(sample.to_bytes() for sample in
                           self.samples[1:]).ljust(930, b'\0')
        positions = bytes([len(self.positions), 127] +
                          self.positions).ljust(130, b'\0') + self.mk
        # Note: if a pattern was removed from positions, it can't be here!
        patterns = b''.join(pattern.to_bytes() for pattern in self.patterns)
        waves = b''.join(sample.wave_bytes for sample in self.samples[1:])
        return name + samples + positions + patterns + waves

    def write_file(self, filename=None):
        if not filename:
            filename = '~/Desktop/' + self.name + '.mod'
        with open(expanduser(filename), 'wb') as file:
            file.write(self.to_bytes())
    
    def fill_missing_samples(self):
        carryovers = (0, 0, 0, 0)
        for p in self.arranged_patterns():
            carryovers = p.fill_missing_samples(carryovers)

    def arranged_patterns(self):
        return (self.patterns[n] for n in self.positions)
    
    def vector(self):
        return chain(*(pattern.vector(n) for n, pattern in
                     enumerate(self.arranged_patterns())))

    @property
    def instruments(self):
        if not self._instruments:
            self._instruments = [Instrument(sample, song=weakref.ref(self))
                                 if sample else None
                                 for sample in self.samples]
            for n, pattern in enumerate(self.arranged_patterns()):
                for pos, note in pattern.enumerate_notes(n):
                    if note.sample and self.samples[note.sample]:
                        self._instruments[note.sample].add_note(note, pos)
        return self._instruments

    def pitch_correlation(self, prob_dex, cond_dex):
        prob_pitches = list(self.instruments[prob_dex].pitches)
        cond_pitches = list(self.instruments[cond_dex].pitches)
        counts = {cp: {pp: 0 for pp in prob_pitches} for cp in cond_pitches}
        # Could add a None entry, but better to just use prior prob/nothing?
        prob_notes = [False]*4
        cond_notes = [False]*4
        for notes in chain(*(pattern.synchronous_notes() for pattern
                             in self.arranged_patterns())):
            for n, note in enumerate(notes):
                if note and note.sample:
                    prob_notes[n] = note.sample == prob_dex and note.pitch
                    cond_notes[n] = note.sample == cond_dex and note.pitch
            for cp, pp in product(filter(None, cond_notes),
                                filter(None, prob_notes)):
                counts[cp][pp] += 1
        arrayed = np.array([[counts[cp][pp] for pp in prob_pitches]
                            for cp in cond_pitches])
        return (prob_pitches, cond_pitches,
                arrayed / np.sum(arrayed, axis=1)[:,np.newaxis])
        
    def beats_correlation(self, prob_dex, cond_dex, size=16):
        counts = np.zeros((size, size))
        prob_beats = [False]*4
        cond_beats = [False]*4
        for pos, notes in enumerate(chain(*(pn.synchronous_notes() for
                                            pn in self.arranged_patterns()))):
            for n, note in enumerate(notes):
                if note and note.sample:
                    prob_beats[n] = note.sample == prob_dex and pos % size
                    cond_beats[n] = note.sample == cond_dex and pos % size
            for cp, pp in product(filter(None, cond_beats),
                                  filter(None, prob_beats)):
                counts[cp, pp] += 1
        sums = np.sum(counts, axis=1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        counts[zeros,:] = 1.0 / size  # No information, uniform probability
        counts[nonzs,:] /= sums[nonzs, np.newaxis]
        return counts

    
def copy_test(filename, outfile=None):
    Song(filename=filename).write_file(
        outfile if outfile else filename.split('.')[-2] + '-copy.mod')


def vector_test(filename, outfile=None):
    if not outfile:
        outfile = filename.split('.')[-2] + '.csv'

    with open(outfile, 'w') as out:
        for note in Song(filename=filename).vector():
            print(*note, sep=',', file=out)


if __name__ == '__main__':
    import sys
    copy_test(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
