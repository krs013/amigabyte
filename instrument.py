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

# MIDI ti MOD pitch numbers
MIDI2MODPITCHES={
    0:1712, 1:1616, 2:1525, 3:1440, 4:1357, 5:1281, 6:1209, 7:1141,
    8:1077, 9:1017, 10:961, 11:907, 12:856, 13:808, 14:762, 15:720,
    16:678, 17:640, 18:604, 19:570, 20:538, 21:508, 22:480, 23:453,
    24:428, 25:404, 26:381, 27:360, 28:339, 29:320, 30:302, 31:285,
    32:269, 33:254, 34:240, 35:226, 36:214, 37:202, 38:190, 39:180,
    40:170, 41:160, 42:151, 43:143, 44:135, 45:127, 46:120, 47:113,
    48:107, 49:101, 50:95, 51:90, 52:85, 53:80, 54:76, 55:71, 56:67,
    57:64, 58:60, 59:57}

NAMES2MIDI = {
    'C-0': 0, 'C#0': 1, 'D-0': 2, 'D#0': 3, 'E-0': 4, 'F-0': 5,
    'F#0': 6, 'G-0': 7, 'G#0': 8, 'A-0': 9, 'A#0': 10, 'B-0': 11,
    'C-1': 12, 'C#1': 13, 'D-1': 14, 'D#1': 15, 'E-1': 16, 'F-1': 17,
    'F#1': 18, 'G-1': 19, 'G#1': 20, 'A-1': 21, 'A#1': 22, 'B-1': 23,
    'C-2': 24, 'C#2': 25, 'D-2': 26, 'D#2': 27, 'E-2': 28, 'F-2': 29,
    'F#2': 30, 'G-2': 31, 'G#2': 32, 'A-2': 33, 'A#2': 34, 'B-2': 35,
    'C-3': 36, 'C#3': 37, 'D-3': 38, 'D#3': 39, 'E-3': 40, 'F-3': 41,
    'F#3': 42, 'G-3': 43, 'G#3': 44, 'A-3': 45, 'A#3': 46, 'B-3': 47,
    'C-4': 48, 'C#4': 49, 'D-4': 50, 'D#4': 51, 'E-4': 52, 'F-4': 53,
    'F#4': 54, 'G-4': 55, 'G#4': 56, 'A-4': 57, 'A#4': 58, 'B-4': 59 }

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


class Instrument:

    BEATS = 16  # Length of beat sequences to track (max 64)
    PAL = 3579545.25


    def __init__(self, sample, song=None):
        self.sample = sample
        self.song = song
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

        self._snr = None
        self._std_freq = None
        self._rounded_pitch_num = None

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
            idx = (np.abs(pitch_nums-avg_midi_pitch)).argmin()
            self._rounded_pitch_num =  pitch_nums[idx]
        return self._rounded_pitch_um

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

        spectrum = np.fft.fft(self.sample)
        freqs = np.fft.fftfreq(len(spectrum))

        idx = np.argmax(np.abs(spectrum))
        freq = freqs[idx]


      # return Note.PAL / self._period if self._period > 0 else 0

        period = MIDI2MODPITCHES[self.rounded_pitch_num]
        sample_rate = PAL / period

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

        #self.principle_freq = freq_in_hertz
        self._snr = snr
        self._std_freq = std_freq

        
# Instrument.analyze_pitch()
