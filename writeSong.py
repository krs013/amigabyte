#!/usr/bin/env python3
from math import sin, pi
from song import Song
from sample import Sample
from pattern import Pattern, Note
import copy
from numpy.random import choice
import random

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


MIDI2NAMES = {
    0: 'C-0', 1: 'C#0', 2: 'D-0', 3: 'D#0', 4: 'E-0', 5: 'F-0',
    6:'F#0', 7: 'G-0', 8: 'G#0', 9: 'A-0', 10: 'A#0', 11: 'B-0',
    12:	'C-1', 13: 'C#1', 14: 'D-1', 15: 'D#1', 16: 'E-1', 17: 'F-1',
    18: 'F#1', 19: 'G-1', 20: 'G#1', 21: 'A-1', 22: 'A#1', 23: 'B-1',
    24:	'C-2', 25: 'C#2', 26: 'D-2', 27: 'D#2', 28: 'E-2', 29: 'F-2',
    30:	'F#2', 31: 'G-2', 32: 'G#2', 33: 'A-2', 34: 'A#2', 35: 'B-2',
    36:	'C-3', 37: 'C#3', 38: 'D-3', 39: 'D#3', 40: 'E-3', 41: 'F-3',
    42:	'F#3', 43: 'G-3', 44: 'G#3', 45: 'A-3', 46: 'A#3', 47: 'B-3',
    48:	'C-4', 49: 'C#4', 50: 'D-4', 51: 'D#4', 52: 'E-4', 53: 'F-4',
    54:	'F#4', 55: 'G-4', 56: 'G#4', 57: 'A-4', 58: 'A#4', 59: 'B-4' }


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


class NoteObj:
    pitch = -1
    timestep = -1

    def __init__(self, pitch_in, timestep_in):
        self.pitch = pitch_in
        self.timestep = timestep_in

		
def rhythmMutation(pattern):
    newPattern = pattern
    print("rhythm")
    channelList = [0,1] # Only remove treble or bass for now
    channelPick = int(choice(channelList))
    timestepList = list(range(16))
    timestepPick = int(choice(timestepList))
    while timestepPick < 16:
        if pattern[channelPick][timestepPick] is not None:
            break
        else:
            timestepPick += 1
    i = 0
    for i in range(4):
        shiftIndex = timestepPick + (i * 16)
        while shiftIndex < 16*(i+1):
            if (shiftIndex != 0):
                pattern[channelPick][shiftIndex - 1] = pattern[
                    channelPick][shiftIndex]
            shiftIndex += 1
    return pattern


# Change into a minor key
# Specifically, turns all E naturals into Eb...
def minorKeyModulation(pattern):
    print("minor")
    for i in range(4):
        j = 0
        for note in pattern[i]:
            if note is not None:
                newNote = note
                if NAMES2MIDI[note.pitch]%12 == 4:
                    newNote.pitch = MIDI2NAMES[NAMES2MIDI[note.pitch] - 1]
                pattern[i][j] = newNote
            j += 1
    return pattern


# Remove a channel (instrument) from a pattern
def removeInstrument(pattern):
    print("removing")
    removeList = [0,1] # Only remove treble or bass for now
    removePick = choice(removeList)
    for i in range(64):
        pattern[int(removePick)][i] = None
    return pattern


def keyModulation(pattern):
    newPattern = pattern
    keychanges = [-3, -2,-3,5]
    offset = choice(keychanges)
    print("key change " + str(offset))
    for i in range(4):
        j = 0
        for note in pattern[i]:
            if note is not None:
                newNote = note
                if offset == -3 and NAMES2MIDI[note.pitch]%12 == 4:
                    newNote.pitch = MIDI2NAMES[NAMES2MIDI[note.pitch]
                                               + offset - 1]
                else:
                    newNote.pitch = MIDI2NAMES[NAMES2MIDI[note.pitch] + offset]
                newPattern[i][j] = newNote
            j += 1
    return newPattern


def addMutation(pattern):
    mutationChoices = [1,2,3,4]
    pick = choice(mutationChoices)
    if (pick == 1):
        newPattern = keyModulation(pattern)    
    if (pick == 2):
        newPattern = removeInstrument(pattern)
    if (pick == 3):
        newPattern = minorKeyModulation(pattern)
    else:
        newPattern = rhythmMutation(pattern)
    return newPattern


def writeFile(Bassline,Lead,songname):
    song = Song(name=songname)

    # It needs at least one sample. I'll just make a simple one
    sample = Sample(name='sine')

    # I think the samples are supposed to have a power of 2 length
    sample.wave = [100 * sin(2*pi*n/32) for n in range(32)]
    song.samples.append(sample)

    note_d = Note()
    note_d.sample = 1
    note_d.pitch = 'D-2'

    random.seed(a=None)

    pattern = Pattern()

    # Write bassline
    basslineChannel = pattern[0]
    for bassNotes in Bassline:
        note = Note()
        note.sample = 1 # Change this
        note.pitch = PITCHES[MIDI2MODPITCHES[bassNotes.pitch + 12]]
        if (bassNotes.timestep < 64):
            #print(bassNotes.timestep)
            basslineChannel[int(bassNotes.timestep)] = note
    
    leadChannel = pattern[1]
    for leadNotes in Lead:
        note = Note()
        note.sample = 1 # Change this
        note.pitch = PITCHES[MIDI2MODPITCHES[leadNotes.pitch + 24]]
        if (leadNotes.timestep < 64):
            #print(int(leadNotes.timestep))
            leadChannel[int(leadNotes.timestep)] = note

    song.patterns.append(pattern)

    patternCopy = copy.deepcopy(pattern)
    mutatedPattern = addMutation(patternCopy)
    song.patterns.append(mutatedPattern)

    patternCopy2 = copy.deepcopy(pattern)
    mutatedPattern2 = addMutation(patternCopy2)
    song.patterns.append(mutatedPattern2)

    patternCopy3 = copy.deepcopy(pattern)
    mutatedPattern3 = addMutation(patternCopy3)
    song.patterns.append(mutatedPattern3)

    song.positions.append(0)
    song.positions.append(1)
    song.positions.append(2)
    song.positions.append(3)

    song.write_file(songname)
