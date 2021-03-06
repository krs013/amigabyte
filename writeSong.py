#!/usr/bin/env python3
from math import sin, pi
from song import Song
from sample import Sample
from pattern import Pattern, Note
import copy
from numpy.random import choice
import random
from tables import *


class NoteObj:
    pitch = -1
    timestep = -1

    def __init__(self, pitch_in, timestep_in):
        self.pitch = pitch_in
        self.timestep = timestep_in

		
def rhythmMutation(pattern):
    print("rhythm")
    channelPick = int(choice([0,1]))
    timestepPick = int(choice(list(range(BEATS_WINDOW))))
    while timestepPick < BEATS_WINDOW:
        if pattern[channelPick][timestepPick] is not None:
            break
        else:
            timestepPick += 1

    rhythmPick = choice([-2,2])
    if timestepPick + rhythmPick >= 0 and timestepPick + rhythmPick < 64:
        pattern[channelPick][int(timestepPick + rhythmPick)] = pattern[channelPick][timestepPick]
        pattern[channelPick][timestepPick] = None
    else:
        rhythmMutation(pattern)

    # i = 0
    # for i in range(64//BEATS_WINDOW):
    #     shiftIndex = timestepPick + (i * 16)
    #     while shiftIndex < 16*(i+1):
    #         if (shiftIndex != 0):
    #             pattern[channelPick][shiftIndex - 1] = pattern[
    #                 channelPick][shiftIndex]
    #         shiftIndex += 1
    return pattern


# Change into a minor key
# Specifically, turns all E naturals into Eb...
def minorKeyModulation(pattern):
    print("minor")
    for i in range(64//BEATS_WINDOW):
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
    removePick = choice([0,1,2])
    removeLengths = [4,8,16,32,64]
    lengthPick = choice(removeLengths)
    for i in range(64 - lengthPick, 64):
        if removePick == 2:
            if pattern[int(removePick)][i]:
                pattern[int(removePick)][i].effect = (12,0)
            if pattern[int(removePick+1)][i]:
                pattern[int(removePick+1)][i].effect = (12,0)
        else:
            if pattern[int(removePick)][i]:
                pattern[int(removePick)][i].effect = (12,0)
    return pattern


def keyModulation(pattern):
    newPattern = pattern
    keychanges = [-3, -2,3,5]
    endpoint = choice([16,32,64,64])
    offset = choice(keychanges)
    print("key change " + str(offset))
    for i in range(2):
        j = 0
        for note in pattern[i]:
            if note is not None:
                newNote = note
                if offset == -3 and NAMES2MIDI[note.pitch]%12 == 4:
                    newNote.pitch = MIDI2NAMES[NAMES2MIDI[note.pitch]
                                               + offset - 1]
                else:
                    if NAMES2MIDI[note.pitch] < 3:
                        MIDI2NAMES[NAMES2MIDI[note.pitch] + offset + 12]
                    else:
                        newNote.pitch = MIDI2NAMES[NAMES2MIDI[note.pitch] + offset]
                newPattern[i][j] = newNote
            j += 1
    return newPattern


def addMutation(pattern):
    mutationChoices = [1,2,3,4]
    pick = choice(mutationChoices)
    print(pick)
    if (pick == 1):
        newPattern = keyModulation(pattern)    
    elif (pick == 2):
        newPattern = removeInstrument(pattern)
    elif (pick == 3):
        #newPattern = minorKeyModulation(pattern)
        print("double!")
        pattern2 = keyModulation(pattern)
        newPattern = removeInstrument(pattern2)
    else:
        newPattern = rhythmMutation(pattern)
        newPattern = removeInstrument(pattern)

    return newPattern


def writeFile(Bassline,
    Lead,
    Kick,
    Snare,
    songname,
    bass_sample, 
    treb_sample,
    kick_sample,
    snare_sample):

    song = Song(name=songname)

    # It needs at least one sample. I'll just make a simple one
    # sample = Sample(name='sine')
    # sample = bass_sample
    # I think the samples are supposed to have a power of 2 length
    # sample.wave = [100 * sin(2*pi*n/32) for n in range(32)]
    song.samples.append(bass_sample)
    song.samples.append(treb_sample)
    song.samples.append(kick_sample)
    song.samples.append(snare_sample)

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
        note.pitch = PITCHES[MIDI2MODPITCHES[bassNotes.pitch]]
        if (bassNotes.timestep < 64):
            #print(bassNotes.timestep)
            basslineChannel[int(bassNotes.timestep) - 12] = note
    
    leadChannel = pattern[1]
    for leadNotes in Lead:
        note = Note()
        note.sample = 2 # Change this
        note.pitch = PITCHES[MIDI2MODPITCHES[leadNotes.pitch]]
        if (leadNotes.timestep < 64):
            #print(int(leadNotes.timestep))
            leadChannel[int(leadNotes.timestep)] = note

    bdChannel = pattern[2]
    for bdNotes in Kick:
        note = Note()
        note.sample = 3 # Change this
        note.pitch = PITCHES[MIDI2MODPITCHES[bdNotes.pitch]]
        if (bdNotes.timestep < 64):
            #print(int(leadNotes.timestep))
            bdChannel[int(bdNotes.timestep)] = note

    snareChannel = pattern[3]
    for snareNotes in Snare:
        note = Note()
        note.sample = 4 # Change this
        note.pitch = PITCHES[MIDI2MODPITCHES[snareNotes.pitch]]
        if (snareNotes.timestep < 64):
            #print(int(leadNotes.timestep))
            snareChannel[int(snareNotes.timestep)] = note

    song.patterns.append(pattern)

    patternCopy = copy.deepcopy(pattern)
    mutatedPattern = addMutation(patternCopy)
    song.patterns.append(mutatedPattern)

    patternCopy2 = copy.deepcopy(pattern)
    mutatedPattern2 = addMutation(patternCopy2)
    mutatedPattern2b = addMutation(mutatedPattern2)
    song.patterns.append(mutatedPattern2b)

    patternCopy3 = copy.deepcopy(pattern)
    mutatedPattern3 = addMutation(patternCopy3)
    song.patterns.append(mutatedPattern3)

    song.positions.append(0)
    song.positions.append(1)
    song.positions.append(2)
    song.positions.append(3)

    song.write_file(songname)
