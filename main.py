#! /usr/bin/env python3

import sys
import aubio
# import numpy as np
import subprocess

def to_lilypond_format(note_list):
    suffixes = {'2':',', '3':'', '4':'\'', '5':'\'\''}
    formatted_notes = []
    formatted_notes.append('{\n')
    formatted_notes.append('\\clef bass \n')
    for note in note_list:
        formatted_notes.append(note[0].lower() + suffixes[note[1]])
    formatted_notes.append('\n}')
    return " ".join(formatted_notes)

def main():
    if len(sys.argv) < 2:
        print("Usage: %s <filename> [samplerate]" % sys.argv[0])
        sys.exit(1)

    filename = "samples/" + sys.argv[1]

    downsample = 1
    samplerate = 44100 // downsample
    if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

    win_s = 4096 // downsample # fft size
    hop_s = 1024  // downsample # hop size

    s = aubio.source(filename, samplerate, hop_s)
    samplerate = s.samplerate

    tolerance = 0.5

    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    pitches = []
    confidences = []

    # countframes = 0
    subnotes = []
    notes = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = s()
        test = pitch_o(samples)
        #print(test)
        pitch = test[0]
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        if confidence < 0.9: pitch = 0.
        #print("%f %f %s %f" % (total_frames / float(samplerate), pitch, aubio.midi2note(round(pitch)), confidence))
        #print("%s" % aubio.freq2note(pitch))
        
        if pitch == 0 and len(subnotes) != 0:
            mode = max(set(subnotes), key=subnotes.count)
            if mode != 0: notes.append(aubio.midi2note(mode))
            subnotes.clear()
        else:
            subnotes.append(round(pitch))

        """
        countframes += hop_s
        if countframes >= 22050:
            notes.append(max(set(subnotes), key=subnotes.count))
            subnotes.clear()
            countframes = 0
        """
        
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    print(notes)
    f_notes = to_lilypond_format(notes)
    print(f_notes)
    with open("out.ly", "w") as out_file:
        subprocess.run(["printf", "%s", f_notes], stdout=out_file)
    subprocess.run(["lilypond", "out.ly"])
    #subprocess.run(["rm", "out.ly"])
    #subprocess.run(["echo", f_notes, ">", "out.ly", "&&", "lilypond", "out.ly", "&&", "rm", "out.ly"])
    


if __name__ == "__main__":
    main()