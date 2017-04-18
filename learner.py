import numpy as np
from os import path
from sys import stderr
from song import Song
from instrument import Instrument


class Learner:

    def __init__(self, files=[]):
        self.pending = [path.abspath(f) for f in files]
        self.prefix = path.commonprefix(self.pending) or path.abspath('.')
        self.learned = []

    def analyze(self, files=[]):
        self.pending.extend((path.relpath(f, self.prefix) for f in files))
        
        for f in self.pending:
            song = Song(filename=f)
            
