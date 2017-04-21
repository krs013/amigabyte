#!/usr/bin/env python3
from song import Song
from numpy.random import choice
from random import randint
from writeSong import writeFile, NoteObj
from tables import *
import time

numPitches = 60
numTimesteps = BEATS_WINDOW

# Create a randomized table for testing purposes
def createPitchTable():
    table = []
    for i in range(numPitches+1):
        entry = [0]
        sum = 0
        for j in range(1,numPitches+1):
            val = randint(0,1000)
            entry.append(val)
            sum += val
        for j in range(numPitches+1):
            entry[j] /= sum
        table.append(entry)
    return table


# Create a randomized upper traingular table for testing purposes
def createTimestepTable():
    table = []
    # first entry in table is NULL
    for i in range(numTimesteps+1):
        entry = []
        val = randint(0,1000)/20
        sum = val
        entry.append(val)
        for j in range(1,numTimesteps+1):
            if (j > i):
                val = randint(0,1000)/j
                sum += val
                entry.append(val)
            else:
                entry.append(0)
        for j in range(numTimesteps+1):
            entry[j] /= sum
        table.append(entry)
    return table


# Generate a bassline
def generateBassline(BassTimestep2BassTimestep, BassPitch2BassPitch):
    # First generate timestep pattern
    Bassline = []

    nextIndex = 0
    weights = BassTimestep2BassTimestep[nextIndex]
    l = list(range(numTimesteps+1))
    pick = choice(l, p=weights)
    note = NoteObj(-1,pick)
    Bassline.append(note)
    while True:
        weights = BassTimestep2BassTimestep[pick]
        pick = choice(l, p=weights)
        if pick ==0:
            break
        else:
            note = NoteObj(-1,pick)
            Bassline.append(note)

    # Then fill in notes with pitches
    prevPitch = 0
    l = list(range(numPitches+1))
    for note in Bassline:
        weights = BassPitch2BassPitch[prevPitch]
        pick = choice(l, p=weights)
        note.pitch = pick
    
    return Bassline

# Generate a bassline to fit the learning phase
def generateBassline2(BassTimestep2BassTimestep, BassPitch2BassPitch):
    # First generate timestep pattern
    Bassline = []

    nextIndex = 0
    weights = BassTimestep2BassTimestep[nextIndex]
    l = list(range(numTimesteps+1))
    #pick = choice(l, p=weights)
    pick = numTimesteps
    note = NoteObj(-1,pick)
    Bassline.append(note)
    while True:
        prevpick = pick
        weights = BassTimestep2BassTimestep[pick]
        pick = choice(l, p=weights)
        if pick == numTimesteps:
            break
        else:
            note = NoteObj(-1,pick)
            Bassline.append(note)

    # Then fill in notes with pitches
    prevPitch = 0
    l = list(range(numPitches))
    for note in Bassline:
        weights = BassPitch2BassPitch[prevPitch]
        pick = choice(l, p=weights)
        note.pitch = pick
        prevPitch = pick
    
    for note in Bassline:
        print(str(note.timestep) + ", " + str(note.pitch))

    return Bassline

# Generate a trebleline to fit the learning phase
def generateTrebleline2(TrebleTimestep2TrebleTimestep, TreblePitch2TreblePitch):
    # First generate timestep pattern
    Trebleline = []

    nextIndex = 0
    weights = TrebleTimestep2TrebleTimestep[nextIndex]
    l = list(range(numTimesteps+1))
    #pick = choice(l, p=weights)
    pick = numTimesteps
    note = NoteObj(-1,pick)
    Trebleline.append(note)
    while True:
        prevpick = pick
        weights = TrebleTimestep2TrebleTimestep[pick]
        pick = choice(l, p=weights)
        if pick == numTimesteps:
            break
        else:
            note = NoteObj(-1,pick)
            Trebleline.append(note)

    # Then fill in notes with pitches
    prevPitch = 0
    l = list(range(numPitches))
    for note in Trebleline:
        weights = TreblePitch2TreblePitch[prevPitch]
        pick = choice(l, p=weights)
        note.pitch = pick
        prevPitch = pick
    
    for note in Trebleline:
        print(str(note.timestep) + ", " + str(note.pitch))

    return Trebleline

# Generate a treble line, contingent on the bassline
def generateTrebleLine(
        Bassline, TreblePitch2TreblePitch,
        BassPitch2TreblePitch, TrebleTimestep2TrebleTimestep,
        BassTimestep2TrebleTimestep, BassTimestep2BassTimestep):
    # First generate timestep pattern
    Trebleline = []
    pick = 0
    l = list(range(numTimesteps+1))

    # Create timestep list first
    currentBassNote = 0 #
    if Bassline[0].timestep == 1:
        currentBassNote = 1
    while True:

        # Compute a dot produce of the two lists
        combinedWeights = [a*b for a,b in
                           zip(TrebleTimestep2TrebleTimestep[pick],
                               BassTimestep2TrebleTimestep[currentBassNote])]
        # Update currentBassNote. How?
        
        # Renomalize the combinedWeights list
        normalizedWeights = [x / sum(combinedWeights) for x in combinedWeights]

        # Make a choice
        pick = choice(l, p=normalizedWeights)
        if pick == 0:
            break
        else:
            note = NoteObj(-1, pick)
            Trebleline.append(note)

            # Find new currentBassNote
            newCurrentBassNote = currentBassNote
            for bassnote in Bassline:
                if (bassnote.timestep > pick):
                    break
                else:
                    newCurrentBassNote = bassnote.timestep
            currentBassNote = newCurrentBassNote

    # Then fill in notes with pitches
    prevPitch = 0
    currentBassPitch = Bassline[0].pitch
    l = list(range(numPitches+1))
    for note in Trebleline:

        for bassnote in Bassline:
            if bassnote.timestep > note.timestep:
                break
            else:
                currentBassPitch = bassnote.pitch

        # Compute a dot proudct of the two lists
        combinedWeights = [a*b for a,b in
                           zip(TreblePitch2TreblePitch[prevPitch],
                               BassPitch2TreblePitch[currentBassPitch])]

        # Renormalize
        normalizedWeights = [x / sum(combinedWeights) for x in combinedWeights]

        pick = choice(l, p=normalizedWeights)
        prevPitch = pick
        note.pitch = pick

    return Trebleline

def generateDrum(t2t, pitch):
    Drumline = []

    nextIndex = 0
    weights = t2t[nextIndex]
    l = list(range(numTimesteps))
    #pick = choice(l, p=weights)
    pick = 0
    note = NoteObj(-1,pick)
    Drumline.append(note)
    while True:
        prevpick = pick
        weights = t2t[pick]
        pick = choice(l, p=weights)
        if pick <= prevpick:
            break
        else:
            note = NoteObj(-1,pick)
            Drumline.append(note)

    # Then fill in notes with pitches
    for note in Drumline:
        note.pitch = pitch
        # prevPitch = pick
    
    # for note in Drumline:
    #     print(str(note.timestep) + ", " + str(note.pitch))

    return Drumline


def generator(BP2BP, 
    BT2BT, 
    TP2TP, 
    TT2TT, 
    bass_sample, 
    treb_sample, 
    bassdrum_sample, 
    bdpitch,
    bd2bd,
    snare_sample, 
    snpitch,
    sn2sn
    ):
    
    Bassline = generateBassline2(BT2BT, BP2BP)
    Trebleline = generateTrebleline2(TT2TT, TP2TP)
    Bassdrumline = generateDrum(bd2bd, bdpitch)
    Snareline = generateDrum(sn2sn, snpitch)

    newTrebleline = []
    newBassline = []
    newBassdrumline = []
    newSnareline = []

    for i in range(64//BEATS_WINDOW):
        for note in Trebleline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newTrebleline.append(newNote)
        for note in Bassline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newBassline.append(newNote)
        for note in Bassdrumline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newBassdrumline.append(newNote)
        for note in Snareline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newSnareline.append(newNote)

    songname = "creation64" + time.strftime('%H%M%S') + ".mod"

    writeFile(newBassline,
        newTrebleline,
        newBassdrumline,
        newSnareline,
        songname, 
        bass_sample, 
        treb_sample,
        bassdrum_sample,
        snare_sample
        )


def random_test():
    BassPitch2BassPitch = createPitchTable()
    BassTimestep2BassTimestep = createTimestepTable()

    TreblePitch2TreblePitch = createPitchTable()
    TrebleTimestep2TrebleTimestep = createTimestepTable()

    BassPitch2TreblePitch = createPitchTable()
    BassTimestep2TrebleTimestep = createTimestepTable()

    Bassline = generateBassline(BassTimestep2BassTimestep, BassPitch2BassPitch)
    Trebleline = generateTrebleLine(
        Bassline, TreblePitch2TreblePitch, BassPitch2TreblePitch,
        TrebleTimestep2TrebleTimestep, BassTimestep2TrebleTimestep,
        BassTimestep2BassTimestep)
    newBassline = []
    newTrebleline = []
    
    for i in range(64//BEATS_WINDOW):
        for note in Trebleline:
            if note.pitch == 1:
                note.pitch = 0
            if note.pitch == 2:
                note.pitch = 2
            if note.pitch == 3 or note.pitch == 4:
                note.pitch += 1
            if note.pitch == 5:
                note.pitch = 7
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newTrebleline.append(newNote)
        for note in Bassline:
            if note.pitch == 1:
                note.pitch = 0
            if note.pitch == 2:
                note.pitch = 2
            if note.pitch == 3 or note.pitch == 4:
                note.pitch += 1
            if note.pitch == 5:
                note.pitch = 7
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newBassline.append(newNote)

    songname = "demo.mod"

    writeFile(newBassline,newTrebleline,songname)

if __name__ == '__main__':
    random_test()
