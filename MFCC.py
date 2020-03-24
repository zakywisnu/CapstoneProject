
# For math/pre-processing -> extract-features
import numpy as np
import scipy.io.wavfile
from scipy.fftpack import dct
from sklearn.preprocessing import minmax_scale

class MFCC_process(object):
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
        mfccs = minmax_scale(mfccs)
        return mfccs.T
