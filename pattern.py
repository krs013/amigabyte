from struct import pack
from itertools import chain
from operator import itemgetter


class Pattern:
    """Amiga module file pattern--64 notes across 4 channels"""

    NCHANNELS = 4
    
    def __init__(self, data=None):
        self._channels = [Channel() for _ in [0]*Pattern.NCHANNELS]
        if data:
            self.read_bytes(data)

    def __len__(self):
        return Pattern.NCHANNELS

    def __getitem__(self, key):
        if type(key) not in [int, slice]:
            raise TypeError
        return self._channels[key]

    def __iter__(self):
        return iter(self._channels)

    def read_bytes(self, data):
        notes = [data[dex:dex+4] for dex in range(0, 1024, 4)]
        for n, channel in enumerate(self._channels):
            channel.read_bytes(notes[n::4])

    def to_bytes(self):
        return b''.join(chain(*zip(*(chan.to_bytes() for chan in
                                     self._channels))))

    def enumerate_notes(self):
        return ((pos, note) for channel in self._channels
                for pos, note in enumerate(channel) if note)


class Channel:
    """Channel in pattern--64 notes"""

    NNOTES = 64

    def __init__(self):
        self._notes = [None]*Channel.NNOTES

    def __len__(self):
        return Pattern.NNOTES

    def __getitem__(self, key):
        if type(key) not in [int, slice]:
            raise TypeError
        return self._notes[key]

    def __setitem__(self, key, value):
        if type(key) is int:
            if type(value) in [NoneType, Note]:
                self._notes[key] = value
            elif type(value) in [bytes, bytearray]:
                self._notes[key] = Note(value)
            else:
                raise TypeError('value must be of type bytes, ' +
                                'bytearray, Note, or None, not ' +
                                '{}'.format(str(type(value))))
        elif type(key) is slice:
            for k, v in zip(range(*key.indices(len(value))), value):
                self.__setitem__(k, v)
        else:
            raise TypeError        

    def __iter__(self):
        return iter(self._notes)

    def __bool__(self):
        return any(self._notes)

    def read_bytes(self, data):
        for n, datum in enumerate(data):
            if any(datum):
                self._notes[n] = Note(datum)
            else:
                self._notes[n] = None

    def to_bytes(self):
        return (note.to_bytes() if note else b'\0\0\0\0' for note in self)


class Note:
    """Note entry in Amiga module file patterns"""

    # There may be many copies, so restrict variables
    __slots__ = ('sample', '_pitch', 'effect', '_period')

    # Sample frequences were based on horizontal scan frequencies
    PAL = 3579545.25
    NTSC = 3546894.6

    def __init__(self, data=None):
        self.sample = 0
        self._period = 0
        self.effect = 0
        self._pitch = None
        if data:
            self.read_bytes(data)

    def __bool__(self):
        return any((self.sample, self._period, *self.effect))

    def read_bytes(self, data):
        self.sample = (0xf0 & data[0]) + ((0xf0 & data[2]) >> 4)
        self.period = ((0x0f & data[0]) << 8) + data[1]  # Property
        self.effect = (0x0f & data[2], data[3])

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
    def pitch(self):
        return self._pitch
              
    @period.setter
    def period(self, period):
        self._period = period
        self._pitch = Note.PITCHES[period] if period else None
                  
    @pitch.setter
    def pitch(self, pitch):
        self._pitch = pitch
        self._period = Note.PERIODS[pitch] if pitch else 0

    PITCHES = {
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

    PERIODS = {v: k for k, v in PITCHES.items()}
