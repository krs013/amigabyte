from struct import pack

class Sample:

    def __init__(self, name='instrument'):
        self.name = name
        self._wave = None
        self.length = 0
        self.finetune = 0
        self.volume = 64
        self.repeat = (None, None)

    def read_bytes(self, bytes):
        name = bytes[0:22].rstrip(b'\x00').decode()
        if name:
            self.name = name
        self.length = 2 * int.from_bytes(bytes[22:24], 'big')
        self.finetune = 0x0f & bytes[24]
        self.volume = (lambda x: x if x <= 64 else 64)(bytes[25])
        self._repeat = (int.from_bytes(bytes[26:28], 'big'),
                        int.from_bytes(bytes[28:30], 'big'))
        self._wave = None
        # If these fields are manipulated, validate in setters

    def to_bytes(self):
        data = bytearray(30)
        data[:22] = self.name.rstrip()
        data[22:24] = int.to_bytes(self.length // 2, 2, 'big')
        data[24] = self.finetune
        data[25] = self.volume
        data[26:30] = pack('>HH', self.repeat[0] // 2, self.repeat[1] // 2)

    @property
    def repeat(self):
        return 2 * self._repeat[0], 2 * self._repeat[1]

    @property
    def repeat_point(self):
        return 2 * self._repeat[0]

    @repeat_point.setter
    def repeat_point(self, repeat_point):
        self._repeat[0] = repeat_point // 2

    @property
    def repeat_length(self):
        return 2 * self._repeat[1]

    @repeat_length.setter
    def repeat_length(self, repeat_length):
        self._repeat[1] = repeat_point // 2

    @property
    def wave(self):
        return self._wave

    @wave.setter
    def wave(self, value):
        if type(value) is bytes:
            self._wave = [x-256 if x > 127 else x for x in value]
        else:
            self._wave = map(lambda x: min(max(x, -128), 127), value)
