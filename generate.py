#!/bin/bash/
from song import Song
from numpy.random import choice
from random import randint
from writeSong import writeFile, NoteObj

numPitches = 5
numTimesteps = 16 # 4 timesteps per beat

# rest = '|'


# # Everything from C1 to B4
# def getPitchIndex(s):
#     split = s.split('_')
#     index = 0
#     if (split[0] == "C"):
#         index = 0;
#     elif (split[0] == "Db"):
#         index = 1
#     elif (split[0] == "D"):
#         index = 2
#     elif (split[0] == "Eb"):
#         index = 3
#     elif (split[0] == "E"):
#         index = 4
#     elif (split[0] == "F"):
#         index = 5
#     elif (split[0] == "Gb"):
#         index = 6
#     elif (split[0] == "G"):
#         index = 7
#     elif (split[0] == "Ab"):
#         index = 8
#     elif (split[0] == "A"):
#         index = 9
#     elif (split[0] == "Bb"):
#         index = 10
#     elif (split[0] == "B"):
#         index = 11
#     else:
#         print("eRROR!")
#     if (index < 9):
#         octave = (int(split[1]) - 1)
#     else:
#         octave = (int(split[1]) - 2)
#     index = index + (12 * octave) + 1
#     return index
    
# def getPitchName(p):
#     if p == 0:
#         return "error"
#     elif p == 1:
#         return "C_1"
#     elif p == 2:
#         return "Db_1"
#     elif p == 3:
#         return "D_1"
#     elif p == 4:
#         return "Eb_1"
#     elif p == 5:
#         return "E_1"
#     elif p == 6:
#         return "F_1"
#     elif p == 7:
#         return "Gb_1"
#     elif p == 8:
#         return "G_1"
#     elif p == 9:
#         return "Ab_1"
#     elif p == 10:
#         return "A_2"
#     elif p == 11:
#         return "Bb_2"
#     elif p == 12:
#         return "B_2"
#     elif p == 13:
#         return "C_2"
#     elif p == 14:
#         return "Db_2"
#     elif p == 15:
#         return "D_2"
#     elif p == 16:
#         return "Eb_2"
#     elif p == 17:
#         return "E_2"
#     elif p == 18:
#         return "F_2"
#     elif p == 19:
#         return "Gb_2"
#     elif p == 20:
#         return "G_2"
#     elif p == 21:
#         return "Ab_2"
#     elif p == 22:
#         return "A_3"
#     elif p == 23:
#         return "Bb_3"
#     elif p == 24:
#         return "B_3"
#     elif p == 25:
#         return "C_3"
#     elif p == 26:
#         return "Db_3"
#     elif p == 27:
#         return "D_3"
#     elif p == 28:
#         return "Eb_3"
#     elif p == 29:
#         return "E_3"
#     elif p == 30:
#         return "F_3"
#     elif p == 31:
#         return "Gb_3"
#     elif p == 32:
#         return "G_3"
#     elif p == 33:
#         return "Ab_3"
#     elif p == 34:
#         return "A_4"
#     elif p == 35:
#         return "Bb_4"
#     elif p == 36:
#         return "B_4"
#     else:
#         return "ERROR"

# print("hello world")
# MarkovChain = []
# PitchMarkovChain = []
# song = Song()

# def initMarkovChains():
#     # Initialize rhythm markov chain
#     for i in range(0,18):
#         mylist = []
#         for j in range(0,18):
#             # index 0 is start
#             # index 1-16 is measure
#             # index 17 is stop
#             mylist.append(0.0)
#         MarkovChain.append(mylist)
#     # Initialize pitch markov chain. Range: C1 - B4 = 12 * 3 = 36
#     # Index 0 is the null pitch (before the first note in the sequence)
#     for i in range(0,37):
#         transitionList = []
#         for j in range(0,37):
#             transitionList.append(0.0)
#         PitchMarkovChain.append(transitionList)

# def extractData():
#     # single level Markov chain
#     with open('basslines.txt') as fp:
#         for line in fp:
#             array = line.split()
#             if array and array[0] != '%':
#                 if len(array) != 32:    # Check to see that the input bassline is the right length
#                     print('ERROR! wrong size')
#                     print(array)
#                 else:
#                     # First do all the rhythm stuff
#                     oldIndex = 0
#                     for i in range(1,17):
#                         if (array[i-1] != rest):
#                             MarkovChain[oldIndex][i] += 1
#                             oldIndex = i
#                     MarkovChain[oldIndex][17] += 1
                    
#                     # Then get pitch information
#                     oldPitch = 0;
#                     for i in range(0,16):
#                         if (array[i] != rest):
#                             pitch = getPitchIndex(array[i])
#                             PitchMarkovChain[oldPitch][pitch] += 1
#                             oldPitch = pitch
                    
# def computeProbabilities():
#     # Compute rhythm probabilities
#     for i in range(0,18):
#         total = 0.0
#         for j in range(0,18):
#             total += MarkovChain[i][j]
#         if (total != 0):
#             for j in range(0,18):
#                 MarkovChain[i][j] /= total
    
#     # Compute pitches probabilities
#     for i in range(0,37):
#         total = 0.0
#         for j in range(0,37):
#             total += PitchMarkovChain[i][j]
#         if (total != 0):
#             for j in range(0,37):
#                 PitchMarkovChain[i][j] /= total

# def createBassline():
#     beat = 0
#     newBassline = []
#     for i in range(0,16):
#         newBassline.append('|')
#     i = 0;
#     l = range(18)
#     #target = open('beats.txt', 'w')
#     beatList = []
#     while (i < 17):
#         weights = MarkovChain[i]
#         nextBeat = choice(l, p=weights)
#         beatList.append(nextBeat)
#         i = nextBeat

#     for beat in beatList:
#         l = range(37)
#         weights = PitchMarkovChain[0]
#         pitch = choice(l, p=weights)
#         if (beat != 17):
#             newBassline[beat-1] = getPitchName(pitch)
#             weights = PitchMarkovChain[pitch]
#             pitch = choice(l, p=weights)
#     str = ""
#     for note in newBassline:
#         note += " "
#         str += note
#     f = open('newBassline.txt', 'w')
#     f.write(str)
#     f.close()

# # This will be generated in a similar manner as the basslines,
# # but each next state will be a probability function of two previous states
# def createLeadVoice():
# 	newLeadLine = []
# 	for i in range(0, 16):
# 		newLeadLine.append('|')
# 	mostRecentBassNote = 24 # TODO! Make this the first note of the bassline
# 	# for i in range(0, 16):
# 	i = 0
# 	l = list(range(18,34))
# 	# Get the next location (time) of the beat
# 	while (i < 17):
# 		weights = [] # figure out what these weights should be!
# 		nextNote = choice

# 	# And then get the pitch




# # TODO: Let's do everything in terms of MIDI numbers

# def main():
# 	initMarkovChains();
# 	# Ideally, these next two lines are done somewhere else, and the results are written to a database
# 	# This file then simply reads in the pre-computed data
# 	extractData();
# 	computeProbabilities();


# 	createBassline()
# 	#createLeadVoice()


# main()




# This function generates a song based on the values given in three 2-dimensional tables
# These tables contain transition probabilities
# Each of these tables will be (47 notes x 16 timesteps + 1)^2 in size, or 753x753


#		____To_____
#		| [...]
#		| [...]
# From	| [...]
#		| [...]

# def generate(Bass2Bass, Bass2Treble, Treble2Treble):
# #def generate(BassTimestepConditionalProbabilitiesTable, BassPitchConditionalProbabilitiesTable)
# 	size = len(Bass2Bass)
	
# 	tableSize = numPitches*numTimesteps + 1

# 	l = list(range(size))
# 	#print(l)

# 	Bassline = []
# 	# Let's start by building a first-order Markov chain

# 	# Generate Bass Line
# 	nextNote = NoteObj(-1,-1)
# 	nextIndex = 0	# Index into location in the table
# 	#print(nextNote.pitch)
# 	#print(nextNote.timestep)

# 	while True:
# 		# stuff()
# 		weights = Bass2Bass[nextIndex]
# 		nextIndex = choice(l, p=weights)
# 		# l is the index into the table
# 		if (nextIndex == 0):
# 			break
# 		# Index 1 is equivalent to MIDI note 12
# 		print(nextIndex)
# 		pitch_in = (nextIndex-1)%numPitches + 12
# 		timestep_in = (nextIndex-1)//numPitches
# 		nextNote = NoteObj(pitch_in,timestep_in)
# 		#print(nextNote.pitch)
# 		#print(nextNote.timestep)
# 		Bassline.append(nextNote)

# 	for note in Bassline:
# 		print(str(note.pitch) + ", " + str(note.timestep))

# 	print("===")

# 	# Generate Treble Line (using probabilities from two tables)
# 	#nextIndex = 0
# 	if len(Bassline) > 0:
# 		lastBassNoteIndex = Bassline[0].pitch-1
# 		nextIndex = 0
# 		TrebleLine = []
# 		while True:
# 			weights = []
# 			sum = 0
# 			for i in range(tableSize):
# 				weight = Bass2Treble[lastBassNoteIndex][i] * Treble2Treble[nextIndex][i]
# 				weights.append(weight)
# 				sum += weight
# 			for i in range(tableSize):
# 				weights[i] /= sum
# 			print(weights)
# 			nextIndex = choice(l, p=weights)
# 			# l is the index into the table
# 			if (nextIndex == 0):
# 				break
# 			# Index 1 is equivalent to MIDI note 12
# 			print(nextIndex)
# 			pitch_in = (nextIndex-1)%numPitches + 12
# 			timestep_in = (nextIndex-1)//numPitches
# 			nextNote = NoteObj(pitch_in,timestep_in)
# 			#print(nextNote.pitch)
# 			#print(nextNote.timestep)
# 			TrebleLine.append(nextNote)
# 		for note in TrebleLine:
# 			print(str(note.pitch) + ", " + str(note.timestep))

# def createRandomTable():
# 	numPitches = 4
# 	numTimesteps = 4
# 	tableSize = numPitches*numTimesteps + 1
# 	Table = []
# 	entry = []
# 	max = 0
# 	sum = 0
# 	for i in range(tableSize):
# 		val = randint(0,1000)
# 		entry.append(val)
# 		sum += val
# 		if val > max:
# 			max = val

# 	for j in range(tableSize):
# 		entry[j] /= sum
# 	# print(entry)


# 	Table.append(entry)

# 	for i in range(1,tableSize):
# 		entry = []
# 		for j in range(tableSize):
# 			entry.append(0)
# 		sum = 0
# 		for j in range(((i-1)//numPitches)*numPitches+numPitches+1,tableSize):
# 			val = randint(0,1000)
# 			sum += val
# 			entry[j] = val
# 		val = randint(0,1000) + 500
# 		sum += val
# 		entry[0] = val


# 		# for j in range(((i-1)//numPitches)*numPitches+1,tableSize):
# 		# 	val = randint(0,1000)
# 		# 	entry[j] = val
# 		# 	if (val > max):
# 		# 		max = val
# 		for j in range(tableSize):
# 			entry[j] /= sum



# 		Table.append(entry)
# 		#print(entry)
# 	#print(Table)
# 	# for line in Table:
# 	# 	string = ""
# 	# 	for i in line:
# 	# 		string += "%.2f" % i + " "
# 	# 	print(string)
# 	# print("done")
# 	return Table

def createPitchTable():
	Table = []
	for i in range(numPitches+1):
		entry = []
		entry.append(0)
		sum = 0
		for j in range(1,numPitches+1):
			val = randint(0,1000)
			entry.append(val)
			sum += val
		for j in range(numPitches+1):
			entry[j] /= sum
		Table.append(entry)
	return Table

def createTimestepTable():
	Table = []
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
		Table.append(entry)
	return Table

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
		# if pick == 1:				# FIXME: this is a hack
		# 	pick = 0
		# if pick == 2:
		# 	pick = 2
		# if pick == 3 or pick == 4:
		# 	pick += 1
		# if pick == 5:
		# 	pick = 7
		note.pitch = pick
	
	return Bassline

def generateTrebleLine(Bassline,TreblePitch2TreblePitch,BassPitch2TreblePitch,TrebleTimestep2TrebleTimestep,BassTimestep2TrebleTimestep, BassTimestep2BassTimestep):
	# First generate timestep pattern
	Trebleline = []
	pick = 0
	l = list(range(numTimesteps+1))

	# You need to be considering only the most recent bass note played.....

	# Create timestep list first
	currentBassNote = 0 #>>Bassline[0].timestep # Or else a treble line may never start before the bassline...
	if Bassline[0].timestep == 1:
		currentBassNote = 1
	print(str([x.timestep for x in Bassline]))
	while True:

		# Compute a dot produce of the two lists
		combinedWeights = [a*b for a,b in zip(TrebleTimestep2TrebleTimestep[pick], BassTimestep2TrebleTimestep[currentBassNote])] # Update currentBassNote. How?
		
		# Renomalize the combinedWeights list
		normalizedWeights = [x / sum(combinedWeights) for x in combinedWeights]

		# Make a choice
		pick = choice(l, p=normalizedWeights)
		print(pick)
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
			print("currentBassNote is now " + str(currentBassNote))
			print("=======")

				

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

		print("currentBassPitch is " + str(currentBassPitch))
		print("prev pitch is " + str(prevPitch))
		# Compute a dot proudct of the two lists
		combinedWeights = [a*b for a,b in zip(TreblePitch2TreblePitch[prevPitch], BassPitch2TreblePitch[currentBassPitch])]

		# Renormalize
		normalizedWeights = [x / sum(combinedWeights) for x in combinedWeights]

		pick = choice(l, p=normalizedWeights)
		
		prevPitch = pick

		note.pitch = pick
		# newpitch = 0
		# if pick == 1:
		# 	newpitch = 0
		# if pick == 2:
		# 	newpitch = 2
		# if pick == 3 or pick == 4:
		# 	newpitch += 1
		# if pick == 5:
		# 	newpitch = 7
		# note.pitch = newpitch
	
	return Trebleline


# Bass Notes go from C1 to B4, aka MIDI notes 12 - 59
# Treble Notes go from C5 to C8, aka MIDI notes 60 - 107

def main():
	BassPitch2BassPitch = createPitchTable()
	BassTimestep2BassTimestep = createTimestepTable()

	TreblePitch2TreblePitch = createPitchTable()
	TrebleTimestep2TrebleTimestep = createTimestepTable()

	BassPitch2TreblePitch = createPitchTable()
	BassTimestep2TrebleTimestep = createTimestepTable()

	Bassline = generateBassline(BassTimestep2BassTimestep, BassPitch2BassPitch)
	Trebleline = generateTrebleLine(Bassline,TreblePitch2TreblePitch,BassPitch2TreblePitch,TrebleTimestep2TrebleTimestep,BassTimestep2TrebleTimestep,BassTimestep2BassTimestep)
	newBassline = []
	newTrebleline = []

	# for note in Bassline:
	# 	newNote = NoteObj(int(note.pitch), int(note.timestep))
	# 	newBassline.append(newNote)
	# for note in Bassline:
	# 	newNote = NoteObj(int(note.pitch), int(note.timestep+16))
	# 	newBassline.append(newNote)
	# for note in Bassline:
	# 	newNote = NoteObj(int(note.pitch), int(note.timestep+32))
	# 	newBassline.append(newNote)
	# for note in Bassline:
	# 	newNote = NoteObj(int(note.pitch), int(note.timestep+48))
	# 	newBassline.append(newNote)
	
	for i in range(4):
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
		# for note in Trebleline:
		# 	newNote = NoteObj(int(note.pitch), int(note.timestep+16))
		# 	newTrebleline.append(newNote)
		# for note in Trebleline:
		# 	newNote = NoteObj(int(note.pitch), int(note.timestep+32))
		# 	newTrebleline.append(newNote)
		# for note in Trebleline:
		# 	newNote = NoteObj(int(note.pitch), int(note.timestep+48))
		# 	newTrebleline.append(newNote)


	songname = "demo.mod"

	writeFile(newBassline,newTrebleline,songname)

main()