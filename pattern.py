from struct import pack
from itertools import chain
from operator import itemgetter


class Pattern(tuple):
    """Amiga module file pattern--64 notes across 4 channels"""

    def __new__(self, bytes=None):
        return tuple.__new__(Pattern, (tuple(Note() for _ in [0]*64)
                                       for _ in [0]*4))
                             
    def __init__(self, bytes=None):
        if bytes:
            self.read_bytes(bytes)

    def read_bytes(self, bytes):
        map(lambda note: note.clear(), self.channel1)
        map(lambda note: note.clear(), self.channel2)
        map(lambda note: note.clear(), self.channel3)
        map(lambda note: note.clear(), self.channel4)

        for n, offset in enumerate(range(0, 1024, 16)):
            self.channel1[n].read_bytes(bytes[offset:offset+4])
            self.channel2[n].read_bytes(bytes[offset+4:offset+8])
            self.channel3[n].read_bytes(bytes[offset+8:offset+12])
            self.channel4[n].read_bytes(bytes[offset+12:offset+16])

    def to_bytes(self):
        return bytes(chain(zip(
            *((n.to_bytes() for n in channel) for channel in
              [self.channel1, self.channel2, self.channel3, self.channel4]))))
                               

class Note:
    """Note entry in Amiga module file patterns"""

    # Sample frequences were based on horizontal scan frequencies
    PAL = 3579545.25
    NTSC = 3546894.6

    def __init__(self):
        self.sample = 0
        self._period = 0
        self.effect = 0
        self._note = None

    def read_bytes(self, bytes):
        self.sample = (0xf0 & bytes[0]) + ((0xf0 & bytes[2]) >> 4)
        self.period = ((0x0f & bytes[0]) << 8) + bytes[1]  # Property
        self.effect = (0x0f & bytes[2], bytes[3])

    def to_bytes(self):
        return pack('BBBB',
                    (0xf0 & self.sample) + (0x0f & self.period >> 8),
                    0xff & self.period,
                    (0xf0 & self.sample << 4) + self.effect[0],
                    self.effect[1])
        
    @property
    def rate(self):
        return Note.PAL / self._period if self._period > 0 else 0

    @property
    def period(self):
        return self._period
    
    @property
    def note(self):
        return self._note

    NOTES = {
        1712: 'C-0', 856: 'C-1', 428: 'C-2', 214: 'C-3', 107: 'C-4',
        1616: 'C#0', 808: 'C#1', 404: 'C#2', 202: 'C#3', 101: 'C#4',
        1525: 'D-0', 762: 'D-1', 381: 'D-2', 190: 'D-3', 95: 'D-4',
        1440: 'D#0', 720: 'D#1', 360: 'D#2', 180: 'D#3', 90: 'D#4',
        1357: 'E-0', 678: 'E-1', 339: 'E-2', 170: 'E-3', 85: 'E-4',
        1281: 'F-0', 640: 'F-1', 320: 'F-2', 160: 'F-3', 80: 'F-4',
        1209: 'F#0', 604: 'F#1', 302: 'F#2', 151: 'F#3', 76: 'F#4',
        1141: 'G-0', 570: 'G-1', 285: 'G-2', 143: 'G-3', 71: 'G-4',
        1077: 'G#0', 538: 'G#1', 269: 'G#2', 135: 'G#3', 67: 'G#4',
        1017: 'A-0', 508: 'A-1', 254: 'A-2', 127: 'A-3', 64: 'A-4',
        961: 'A#0', 480: 'A#1', 240: 'A#2', 120: 'A#3', 60: 'A#4',
        907: 'B-0', 453: 'B-1', 226: 'B-2', 113: 'B-3', 57: 'B-4'}

    PERIODS = {v: k for k, v in Note.NOTES.items()}
              
    @period.setter
    def period(self, period):
        self._period = period
        self._note = Note.NOTES[period]
                  
    @note.setter
    def note(self, note):
        self._note = note
        self._period = Note.PERIODS[note]

                  
