import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

def low_pass_filter(data, sample_rate, cutoff_freq=200, order=4):
    # Designs the low-pass filter using a Butterworth filter from scipy.signal
    nyquist = 0.5 * sample_rate 
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Apply the filter to the data using lfilter from scipy.signal
    filtered_data = lfilter(b, a, data)
    return filtered_data

def read_wav_file(file_path):
    """I repurposed the function chatGPT gave me from frequency_finder.py in ../FFT"""
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) > 1 and data.shape[1] > 1:
        data = np.mean(data, axis=1)
    return data, sample_rate

def write_low_wav(file_path, data, sample_rate):
    wavfile.write(file_path, sample_rate, np.int16(data))

def main():
    input_file_path = "./wavs/collectathon.wav"
    output_file_path = "./wavs/collectathon-muffled.wav"

    data, sample_rate = read_wav_file(input_file_path)
    filtered_data = low_pass_filter(data, sample_rate, cutoff_freq=200)


    write_low_wav(output_file_path, filtered_data, sample_rate)

if __name__ == "__main__":
    main()