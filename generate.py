#!/bin/bash/
from song import Song
from numpy.random import choice
from random import randint
from writeSong import writeFile, NoteObj

numPitches = 5
numTimesteps = 16 # 4 timesteps per beat

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
		note.pitch = pick
	
	return Bassline

def generateTrebleLine(Bassline,TreblePitch2TreblePitch,BassPitch2TreblePitch,TrebleTimestep2TrebleTimestep,BassTimestep2TrebleTimestep, BassTimestep2BassTimestep):
	# First generate timestep pattern
	Trebleline = []
	pick = 0
	l = list(range(numTimesteps+1))

	# You need to be considering only the most recent bass note played.....

	# Create timestep list first
	currentBassNote = 0 #
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

	songname = "demo.mod"

	writeFile(newBassline,newTrebleline,songname)

main()