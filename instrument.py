import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import math
from math import sin, pi, log
from random import randint
from collections import defaultdict


FREQ2MIDI = {
    65.4: 0, 69.3: 1, 73.4: 2, 77.8: 3, 82.4: 4, 87.3: 5,
    92.5: 6, 98.0: 7, 103.8: 8, 110.0: 9, 116.5: 10, 123.5: 11,
    130.8: 12, 138.6: 13, 146.8: 14, 155.6: 15, 164.8: 16, 174.6: 17,
    185.0: 18, 196.0: 19, 207.7: 20, 220.0: 21, 233.1: 22, 246.9: 23,
    261.6: 24, 277.2: 25, 293.7: 26, 311.1: 27, 329.6: 28, 349.2: 29,
    370.0: 30, 392.0: 31, 415.3: 32, 440.0: 33, 466.2: 34, 493.9: 35,
    523.3: 36, 554.4: 37, 587.3: 38, 622.3: 39, 659.3: 40, 698.5: 41,
    740.0: 42, 784.0: 43, 830.6: 44, 880.0: 45, 932.3: 46, 987.8: 47,
    1046.5: 48, 1108.7: 49, 1174.7: 50, 1244.5: 51, 1318.5: 52, 1396.9: 53,
    1480.0: 54, 1568.0: 55, 1661.2: 56, 1760.0: 57, 1864.7: 58, 1975.5: 59 }


freq_array = [130.8, 261.6, 392.0, 138.6, 523.3, 784.0, 146.8, 659.3, 622.3, 1046.5, 155.6, 329.6, 415.3, 1568.0, 164.8, 293.7, 1318.5, 220.0, 554.4, 174.6, 466.2, 1864.7, 1975.5, 311.1, 440.0, 185.0, 698.5, 830.6, 65.4, 196.0, 69.3, 1244.5, 1480.0, 73.4, 587.3, 77.8, 207.7, 82.4, 1108.7, 87.3, 932.3, 987.8, 92.5, 349.2, 1760.0, 98.0, 740.0, 103.8, 233.1, 493.9, 110.0, 1396.9, 880.0, 370.0, 116.5, 246.9, 1174.7, 123.5, 1661.2, 277.2]

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

    def find_nearest(value):
        idx = (np.abs(freq_array-value)).argmin()
        return array[idx]

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

        lo_std_freq = min(freq_array)
        hi_std_freq = max(freq_array)
        print(str(lo_std_freq) + ", " + str(hi_std_freq))

        normalized_freq = freq_in_hertz

        while normalized_freq < lo_std_freq:
            normalized_freq *= 2

        while normalized_freq > hi_std_freq:
            normalized_freq /= 2

        print("normalized_freq: " + str(normalized_freq))

        idx = (np.abs(freq_array-normalized_freq)).argmin()
        std_freq =  freq_array[idx]     
        print("std freq: " + str(std_freq)) 

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

# Instrument.analyze_pitch()