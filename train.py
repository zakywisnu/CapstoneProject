# For loading files, directory, etc
import os

from os.path import isdir, join

# For math/pre-processing -> extract-features
import librosa
import csv
import numpy as np
from sklearn.preprocessing import normalize, label_binarize
import scipy.io.wavfile
from scipy.fftpack import dct
import joblib

# Packages for displaying plots
import matplotlib.pyplot as plt

# For splitting data
from sklearn.model_selection import train_test_split

# For classifier
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import minmax_scale

import pandas as pd

#Initialize Path to Training Directory and Testing Directory

# TS_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data/TS_SET' # dataset for testing
# TS_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_new_test' # dataset for testing
TS_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_record/TEST' # dataset for testing

# TR_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_new_train' # dataset for training
TR_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_record/TRAIN' # dataset for training

class Preprocessing(object):

    def mfcc(self,fn):
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
        mfccs = minmax_scale(mfccs)
        return mfccs.T

    def extract_features(self, path, file_ext="*.wav"):
        features = np.empty((0, 13))  # initialize feature vector
        for root, sub, files in os.walk(path, file_ext):  # read all files in said path
            files = sorted(files)
            os.chdir(root)
            for fn in files:
                try:
                    mfccs = self.mfcc(fn)
                    ext_features = np.hstack([mfccs])
                    features = np.vstack([features, ext_features])
                except Exception as e:
                    print("Error encountered while parsing file: ", fn)
                continue
        return features  # return feature vectors

    def label(self, path):
        audio_path = path
        sub_labels = os.listdir(audio_path)
        print(f'Number of labels: {len(sub_labels)}')

        wavs = []
        labels = []
        for label in sub_labels:
            files = os.listdir(audio_path + '/' + label)
            for f in files:
                if not f.endswith('wav'):
                    continue
                wavs.append(f)
                labels.append(label)

        label_num = pd.Categorical(pd.factorize(labels)[0] + 1)
        speech_data = pd.DataFrame({'file': wavs, 'label': labels, 'kategori': label_num})
        speech_data.info()
        print()
        labels = np.array(labels)
        label_num = np.array(label_num)
        return labels, label_num


class Recognizer(object):
    def __init__(self):

        self.tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                                  'C': [1, 10, 100, 1000]},
                                 {'kernel': ['linear'], 'C': [0.01, 0.1, 1, 10, 100, 100, 1000]}]

    def gridSearch(self, X, y, K):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        scores = ['precision', 'recall']

        for score in scores:
            print("# Tuning hyper-parameters for %s" % score)
            print()

            clf = GridSearchCV(svm.SVC(probability=True),
                               self.tuned_parameters, refit= True,cv=K,
                               scoring='%s_macro' % score)
            clf.fit(X_train, y_train)

            print("Best parameters set found on development set:")
            print()
            best_param = clf.best_params_
            print(best_param)
            print()
            print("Grid scores on development set:")
            print()
            means = clf.cv_results_['mean_test_score']
            stds = clf.cv_results_['std_test_score']
            for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
            print()

            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            y_true, y_pred = y_test, clf.predict(X_test)
            print(classification_report(y_true, y_pred))
            print()

        print("Done training")
        best_clf = clf
        joblib.dump(best_clf, 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_record/best_clf.joblib')  # Menyimpan model classifier pada suatu file .joblib.
        return best_clf, best_param

if __name__ == '__main__':
    data = Preprocessing()
    X = data.extract_features(TR_DIR)
    y, y_num = data.label(TR_DIR)

    # Use label_binarize to be multi-label like settings
    y_bin = label_binarize(y, classes=['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan'])
    n_classes = y_bin.shape[1]
    y_test = y_bin

    X_test = data.extract_features(TS_DIR)
    y_test, y_num1 = data.label(TS_DIR)

    # Use label_binarize to be multi-label like settings
    y_bin2 = label_binarize(y_test, classes=['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan', 'sembilan'])

    recognizer = Recognizer()
    K = 10
    grid_search_clf,best_parameter = recognizer.gridSearch(X,y,K)

    print()
    print("Testing Report : ")
    print()
    y_true, y_pred = y_test, grid_search_clf.predict(X_test)
    print(classification_report(y_true, y_pred))
