from math import sin, pi
from song import Song
from sample import Sample
from pattern import Pattern, Note


def main():
    song = Song(name='demo')

    # It needs at least one sample. I'll just make a simple one
    sample = Sample(name='sine')

    # I think the samples are supposed to have a power of 2 length
    sample.wave = [100 * sin(2*pi*n/32) for n in range(32)]
    song.samples.append(sample)

    # I didn't really think all the way through ex nihilo generation,
    # so this is a little clunky. Make some note objects...
    note_c = Note()
    note_c.sample = 1  # Sample numbers start at 1, 0 is empty
    note_c.pitch = 'C-2'

    note_d = Note()
    note_d.sample = 1
    note_d.pitch = 'D-2'

    note_e = Note()
    note_e.sample = 1
    note_e.pitch = 'E-2'

    note_f4 = Note()
    note_f4.sample = 1
    note_f4.pitch = 'F-3'

    note_d5 = Note()
    note_d5.sample = 1
    note_d5.pitch = 'D-4'

    note_d4 = Note()
    note_d4.sample = 1
    note_d4.pitch = 'D-3'

    # I'm not sure if there will be side-effects of using a note
    # object in multiple places. I should look into making them
    # behave more like primitves. It will be ok for now.
    
    # Make a new pattern to go in our song
    pattern0 = Pattern()

    # Channels are made automatically and can't be moved or replaced,
    # but we'll grab one so we don't have to type pattern0[0] everywhere
    channel = pattern0[0]
    #channel = [0] * 64

    # Write our song
    #channel[0] = note_e
    #channel[4] = note_d
    #channel[8] = note_c

    #channel[16] = note_e
    #channel[20] = note_d
    #channel[24] = note_c

    #channel[32:40:2] = note_c
    #channel[40:48:2] = note_d

    #channel[48] = note_e
    #channel[52] = note_d
    #channel[56] = note_c

    channel[0] = note_f4
    channel[8] = note_d5
    channel[16] = note_d4
    channel[24] = note_d5
    channel[28] = note_f4
    channel[32] = note_f4
    channel[40] = note_f4
    channel[48] = note_d4
    channel[56] = note_d5



    # Adding a pattern takes two steps
    song.patterns.append(pattern0)  # Store the pattern
    song.positions = [0]  # Give it a position

    # Write out the file
    song.write_file('~/Desktop/forths.mod')


if __name__ == '__main__':
    main()
