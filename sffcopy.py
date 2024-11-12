from scipy import fft
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplib
mplib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy.io import wavfile
import os
import tkinter as tk
from tkinter import ttk

LARGE_FONT= ("Verdana", 12)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        sliderstart = ttk.Scale(self,length=500,from_=0,to=1, orient='horizontal')
        sliderseek = tk.Scale(self,length=500,from_=0,to=1,tickinterval=0.1, orient='horizontal')
        sliderend = ttk.Scale(self,length=500,from_=0,to=1, orient='horizontal')
        sliderstart.pack()
        sliderseek.pack()
        sliderend.pack()
        
        

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

def seek_plot(seekpointstart,seek, seekpointend):
    signal1 = signal[int(len(signal)*seekpointstart):int(len(signal)*seek)]
    signal2 = signal[int(len(signal)*seekpointstart):int(len(signal)*seekpointend)]
    print(len(signal1),len(signal2))

y1 = signal1[:, 0]  # use the first channel (or take their average, alternatively)
t1 = np.arange(len(y1)) / float(sr)

# plt.subplot(2, 2, 1)
# plt.plot(t1, y1)
# plt.xlabel('t1')
# plt.ylabel('y1')

frq1, X1 = frequency_spectrum(y1, sr)

# plt.subplot(2, 2, 2)

# # plt.plot(frq1, X1, 'r')
# plt.xlabel('Freq1 (Hz)')
# plt.ylabel('|X(freq1)|')
# plt.tight_layout()

y2 = signal2[:, 0]  # use the first channel (or take their average, alternatively)
t2 = np.arange(len(y2)) / float(sr)

# plt.subplot(2, 2, 3)
# plt.plot(t2, y2)
# plt.xlabel('t2')
# plt.ylabel('y2')

frq2, X2 = frequency_spectrum(y2, sr)

# plt.subplot(2, 2, 4)
plt.plot(frq1, X1, 'b',frq2, X2, 'r',alpha=0.5)
plt.xlabel('Freq (Hz)')
plt.ylabel('|X(freq)|')
# plt.xlabel('Freq2 (Hz)')
# plt.ylabel('|X(freq2)|')
plt.tight_layout()

plt.show()
        

app = SeaofBTCapp()
app.mainloop()

        


