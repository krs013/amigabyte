import numpy as np
from song import Song


def main():

    song = Song(filename='mods/mods/SimpleMods/3_pasar_lypsyl_4.mod')

    bass_pitches, bass_pitch_fomm = song.instruments[8].fomm_pitch()
    bass_beats_fomm = song.instruments[8].fomm_beats()
    
    for n in range(1, len(bb2bb)):
        bb2bb[n,:n]=0.0
        if sum(bb2bb[n]) == 0:
            bb2bb[n,-1] = 1.0
        else:
            bb2bb[n] /= sum(bb2bb[n])

    melody_pitches, melody_pitch_fomm = song.instruments[15].fomm_pitch()
    melody_beats_fomm = song.instruments[15].fomm_beats()
                            
    for n in range(1, len(bb2bb)):
        tb2tb[n,:n]=0.0
        if sum(tb2tb[n]) == 0:
            tb2tb[n,-1] = 1.0
        else:
            tb2tb[n] /= sum(tb2tb[n])
                            
    _, _, pitch_correlation = song.pitch_correlation(8, 15)
    beats_correlation = song.beats_correlation(8, 15)

    newBassline = []
    newTrebleline = []
    
    for i in range(4):
        for note in trebleline:
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
        for note in bassline:
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

    songname = "mimic.mod"

    writeFile(newBassline,newTrebleline,songname)

def mimic_test():
    song = Song(filename='mods/mods/SimpleMods/3_pasar_lypsyl_4.mod')
    print(len(song.instruments))

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

if __name__ == '__main__':
    # random_test()
    mimic_test()
