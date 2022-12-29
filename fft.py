from scipy import fft
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import sys

def frequency_spectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = np.arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft.fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    return frqarr, abs(x)


# Only works for wav files
here_path = os.path.dirname(os.path.realpath(__file__))
wav_file_name = "samples/" + sys.argv[1]
wave_file_path = os.path.join(here_path, wav_file_name)
sr, signal = wavfile.read(wave_file_path)

# y = signal[:, 0]  # use the first channel (or take their average, alternatively)
y = signal # Our test file is 1 channel
t = np.arange(len(y)) / float(sr)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('y')

frq, X = frequency_spectrum(y, sr)

plt.subplot(2, 1, 2)
plt.plot(frq, X, 'b')
plt.xlabel('Freq (Hz)')
plt.ylabel('|X(freq)|')
plt.tight_layout()

plt.show()
