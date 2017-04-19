import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import math
from math import sin, pi, log
from random import randint
from collections import defaultdict


class Instrument:

    BEATS = 16  # Length of beat sequences to track (max 64)

    def __init__(self, sample):
        self.sample = sample
        self.base_freq = 0
        self.notes = []
        self.pitches = defaultdict(int)
        self.beats = defaultdict(int)
        self.effects = defaultdict(int)
        self.counts_pitch = defaultdict(lambda: defaultdict(int))
        self.counts_beats = np.zeros((self.BEATS, self.BEATS))
        self.melodic = None
        self.related = []
        self.last_pos, self.last_note = 0, None

        # Adam's added code
        self.unique_pitches = 0
        self.beat_occurrences = 0
        self.snr = 0
        self.principle_freq = 0

    def add_note(self, note, pos):
        # Record data
        self.notes += [(pos, note)]
        self.pitches[note.pitch] += 1
        self.beats[pos] += 1
        self.effects[note.effect] += 1

        # Populate first-order Markov Models
        self.counts_pitch[self.last_note][note.pitch] += 1
        self.counts_beats[self.last_pos][pos%self.BEATS] += 1
        self.last_note = note.pitch
        self.last_pos = pos % self.BEATS

    def fomm_pitch(self):
        pitches = list(self.pitches)
        arrayed = np.array([[self.counts_pitch[p1][p2] for p2 in pitches]
                            for p1 in pitches])
        return pitches, arrayed / np.sum(arrayed, axis=1)[:, np.newaxis]

    def fomm_beats(self):
        normed = self.counts_beats.copy()
        sums = np.sum(normed, axis=1)
        zeros = np.where(sums == 0.0)
        nonzs = np.where(sums != 0.0)
        normed[zeros,0] = 1.0
        normed[nonzs,:] /= sums[nonzs,np.newaxis]
        return normed

    def analyze_pitch(self):
        if not self.sample or not self.sample._wave:
           raise Exception('No wave to analyze')

        myWave = [100 * sin(2*pi*n/32) for n in range(32)]
        myWave = np.array(myWave)

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

        spectrum = np.fft.fft(myWave)
        freqs = np.fft.fftfreq(len(spectrum))

        idx = np.argmax(np.abs(spectrum))
        freq = freqs[idx]
        sample_rate = 100 # TODO
        freq_in_hertz = abs(freq * sample_rate)
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

        snr = P_s / P_n
        print("snr: " + str(snr))

        # Signal to noise ratio defined as mean / std deviation # of original signal, not the fft.............
        # snr = np.mean(myWave)/np.std(noise_list)
        # print(snr)

        # Then save another parameter that's something like the magnitude
        # of the dominant pitch fft[dom_freq_dex] divided by the mean of
        # the rest of it or something, so that a bass drum with a strong
        # but not tonal peak will be distinct from a bass guitar with the
        # same peak location and magnitude (but more prominent, higher SNR)
        # raise NotImplementedError('Still have to write analyze_pitch')

        self.principle_freq = freq_in_hertz
        self.snr = snr
        
    def get_distinct_beat(self):
        self.beat_occurrences = len(self.beats)

    def get_pitch_variance(self):
        self.unique_pitches = len(self.pitches)

Instrument.analyze_pitch()