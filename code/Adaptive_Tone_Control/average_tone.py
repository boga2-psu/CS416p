import numpy as np
from scipy.io import wavfile
from scipy.fft import rfft, irfft


def read_wav_file(file_path):
    """I repurposed the function chatGPT gave me from frequency_finder.py in ../FFT"""
    sample_rate, data = wavfile.read(file_path)
    if len(data.shape) > 1 and data.shape[1] > 1:
        data = np.mean(data, axis=1)
    return data, sample_rate


def write_wav_file(file_path, data, sample_rate):
    wavfile.write(file_path, sample_rate, np.clip(data, -32768, 32767).astype(np.int16))


def process_audio(data, sample_rate, window_size=1024):
    # 30% overlapping windows
    step_size = int(window_size * (.7)) 

    # Calculates the number of windows based on the input length
    num_windows = (len(data) - window_size) // step_size + 1
    output_data = np.zeros_like(data, dtype=np.float64)

    # Frequency band limits (low, mid, high)
    low_band = (0, 300)
    mid_band = (300, 2000)
    # This ends the high band right at the Nyquist frequency
    high_band = (2000, sample_rate // 2)


    for i in range(num_windows):
        start = i * step_size
        end = start + window_size
        window_data = data[start:end] * np.hanning(window_size) 

        # Applies an FFT to get the frequency spectrum
        spectrum = rfft(window_data)
        
        # Generates array of frequencies for bins which match len(spectrum[])
        freqs = np.fft.fftfreq(window_size, 1/sample_rate)[:len(spectrum)]

        # Calculates energy in each band
        low_energy = calculate_band_energy(spectrum, freqs, low_band)
        mid_energy = calculate_band_energy(spectrum, freqs, mid_band)
        high_energy = calculate_band_energy(spectrum, freqs, high_band)

        # Average energy across all bands
        avg_energy = (low_energy + mid_energy + high_energy) / 3

        # Applies tone control to balance the energy
        spectrum = apply_tone_control(spectrum, freqs, avg_energy, low_band)
        spectrum = apply_tone_control(spectrum, freqs, avg_energy, mid_band)
        spectrum = apply_tone_control(spectrum, freqs, avg_energy, high_band)

        # Reconstructs the time-domain signal for this window
        filtered_window = irfft(spectrum)

        # Stores the overlapping filtered windows in the array
        output_data[start:end] += filtered_window

    return output_data.astype(np.int16)


def calculate_band_energy(spectrum, freqs, band_limits):
    # Selects only the frequencies the band covers
    band_mask = (freqs >= band_limits[0]) & (freqs < band_limits[1])

    # Energy is magnitude squared
    band_spectrum = np.abs(spectrum[band_mask])**2  

    return np.mean(band_spectrum)


def apply_tone_control(spectrum, freqs, target_band_energy, band_limits):
    band_energy = calculate_band_energy(spectrum, freqs, band_limits)

    # Scale to match target energy
    scale_factor = np.sqrt(target_band_energy / band_energy)

    # Selects only the frequencies the band covers and scales them to the target
    band_mask = (freqs >= band_limits[0]) & (freqs < band_limits[1])

    # Adjusts the amplitude in the band
    spectrum[band_mask] *= scale_factor 
    return spectrum


def main():
    input_file_path = "./wavs/collectathon.wav"
    output_file_path = "./wavs/leveled_collectathon.wav"

    data, sample_rate = read_wav_file(input_file_path)
    output_data = process_audio(data, sample_rate)

    write_wav_file(output_file_path, output_data, sample_rate)


if __name__ == "__main__":
    main()