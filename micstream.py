import audioop
import math
from struct import pack
from sys import byteorder

from sklearn.externals import joblib
from MFCC import MFCC_process
import pyaudio
import wave
import numpy as np
from array import array


class Streaming(object):
    def __init__(self):
        self.mfcc_feature = MFCC_process()
        RATE = 16000
        CHANNELS = 1
        FORMAT = pyaudio.paInt16
        CHUNK_SIZE = 1024
        INDEX = 2

        self.audio_instance = pyaudio.PyAudio()
        self._channels = CHANNELS
        self._chunk = CHUNK_SIZE
        self._bits = FORMAT
        self._rate = RATE
        self._index = INDEX
        self._threshold = np.around(self.audio_int() + 1000, 0)

    def audio_int(self, num_sample=50):

        p = pyaudio.PyAudio()

        stream = p.open(format=self._bits,
                        channels=self._channels,
                        rate=self._rate,
                        input=True,
                        frames_per_buffer=self._chunk)
        values = [math.sqrt(abs(audioop.avg(stream.read(self._chunk), 4)))
                  for x in range(num_sample)]
        r = sum(values[:int(num_sample * 0.2)]) / int(num_sample * 0.2)
        stream.close()
        p.terminate()
        return r

    def is_silent(self, snd_data):
        return max(snd_data) < self._threshold

    def normalize(self, snd_data):
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self._threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in range(int(seconds * self._rate))])
        r.extend(snd_data)
        r.extend([0 for i in range(int(seconds * self._rate))])
        return r

    def record(self):
        self.stream = self.audio_instance.open(format=self._bits,
                                               channels=self._channels,
                                               rate=self._rate,
                                               input=True,
                                               frames_per_buffer=self._chunk)
        num_silent = 0
        snd_started = False
        self.r = array('h')

        while True:
            # little endian, signed short
            snd_data = array('h', self.stream.read(self._chunk))
            if byteorder == 'big':
                snd_data.byteswap()
            self.r.extend(snd_data)

            silent = self.is_silent(snd_data)

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True
                print('merekam')
            if snd_started and num_silent > 30:
                break

        sample_width = self.audio_instance.get_sample_size(self._bits)
        self.stream.stop_stream()
        self.stream.close()

        self.r = self.normalize(self.r)
        self.r = self.trim(self.r)
        self.r = self.add_silence(self.r, 1)

        self.filename = 'temp1.wav'
        signal = self.record_to_file(self.filename, sample_width, self.r)
        return signal

    def record_to_file(self, path, sample_width, data):

        data = pack('<' + ('h' * len(data)), *data)
        wf = wave.open(path, 'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self._rate)
        wf.writeframes(data)
        wf.close()
        print("Done Recording..")
        return self.filename

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio_instance.terminate()

    def features_extract(self, file):
        features = np.empty((0, 13))
        features = self.mfcc_feature.mfcc(file)
        features = np.array(features)  # Features of real time (test) data
        features = features.reshape(1, -1)  # (-1,1) utk single feature, (1,-1) utk single sample
        return features

    def listening(self, signal):
        features = self.features_extract(signal)
        threshold = 3.38  # utk clf.joblib, ovr.joblib

        clf = joblib.load('best_clf.joblib')  # Call classifier here
        response = clf.predict(features)
        print("Predicted: ")
        print(response)
        return response
