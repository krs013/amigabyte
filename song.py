from os.path import expanduser
from itertools import chain
from sample import Sample
from pattern import Pattern
from instrument import Instrument


class Song:

    def __init__(self, *, name='untitled', filename=None):
        self.name = name
        self.vanity = ''
        self.samples = []
        self.patterns = []
        self.positions = []
        self.mk = b'M.K.'
        if filename:
            self.read_file(filename)
        
    def read_file(self, filename):
        with open(expanduser(filename), 'rb') as file:
            data = file.read()
            self.read_bytes(data)

    def read_bytes(self, data):
        self.name = data[0:20].rstrip(b'\0').decode()
        for offset in range(20, 950, 30):
            sample = Sample(data[offset:offset+30])
            if sample:
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
        for sample in self.samples:
            dex2 = dex + sample.length
            sample.wave = data[dex:dex2]
            dex = dex2

    def to_bytes(self):
        name = self.name.encode().ljust(20, b'\0')
        samples = b''.join(sample.to_bytes() for sample in self.samples)
        positions = bytes([len(self.positions), 127] +
                          self.positions).ljust(130, b'\0') + self.mk
        # Note: if a pattern was removed from positions, it can't be here!
        patterns = b''.join(pattern.to_bytes() for pattern in self.patterns)
        waves = b''.join(sample.wave_bytes for sample in self.samples)
        return name + samples + positions + patterns + waves

    def write_file(self, filename=None):
        if not filename:
            filename = '~/Desktop/' + self.name + '.mod'
        with open(expanduser(filename), 'wb') as file:
            file.write(self.to_bytes())
    
    def instruments(self):
        instruments = [None] + [Instrument(sample) for sample in self.samples]
        for pattern in self.patterns:
            for pos, note in pattern.enumerate_notes():
                if note.sample:  # Filter out 0's, but may be useful later
                    instruments[note.sample].add_note(note, pos)
        return instruments

    def arranged_patterns(self):
        return (self.patterns[n] for n in self.positions)
    
    def vector(self):
        return chain(*(pattern.vector(n) for n, pattern in
                     enumerate(self.arranged_patterns())))


def copy_test(filename, outfile=None):
    Song(filename=filename).write_file(
        outfile if outfile else filename.split('.')[-2] + '-copy.mod')


if __name__ == '__main__':
    import sys
    copy_test(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
