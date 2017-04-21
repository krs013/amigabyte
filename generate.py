#!/usr/bin/env python3
from song import Song
from numpy.random import choice
from random import randint
from writeSong import writeFile, NoteObj
from tables import *
import time
import numpy as np
import copy

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
    
    # for note in Bassline:
    #     print(str(note.timestep) + ", " + str(note.pitch))

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

def generateTrebleLine3(
    Bassline,
    TP2TP,
    BP2TP,
    TT2TT,
    BT2TT):

    Trebleline = []
    pick = numTimesteps
    l = list(range(numTimesteps+1))

    # Create timestep list first
    currentBassNote = numTimesteps #
    if Bassline[0].timestep == 0:
        currentBassNote = 0

    matrix = copy.deepcopy(TT2TT)
    matrix[:-1,:-1] * np.power(BT2TT,1)
    while True:

        # Compute a dot produce of the two lists
        #combinedWeights = [a*b for a,b in zip(TT2TT[pick], BT2TT[currentBassNote])]
        combinedWeights = matrix[pick]
        # Update currentBassNote. How?
        
        # Renomalize the combinedWeights list
        if (sum(combinedWeights) == 0.0):
            print("zero!!")
            normalizedWeights = [0 for x in combinedWeights]
            normalizedWeights[numTimesteps] = 1.0
            # while True:
            #     x = 7
            pick = numTimesteps
        else:
            normalizedWeights = [x / sum(combinedWeights) for x in combinedWeights]
            # Make a choice
            pick = choice(l, p=normalizedWeights)
        if pick == numTimesteps:
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
    l = list(range(numPitches))

    for note in Trebleline:
        for bassnote in Bassline:
            if bassnote.timestep > note.timestep:
                break
            else:
                currentBassPitch = bassnote.pitch

        # Compute a dot proudct of the two lists
        combinedWeights = [a*b for a,b in zip(TP2TP[prevPitch],BP2TP[currentBassPitch])]

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
    l = list(range(numTimesteps+1))
    #pick = choice(l, p=weights)
    pick = 0
    note = NoteObj(-1,pick)
    Drumline.append(note)
    while True:
        prevpick = pick
        weights = t2t[pick]
        pick = choice(l, p=weights)
        if pick == numTimesteps:
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

def harmonyValue(b,t):
    if b > t:
        t += 12
    # smallest = min(b,t)
    # Offset in halfnotes
    offset = t - b

    if offset == 0:
        return 15
    elif offset == 1:
        return 0
    elif offset == 2:
        return 0
    elif offset == 3:
        return 0
    elif offset == 4:
        return 0
    elif offset == 5:
        return 10
    elif offset == 6:
        return 0
    elif offset == 7:
        return 20
    elif offset == 8:
        return 0
    elif offset == 9:
        return 0
    elif offset == 10:
        return 0
    elif offset == 11:
        return 0
    else:
        print("WARNING")
        return -100



def fitnessFunction(Bassline, Trebleline):
    score = 0
    # Well, let's just do this the easy way..
    eclipseCount = 0
    for bassnote in Bassline:
        for trebnote in Trebleline:
            if (bassnote.timestep == trebnote.timestep):
                eclipseCount += 1
                score += harmonyValue(bassnote.pitch%12, trebnote.pitch%12)
    score = score - eclipseCount
    lastTreb = 0
    for trebnote in Trebleline:
        if abs(trebnote.pitch - lastTreb) == 1:
            score -= 5
        lastTreb = trebnote.pitch

    lastBass = 0
    for bassnote in Bassline:
        if abs(bassnote.pitch - lastBass) == 1:
            score -= 5
        lastBass = bassnote.pitch

    return score

def generator(BP2BP, 
    BT2BT, 
    TP2TP, 
    TT2TT, 
    bass_sample, 
    treb_sample, 
    kick_sample, 
    bdpitch,
    bd2bd,
    snare_sample, 
    snpitch,
    sn2sn,
    BP2TP,
    BT2TT
    ):

    score = 0

    while score < 70:
        Bassline = generateBassline2(BT2BT, BP2BP)
        Trebleline = generateTrebleLine3(Bassline, TP2TP, BP2TP, TT2TT, BT2TT)
        score = fitnessFunction(Bassline, Trebleline)
        print("SCORE: " + str(score))

    Kickline = generateDrum(bd2bd, bdpitch)
    Snareline = generateDrum(sn2sn, snpitch)

    newTrebleline = []
    newBassline = []
    newKickline = []
    newSnareline = []

    for i in range(64//BEATS_WINDOW):
        for note in Trebleline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newTrebleline.append(newNote)
        for note in Bassline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newBassline.append(newNote)
        for note in Kickline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newKickline.append(newNote)
        for note in Snareline:
            newNote = NoteObj(int(note.pitch), int(note.timestep + i*16))
            newSnareline.append(newNote)




    songname = "creation64" + time.strftime('%H%M%S') + ".mod"

    writeFile(newBassline,
        newTrebleline,
        newKickline,
        newSnareline,
        songname, 
        bass_sample, 
        treb_sample,
        kick_sample,
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
