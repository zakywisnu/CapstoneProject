import scipy.io.wavfile

sample_rate, signal2 = scipy.io.wavfile.read('1_0_1.wav')
print(sample_rate)
