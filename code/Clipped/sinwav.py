import numpy as np
#import sounddevice as sd
from scipy.io import wavfile

amplitude = 8192 #1/4 of 32767 (max for a 16bit signed int)
duration = 1 #seconds
frequency = 440 #hz
sample_rate = 48_000 #samples / sec


t = np.linspace(0, duration, sample_rate, dtype=np.float64, endpoint=False)

# Normal wave
wav = amplitude * np.sin(2 * np.pi * frequency * t)
wav_int16 = wav.astype(np.int16)

wavfile.write('440hz.wav', sample_rate, wav_int16)

# Clipped wave
amplitude = 16384 #1/2 amplitude wave

clipped_wav = amplitude * np.sin(2 * np.pi * frequency * t)
clipped_wav = np.clip(clipped_wav, -8192, 8192)
clipped_wav_int16 = clipped_wav.astype(np.int16

wavfile.write('440hz_clipped.wav', sample_rate, clipped_wav_int16)
