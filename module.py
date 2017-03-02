#!/usr/bin/env python3

import argparse
import sys
from pdb import set_trace


class Module:
    """Amiga mod file object"""

    def __init__(self, file):
        """Open and decode a .mod file"""
        self.bytes = file.read()
        file.close()

        self.name = self.bytes[0:20].rstrip(b'\x00').decode()
        
        self.samples = [None]
        self.vanity = ""
        for offset in range(20, 950, 30):
            sample = Sample(self.bytes[offset:offset+30])
            if sample.name:
                self.vanity += '\n' + sample.name
            if sample:
                self.samples.append(sample)

        self.length = int.from_bytes(self.bytes[950:951], 'big')
        self.pattern_positions = [byte for byte in self.bytes[952:1080]]
        self.mk = self.bytes[1080:1084]

        self.patterns = []
        self.num_patterns = max(self.pattern_positions) + 1
        for offset in range(1084, 1024 * self.num_patterns + 1084, 1024):
            self.patterns.append(Pattern(self.bytes[offset:offset+1024]))

        dex = 1024 * self.num_patterns + 1084
        for sample in self.samples:
            dex2 = dex + sample.length
            sample.wave = self.bytes[dex:dex2]
            dex = dex2

    def sample_style(self):
        for sample in self.samples:
            pass

            
class Sample:
    """Amiga mod sample object"""

    def __init__(self, bytes):
        self.bytes = bytes
        self.name = bytes[0:22].rstrip(b'\x00').decode()
        self.length = 2 * int.from_bytes(bytes[22:24], 'big')
        self.finetune = 0x0f & bytes[24]
        self.volume = (lambda x: x if x <= 64 else 64)(bytes[25])
        self.repeat_point = 2 * int.from_bytes(bytes[26:28], 'big')
        self.repeat_length = 2 * int.from_bytes(bytes[28:30], 'big')
        self._wave = None

    @property
    def wave(self):
        return self._wave

    @wave.setter
    def wave(self, value):
        self._wave = [x - 256 if x > 127 else x for x in value]

    def __bool__(self):
        return bool(self.length and self.volume)
    

class Pattern:
    """Amiga mod pattern object--a sequence of notes across 4 channels"""

    def __init__(self, bytes):
        self.channel1 = []
        self.channel2 = []
        self.channel3 = []
        self.channel4 = []
        
        for offset in range(0, 1024, 16):
            self.channel1.append(Note(bytes[offset:offset+4]))
            self.channel2.append(Note(bytes[offset+4:offset+8]))
            self.channel3.append(Note(bytes[offset+8:offset+12]))
            self.channel4.append(Note(bytes[offset+12:offset+16]))


class Note:
    """Note entries in Amiga mod patterns"""

    # Sample frequencies were based on horizontal scan frequencies in
    # Amiga
    PAL = 3579545.25
    NTSC = 3546894.6

    def __init__(self, bytes):
        self.bytes = bytes
        self.sample = (0xf0 & bytes[0]) + ((0xf0 & bytes[2]) >> 4)
        self.period = ((0x0f & bytes[0]) << 8) + bytes[1]
        self.effect = (0x0f & bytes[2], bytes[3])

        # Sample rate (based on PAL)
        self.rate = Note.PAL / self.period if self.period > 0 else 0

    @property
    def note(self):
        pass

        
def main():
    parser = argparse.ArgumentParser(description='Open a .mod file')
    parser.add_argument('file', type=argparse.FileType('rb'),
                        default=sys.stdin)
    args = parser.parse_args()
    mod = Module(args.file)
    set_trace()


if __name__ == '__main__':
    main()
