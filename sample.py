from struct import pack


class Sample:

    def __init__(self, data=None, *, name=''):
        self.name = name
        self._wave = None
        self._length = 0
        self.finetune = 0
        self.volume = 64
        self._repeat = (0, 0)
        if data:
            self.read_bytes(data)

    def read_bytes(self, data):
        try:
            name = data[:22].rstrip(b'\x00').decode()
        except UnicodeDecodeError:
            name = 'invalid'
        if name:
            self.name = name
        self._length = int.from_bytes(data[22:24], 'big')
        self.finetune = 0x0f & data[24]
        self.volume = (lambda x: x if x <= 64 else 64)(data[25])
        self._repeat = (int.from_bytes(data[26:28], 'big'),
                        int.from_bytes(data[28:30], 'big'))
        self._wave = None

    def to_bytes(self):
        data = bytearray(30)
        data[:22] = self.name.encode().ljust(22, b'\0')
        data[22:24] = int.to_bytes(self.length // 2, 2, 'big')
        data[24] = self.finetune
        data[25] = self.volume
        data[26:30] = pack('>HH', *self._repeat)
        return data

    @property
    def length(self):
        return 2 * self._length

    @property
    def repeat(self):
        return self.repeat_point, self.repeat_length

    @repeat.setter
    def repeat(self, repeat):
        if type(repeat) is not tuple:
            raise TypeError
        elif len(repeat) != 2:
            raise ValueError
        self.repeat_point, self.repeat_length = repeat

    @property
    def repeat_point(self):
        return 2 * self._repeat[0]

    @repeat_point.setter
    def repeat_point(self, repeat_point):
        self._repeat = (repeat_point // 2, self._repeat[1])

    @property
    def repeat_length(self):
        return 2 * self._repeat[1] if self._repeat[1] > 1 else 0

    @repeat_length.setter
    def repeat_length(self, repeat_length):
        self._repeat = (self._repeat[0], repeat_length // 2)

    @property
    def repeated(self):
        return self._wave[self.repeat_point:
                          self.repeat_point+self.repeat_length]

    @property
    def wave(self):
        if self._wave:
            return self._wave[2:]  # Repeat/null junk at beginning?
        else:
            return []

    @wave.setter
    def wave(self, value):
        if type(value) is bytes:  # Needs to start with 00
            self._wave = [x-256 if x > 127 else x for x in value]
        else:
            self._wave = [0, 0]  # Weird repeat stuff?
            self._wave.extend(map(lambda x: min(max(int(x), -128), 127),
                                  value))
            self._wave += [0] if len(self._wave) % 2 else []  # Even length
            self._length = len(self._wave) // 2
            self.repeat = (2, len(value))

    @property
    def wave_bytes(self):
        return bytes(x+256 if x<0 else x for x in self._wave)

    @property
    def repeated_bytes(self):
        return bytes(x+256 if x<0 else x for x in self.repeated)

    def __bool__(self):
        return bool(self.wave) and self.length>1 and bool(self.volume)
