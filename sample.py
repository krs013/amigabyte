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
        self.repeat = (2 * int.from_bytes(bytes[26:28], 'big'),
                       2 * int.from_bytes(bytes[28:30], 'big'))
        self._wave = None

    @property
    def wave(self):
        return self._wave

    @wave.setter
    def wave(self, value):
        self._wave = [x-256 if x > 127 else x for x in value]
