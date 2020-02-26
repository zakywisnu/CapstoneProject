import sys
from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import numpy as np
import time
import tkinter
from tkinter import ttk


class Stream():
    def __init__(self):
        RATE = 16000
        CHANNELS = 1
        FORMAT = pyaudio.paInt16
        CHUNK_SIZE = 1024
        INDEX = 2

        self.pyaudio_instance = pyaudio.PyAudio()
        self._channels = CHANNELS
        self._chunk = CHUNK_SIZE
        self._bits = FORMAT
        self._rate = RATE
        self._index = INDEX
        self._threshold = np.around(self.audio_int() + 1000,0)

    def audio_int(self,num_sample = 200):

        p = pyaudio.PyAudio()

        stream = p.open(format = self._bits,
                        channels = self._channels,
                        rate = self._rate,
                        input = True,
                        frame_per_buffer = self._chunk)
