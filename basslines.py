#!/usr/bin/env python
from numpy.random import choice
from datetime import datetime
from writeSong import writeFile

rest = '|'

MarkovChain = []
PitchMarkovChain = []
Bassline = []


# Everything from C1 to B4
def getPitchIndex(s):
    split = s.split('_')
    index = 0
    if (split[0] == "C"):
        index = 0;
    elif (split[0] == "Db"):
        index = 1
    elif (split[0] == "D"):
        index = 2
    elif (split[0] == "Eb"):
        index = 3
    elif (split[0] == "E"):
        index = 4
    elif (split[0] == "F"):
        index = 5
    elif (split[0] == "Gb"):
        index = 6
    elif (split[0] == "G"):
        index = 7
    elif (split[0] == "Ab"):
        index = 8
    elif (split[0] == "A"):
        index = 9
    elif (split[0] == "Bb"):
        index = 10
    elif (split[0] == "B"):
        index = 11
    else:
        print("eRROR!")
    if (index < 9):
        octave = (int(split[1]) - 1)
    else:
        octave = (int(split[1]) - 2)
    index = index + (12 * octave) + 1
    return index
    
def getPitchName(p):
    if p == 0:
        return "error"
    elif p == 1:
        return "C_1"
    elif p == 2:
        return "Db_1"
    elif p == 3:
        return "D_1"
    elif p == 4:
        return "Eb_1"
    elif p == 5:
        return "E_1"
    elif p == 6:
        return "F_1"
    elif p == 7:
        return "Gb_1"
    elif p == 8:
        return "G_1"
    elif p == 9:
        return "Ab_1"
    elif p == 10:
        return "A_2"
    elif p == 11:
        return "Bb_2"
    elif p == 12:
        return "B_2"
    elif p == 13:
        return "C_2"
    elif p == 14:
        return "Db_2"
    elif p == 15:
        return "D_2"
    elif p == 16:
        return "Eb_2"
    elif p == 17:
        return "E_2"
    elif p == 18:
        return "F_2"
    elif p == 19:
        return "Gb_2"
    elif p == 20:
        return "G_2"
    elif p == 21:
        return "Ab_2"
    elif p == 22:
        return "A_3"
    elif p == 23:
        return "Bb_3"
    elif p == 24:
        return "B_3"
    elif p == 25:
        return "C_3"
    elif p == 26:
        return "Db_3"
    elif p == 27:
        return "D_3"
    elif p == 28:
        return "Eb_3"
    elif p == 29:
        return "E_3"
    elif p == 30:
        return "F_3"
    elif p == 31:
        return "Gb_3"
    elif p == 32:
        return "G_3"
    elif p == 33:
        return "Ab_3"
    elif p == 34:
        return "A_4"
    elif p == 35:
        return "Bb_4"
    elif p == 36:
        return "B_4"
    else:
        return "ERROR"
    
    
    
    
def initMarkovChains():
    # Initialize rhythm markov chain
    for i in range(0,18):
        mylist = []
        for j in range(0,18):
            # index 0 is start
            # index 1-16 is measure
            # index 17 is stop
            mylist.append(0.0)
        MarkovChain.append(mylist)
    # Initialize pitch markov chain. Range: C1 - B4 = 12 * 3 = 36
    # Index 0 is the null pitch (before the first note in the sequence)
    for i in range(0,37):
        transitionList = []
        for j in range(0,37):
            transitionList.append(0.0)
        PitchMarkovChain.append(transitionList)

def extractData():
    # single level Markov chain
    with open('basslines.txt') as fp:
        for line in fp:
            array = line.split()
            if array and array[0] != '%':
                if len(array) != 32:    # Check to see that the input bassline is the right length
                    print('ERROR! wrong size')
                    print(array)
                else:
                    # First do all the rhythm stuff
                    oldIndex = 0
                    for i in range(1,17):
                        if (array[i-1] != rest):
                            MarkovChain[oldIndex][i] += 1
                            oldIndex = i
                    MarkovChain[oldIndex][17] += 1
                    
                    # Then get pitch information
                    oldPitch = 0;
                    for i in range(0,16):
                        if (array[i] != rest):
                            pitch = getPitchIndex(array[i])
                            PitchMarkovChain[oldPitch][pitch] += 1
                            oldPitch = pitch
                    
def computeProbabilities():
    # Compute rhythm probabilities
    for i in range(0,18):
        total = 0.0
        for j in range(0,18):
            total += MarkovChain[i][j]
        if (total != 0):
            for j in range(0,18):
                MarkovChain[i][j] /= total
    
    # Compute pitches probabilities
    for i in range(0,37):
        total = 0.0
        for j in range(0,37):
            total += PitchMarkovChain[i][j]
        if (total != 0):
            for j in range(0,37):
                PitchMarkovChain[i][j] /= total

def createBassline():
    beat = 0
    newBassline = []
    for i in range(0,16):
        newBassline.append('|')
    i = 0;
    l = range(18)
    #target = open('beats.txt', 'w')
    beatList = []
    while (i < 17):
        weights = MarkovChain[i]
        nextBeat = choice(l, p=weights)
        beatList.append(nextBeat)
        i = nextBeat

        note = []
        note.append(int(nextBeat)*4)
        Bassline.append(note)
    print(beatList)
    i=0
    for beat in beatList:
        l = range(37)
        weights = PitchMarkovChain[0]
        pitch = choice(l, p=weights)
        Bassline[i].append(int(pitch)+12)
        i = i + 1
        if (beat != 17):
            newBassline[beat-1] = getPitchName(pitch)
            weights = PitchMarkovChain[pitch]
            pitch = choice(l, p=weights)
    str = ""
    for note in newBassline:
        note += " "
        str += note
    f = open('newBassline.txt', 'w')
    f.write(str)
    f.close()

    print(Bassline)


    
initMarkovChains();
extractData();
computeProbabilities();
createBassline();
writeFile(Bassline,Bassline,"bassline" + ".mod")
