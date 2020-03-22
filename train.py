# For loading files, directory, etc
import os

from os.path import isdir, join

# For math/pre-processing -> extract-features
import numpy as np
from sklearn.preprocessing import normalize, label_binarize
import scipy.io.wavfile
from scipy.fftpack import dct
import joblib
from MFCC import MFCC_process

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

# TS_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_new/test'  # dataset for testing

TR_DIR = 'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/data_combi'  # dataset for training


class Preprocessing(object):

    def __init__(self):
        self.feature = MFCC_process()

    def extract_features(self, path, file_ext="*.wav"):
        features = np.empty((0, 13))  # initialize feature vector
        for root, sub, files in os.walk(path, file_ext):  # read all files in said path
            files = sorted(files)
            os.chdir(root)
            for fn in files:
                try:
                    mfccs = self.feature.mfcc(fn)
                    # mfccs = self.mfcc(fn)
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
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

        scores = ['precision', 'recall']

        for score in scores:
            print("# Tuning hyper-parameters for %s" % score)
            print()

            clf = GridSearchCV(svm.SVC(probability=True),
                               self.tuned_parameters, cv=K,
                               scoring='%s_macro' % score)
            clf.fit(X_train, y_train)
            print(clf)
            print('Best Score: ', clf.best_score_)
            print('Best C: ', clf.best_estimator_.C)
            print('Best kernel: ', clf.best_estimator_.kernel)

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
        print(best_clf)
        joblib.dump(best_clf,
                    'D:/Zaky/CapstoneProject/ASR/SpeechRecognition/best_clf.joblib')  # Menyimpan model classifier pada suatu file .joblib.
        return best_clf, best_param



if __name__ == '__main__':
    data = Preprocessing()
    X = data.extract_features(TR_DIR)
    y, y_num = data.label(TR_DIR)

    y_bin = label_binarize(y, classes=['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam', 'tujuh', 'delapan',
                                       'sembilan'])
    n_classes = y_bin.shape[1]
    y_test = y_bin

    recognizer = Recognizer()
    K = 10
    grid_search_clf, best_parameter = recognizer.gridSearch(X, y, K)
