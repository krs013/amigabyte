import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import math
from math import sin, pi, log
from random import randint
from collections import defaultdict
from tables import *


class Instrument:

    BEATS = 16  # Length of beat sequences to track (max 64)
    PAL = 3579545.25

    def __init__(self, sample, song=None):
        self.sample = sample
        self.song = song
        self.notes = []
        self.pitches = defaultdict(int)
        self.beats = defaultdict(int)
        self.effects = defaultdict(int)
        self.counts_pitch = defaultdict(lambda: defaultdict(int))
        self.counts_beats = np.zeros((self.BEATS, self.BEATS))
        self.last_pos, self.last_note = 0, None

        self._snr = None
        self._std_freq = None
        self._rounded_pitch_num = None
        self._pitch_probs = None

    @property
    def vector(self):
        return (self.std_freq, self.snr,
                self.unique_pitches, self.beat_occurrences)

    @property
    def unique_pitches(self):
        return len(self.pitches)

    @property
    def beat_occurrences(self):
        return len(self.beats)
        
    @property
    def std_freq(self):
        if self._std_freq is None:
            self.analyze_pitch()
        return self._std_freq

    @property
    def snr(self):
        if self._snr is None:
            self.analyze_pitch()
        return self._snr

    @property
    def rounded_pitch_num(self):
        if self._rounded_pitch_num is None:
            pitch_sum = 0
            for key, value in self.pitches.items():
                pitch_sum += (value * NAMES2MIDI[key])
            avg_midi_pitch = pitch_sum/len(self.pitches)
            pitch_nums = list(range(60))
            idx = (np.abs(np.array(pitch_nums)-avg_midi_pitch)).argmin()
            self._rounded_pitch_num =  pitch_nums[idx]
        return self._rounded_pitch_num

    @property
    def pitch_probs(self):
        if self._pitch_probs is None:
            self._pitch_probs = np.array([self.pitches[p] for p in
                                          PITCH_LIST], dtype='float')
            self._pitch_probs /= np.sum(self._pitch_probs)
        return self._pitch_probs

    def add_note(self, note, pos):
        # Record data
        self.notes += [(pos, note)]
        self.pitches[note.pitch] += 1
        self.beats[pos%self.BEATS] += 1  # Or just %64?
        self.effects[note.effect] += 1

        # Populate first-order Markov Models
        self.counts_pitch[self.last_note][note.pitch] += 1
        self.counts_beats[self.last_pos][pos%self.BEATS] += 1
        self.last_note = note.pitch
        self.last_pos = pos % self.BEATS

    def fomm_pitch(self):
        arrayed = np.array([[self.counts_pitch[p1][p2] for p2 in PITCH_LIST]
                            for p1 in PITCH_LIST], dtype='float')
        sums = np.sum(arrayed, axis=1)
        nonzs = np.where(sums != 0.0)
        arrayed[nonzs,:] /= sums[nonzs, np.newaxis]
        return arrayed

    def fomm_beats(self):
        normed = self.counts_beats.copy()
        sums = np.sum(normed, axis=1)
        nonzs = np.where(sums != 0.0)
        # zeros = np.where(sums == 0.0)
        # normed[zeros,0] = 1.0
        # Commenting those out is dangerous, but otherwise combined tables
        # will have lots of bad data in them
        normed[nonzs,:] /= sums[nonzs,np.newaxis]
        return normed

    def find_nearest(value):
        idx = (np.abs(FREQ_ARRAY-value)).argmin()
        return array[idx]

    def analyze_pitch(self):
        if not self.sample or not self.sample._wave:
          raise Exception('No wave to analyze')

        #myWave = [100 * sin(2*pi*n/32) for n in range(32)]
        #myWave = np.array(myWave)

        # Test case for computing snr
        # myWave = [randint(0,100000) for n in range(100)]


        # fft = np.fft.rfft(myWave)
        # np.abs(fft, fft)
        # np.square(fft, fft)
        # np.log(fft, fft)
        # dom_freq_dex = np.argmax(fft)

        # Still needs interpretation, check for off-key notes, and turn
        # this into something that can tell us basically what octave
        # the instrument is in.

        spectrum = np.fft.fft(self.sample.repeated)
        freqs = np.fft.fftfreq(len(spectrum))

        idx = np.argmax(np.abs(spectrum))
        freq = freqs[idx]


      # return Note.PAL / self._period if self._period > 0 else 0

        period = MIDI2MODPITCHES[self.rounded_pitch_num]
        sample_rate = self.PAL / period

        freq_in_hertz = abs(freq * sample_rate)
        print("freq in hertz: " + str(freq_in_hertz))
        plt.plot(freqs, abs(spectrum))


        # Following what I read here: https://dsp.stackexchange.com/questions/14862/measure-the-snr-of-a-signal-in-the-frequency-domain
        # And here: https://en.wikipedia.org/wiki/Signal-to-noise_ratio#Definition

        abs_spectrum = abs(spectrum)


        max_power = 0
        for i in range(1,math.floor(len(abs_spectrum)/2)):
            if abs_spectrum[i] > max_power:
                max_power = abs_spectrum[i]

        P_n = 0
        for i in range(1,math.floor(len(abs_spectrum)/2)):
            if (abs_spectrum[i] < max_power/2):
                P_n += abs_spectrum[i] * abs_spectrum[i]
        P_n /= len(abs_spectrum)

        P_s = 0
        for i in range(1,math.floor(len(abs_spectrum)/2)):
            if (abs_spectrum[i] > max_power/2):
                P_s += abs_spectrum[i] * abs_spectrum[i]
        P_s /= len(abs_spectrum)

        snr_db = 20 * log(P_s / P_n, 10)
        print("snr_db: " + str(snr_db))

        # Find the nearest standard frequency

        lo_std_freq = min(FREQ_ARRAY)
        hi_std_freq = max(FREQ_ARRAY)
        print(str(lo_std_freq) + ", " + str(hi_std_freq))

        normalized_freq = freq_in_hertz

        while normalized_freq < lo_std_freq:
            normalized_freq *= 2

        while normalized_freq > hi_std_freq:
            normalized_freq /= 2

        print("normalized_freq: " + str(normalized_freq))

        idx = (np.abs(FREQ_ARRAY-normalized_freq)).argmin()
        std_freq =  FREQ_ARRAY[idx]     
        print("std freq: " + str(std_freq)) 

        # Then save another parameter that's something like the magnitude
        # of the dominant pitch fft[dom_freq_dex] divided by the mean of
        # the rest of it or something, so that a bass drum with a strong
        # but not tonal peak will be distinct from a bass guitar with the
        # same peak location and magnitude (but more prominent, higher SNR)
        # raise NotImplementedError('Still have to write analyze_pitch')

        #self.principle_freq = freq_in_hertz
        self._snr = snr_db
        self._std_freq = std_freq

        
# Instrument.analyze_pitch()
