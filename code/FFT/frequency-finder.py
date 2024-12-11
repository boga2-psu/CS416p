import numpy as np
from scipy.io import wavfile
from collections import Counter

"""chatGPT helped me write this function to check if the file is stereo and force mono if it is"""
def read_wav_file(file_path):
    sample_rate, data = wavfile.read(file_path)

    if len(data.shape) > 1 and data.shape[1] > 1:  # Stereo check
        data = np.mean(data, axis=1)

    return sample_rate, np.array(data, dtype=np.float32)

def get_dominant_frequencies(data, sample_rate, window_size):
    # 30% window overlap
    step_size = int(window_size * .7)
    window_count = len(data) // step_size

    dominant_frequencies = []
    
    for i in range(window_count):
        start = i * step_size
        end = start + window_size

        # This creates hanning windows spanning the start to the end of the audio input
        window = data[start:end] * np.hanning(window_size)

        fft_result = np.fft.rfft(window)
        fft_magnitudes = np.abs(fft_result)
        # Returns the maxmimum values of the magnitudes multipled by the sample rate
        # over the window size to find the dominant frequency 
        dominant_frequency = np.argmax(fft_magnitudes) * (sample_rate / window_size)

        # I don't want to count 0hz as a frequency if there was only silence in a window
        if(dominant_frequency > 0):
            dominant_frequencies.append(dominant_frequency)

    return dominant_frequencies

def main():
    file_path = "./wavs/echomorph-nohpf.wav"

    window_size = 1024
    sample_rate, data = read_wav_file(file_path)

    dominant_frequencies = get_dominant_frequencies(data, sample_rate, window_size)

    # Ranks and stores all dominant frequencies before filtering out the top 5 to be printed
    frequency_counter = Counter(dominant_frequencies)
    ranked_frequencies = frequency_counter.most_common(5)

    print("\nTop 5 most common dominant frequencies:")
    for freq, count in ranked_frequencies:
        print(f"Frequency: {freq:.2f} Hz, Count: {count}")

if __name__ == "__main__":
    main()