from scipy import fft, arange
import scipy.signal as sig
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os


def frequency_spectrum(x, sf):
    """
    Derive frequency spectrum of a signal from time domain
    :param x: signal in the time domain
    :param sf: sampling frequency
    :returns frequencies and their content distribution
    """
    x = x - np.average(x)  # zero-centering

    n = len(x)
    k = arange(n)
    tarr = n / float(sf)
    frqarr = k / float(tarr)  # two sides frequency range

    frqarr = frqarr[range(n // 2)]  # one side frequency range

    x = fft.fft(x) / n  # fft computing and normalization
    x = x[range(n // 2)]

    return frqarr, abs(x)


# Sine sample with a frequency of 1hz and add some noise
# sr = 32  # sampling rate
# y = np.linspace(0, 2*np.pi, sr)
# y = np.tile(np.sin(y), 5)
# y += np.random.normal(0, 1, y.shape)
# t = np.arange(len(y)) / float(sr)

# plt.subplot(2, 1, 1)
# plt.plot(t, y)
# plt.xlabel('t')
# plt.ylabel('y')

# frq, X = frequency_spectrum(y, sr)

# plt.subplot(2, 1, 2)
# plt.plot(frq, X, 'b')
# plt.xlabel('Freq (Hz)')
# plt.ylabel('|X(freq)|')
# plt.tight_layout()


# wav sample from https://freewavesamples.com/files/Alesis-Sanctuary-QCard-Crickets.wav
# here_path = os.path.dirname(os.path.realpath(__file__))
# wav_file_name = 'Alesis-Sanctuary-QCard-Crickets.wav'
# wave_file_path = os.path.join(here_path, wav_file_name)
sr, signal = wavfile.read('ald.wav')

notpass= True
bisect_point = int(len(signal)/2)
begin = 0
end = len(signal)
while (notpass):
    signal_appr = signal[begin:bisect_point]
    signal_rec = signal[bisect_point:end]

    peaks_appr=sig.find_peaks(signal_appr,height=np.average(signal_appr)*1.5,distance=500)
    peaks_rec=sig.find_peaks(signal_rec,height=np.average(signal_rec)*1.5,distance=500)

    


print(len(signal_appr),len(signal_rec))

y1 = signal_appr[:, 0]  # use the first channel (or take their average, alternatively)
t1 = np.arange(len(y1)) / float(sr)

plt.subplot(4, 2, 1)
plt.plot(t1, y1)
plt.xlabel('t1')
plt.ylabel('y1')

frq1, X1 = frequency_spectrum(y1, sr)

plt.subplot(4, 2, 2)
plt.plot(frq1, X1, 'b')
plt.xlabel('Freq1 (Hz)')
plt.ylabel('|X(freq1)|')
plt.tight_layout()

y2 = signal_rec[:, 0]  # use the first channel (or take their average, alternatively)
t2 = np.arange(len(y2)) / float(sr)

plt.subplot(4, 2, 3)
plt.plot(t2, y2)
plt.xlabel('t2')
plt.ylabel('y2')

frq2, X2 = frequency_spectrum(y2, sr)

plt.subplot(4, 2, 4)
plt.plot(frq2, X2, 'b')
plt.xlabel('Freq2 (Hz)')
plt.ylabel('|X(freq2)|')
plt.tight_layout()

plt.show()