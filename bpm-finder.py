import wave
import threading
import struct
import sys
import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

SAMPLE_LEN = 230000
CHUNK = 1024


def hear_the_wave():
    sys.argv.append('try.wav')
    if len(sys.argv) < 2:
        print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
        sys.exit(-1)

    wf = wave.open(sys.argv[1], 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


def slice_wav_file():
    t1 = 120
    t2 = 130
    t1 *= 1000  # Works in milliseconds
    t2 *= 1000
    new_audio = AudioSegment.from_wav("try.wav")
    new_audio = new_audio[t1:t2]
    new_audio.export('newSong.wav', format="wav")  # Exports to a wav file in the current path.


def wav_to_floats(wave_file="newSong.wav"):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short
    a = struct.unpack("%ih" % (w.getnframes()*w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a


def print_float():
    signal = wav_to_floats()
    print "read " + str(len(signal)) + " frames"
    print "in the range " + str(min(signal)) + " to " + str(min(signal))


def find_max(signal):
    max_signal = max(signal)
    arr_max = []
    place = []
    i = 0
    while i < len(signal):
        if signal[i] + 5000 >= max_signal:
            if place:
                if i - 30000 >= place[len(place) - 1]:
                    arr_max.append(signal[i])
                    place.append(i)
            else:
                arr_max.append(signal[i])
                place.append(i)
        i += 1
    print arr_max
    print place
    return "BPM: " + str(len(arr_max) * 6)


def main():
    slice_wav_file()
    print_float()
    spf = wave.open('newSong.wav', 'r')

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    bpm = find_max(signal)
    # plt.figure(1)
    # plt.title('Signal Wave...')
    # plt.plot(signal)
    # plt.show()

    t = threading.Thread(target=hear_the_wave)
    t.start()
    plt.figure(1)
    plt.title(bpm)
    plt.plot(signal)
    plt.show()


if __name__ == '__main__':
    main()