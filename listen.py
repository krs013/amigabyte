import pyaudio
from itertools import chain, islice
from sample import Sample
from pattern import Note


class Listen:
    """Hear a note--not ready for full songs... yet"""

    CHUNK = 1024
    
    def __init__(self, song=None, portaudio=None):
        self.song = song
        self.portaudio = portaudio or pyaudio.PyAudio()

    def play_note(self, note, sample=0, duration=2., *, song=None):
        if type(note) is str:
            note = Note(sample, note)
        if type(note.sample) is int:
            if song:
                sample = song.samples[sample]
            elif self.song:
                sample = self.song.samples[sample]
            else:
                raise Exception('No song to dereference sample index')
        if type(note.sample) is not Sample or not sample.length:
            raise Exception('Invalid sample')
        stream = self.portaudio.open(round(note.rate), 1, pyaudio.paInt8,
                                     output=True, frames_per_buffer=self.CHUNK)
        if sample.repeat_length:
            def frames():  # So... this is pretty inefficient...
                for byte in sample.wave_bytes:
                    yield byte
                rstart, rstop = sample.repeat
                rstop += rstart
                while True:
                    for byte in sample.wave_bytes[rstart:rstop]:
                        yield byte
        else:
            def frames():
                for byte in sample.wave_bytes:
                    yield byte
                raise StopIteration
        try:
            framegen = frames()
            for _ in range(round(note.rate*duration/self.CHUNK)):
                stream.write(b''+bytearray(islice(framegen, self.CHUNK)))
        except StopIteration:
            pass
        finally:
            stream.close()
            
