import audioop
import math
from struct import pack
from sys import byteorder

from sklearn.externals import joblib
from train import Preprocessing
import pyaudio
import wave
import numpy as np
import threading
import atexit
from array import array

from scipy.fftpack import dct
from sklearn.preprocessing import minmax_scale, label_binarize
import scipy.io.wavfile


class MicrophoneStream(object):
    def __init__(self):
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

    def mfcc(self, fn):
        sample_rate, signal = scipy.io.wavfile.read(fn)  # Read Audio File

        # FILTERING
        preemphasizes_coeff = 0.97  # define pre-emphasizes coefficients
        emphasizes_signal = np.append(signal[0],
                                      signal[1:] - preemphasizes_coeff * signal[:-1])  # Pre-emphasizes Filtering

        # FRAMING
        frame_size = 0.025  # length of each frame measured in samples
        frame_stride = 0.01  # number of samples after the start of the previous frame that the next frame should begin
        frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # convert from sec to samples
        frame_length = int(round(frame_length))
        frame_step = int(round(frame_step))
        signal_len = len(emphasizes_signal)
        num_frames = int(np.ceil(float(np.abs(signal_len - frame_length)) / frame_step))

        pad_signal_len = num_frames * frame_step + frame_length
        z = np.zeros((pad_signal_len - signal_len))
        pad_signal = np.append(emphasizes_signal,
                               z)  # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal

        indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(
            np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
        frames = pad_signal[indices.astype(np.int32, copy=False)]

        # WINDOWING
        frames *= np.hamming(frame_length)

        # FOURIER TRANSFROM
        NFFT = 512
        frames_mag = np.abs(np.fft.rfft(frames, NFFT))  # FFT Magnitude
        frames_pow = ((1.0 / NFFT) * ((frames_mag) ** 2))  # power spectrum

        # FILTER BANKS
        nfilt = 40
        low_freq_mel = 0
        high_freq_mel = (1125 * np.log10(1 + (sample_rate / 2) / 700))
        mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)
        hz_points = (700 * (10 ** (mel_points / 1125) - 1))
        bin = np.floor((NFFT + 1) * hz_points / sample_rate)

        fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
        for m in range(1, nfilt + 1):
            f_m_minus = int(bin[m - 1])  # left
            f_m = int(bin[m])  # center
            f_m_plus = int(bin[m + 1])  # right

            for k in range(f_m_minus, f_m):
                fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
            for k in range(f_m, f_m_plus):
                fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
        filter_banks = np.dot(frames_pow, fbank.T)
        filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
        filter_banks = 20 * np.log10(filter_banks)  # dB

        # MFCC
        num_ceps = 13
        mfccs = dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1: (num_ceps + 1)]  # Keep 1-13
        mfccs = np.mean(mfccs, axis=0)
        mfccs = minmax_scale(mfccs, feature_range=(0, 1))
        return mfccs.T

    def _features(self, file):
        features = np.empty((0, 13))
        features = (self.mfcc(file))
        features = np.array(features)  # Features of real time (test) data
        features = features.reshape(1, -1)  # (-1,1) utk single feature, (1,-1) utk single sample
        return features

    def _listen(self, signal):
        features = self._features(signal)
        threshold = 3.38  # utk clf.joblib, ovr.joblib

        clf = joblib.load('best_clf.joblib')  # Call classifier here
        response = clf.predict(features)
        print("Predicted: ")
        print(response)
        response2 = self.recognize(clf, features, threshold)  # THIS GONNA RETURN THE RESPONSE
        return response, response2

    def adjusted_classes(self, Y, thresh):
        """
        This function adjusts class predictions based on the prediction threshold (t).
        Will only work for binary classification problems.
        """
        n_classes = Y.shape[1]
        for i in range(n_classes):
            for y in Y:
                if y[:][i] >= thresh:
                    y[:][i] = 1
                elif y[:][i] < thresh:
                    y[:][i] = 0
                else:
                    break

    def recognize(self, clf, feature, thresh):
        # class_prob = clf.decision_function(feature)
        class_prob = clf.decision_function(feature)
        self.adjusted_classes(class_prob, thresh)  # Class_prob will change according to the adjusted class
        response = []

        if class_prob[0][0] == 1:
            response = ["nol"]
        elif class_prob[0][1] == 1:
            response = ["satu"]
        elif class_prob[0][2] == 1:
            response = ["dua"]
        elif class_prob[0][3] == 1:
            response = ["tiga"]
        elif class_prob[0][4] == 1:
            response = ["empat"]
        elif class_prob[0][5] == 1:
            response = ["lima"]
        elif class_prob[0][6] == 1:
            response = ["enam"]
        elif class_prob[0][7] == 1:
            response = ["tujuh"]
        elif class_prob[0][8] == 1:
            response = ["delapan"]
        elif class_prob[0][9] == 1:
            response = ["sembilan"]
        else:
            response = ["unknown"]
        return np.array(response)


# if __name__ == "__main__":
#     data = MicrophoneStream()
#     data._listen('0_6.wav')
