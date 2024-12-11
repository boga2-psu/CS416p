#include "kiss_fft.h"
#include <stdint.h>
#include <stdlib.h>

// Define FFT size (must be a power of 2)
#define FFT_SIZE 1024

// Function to perform FFT and compute bass energy
float compute_bass_energy(int16_t* audio_samples, int num_samples) {
    // Allocate memory for FFT configuration
    kiss_fft_cfg cfg = kiss_fft_alloc(FFT_SIZE, 0, NULL, NULL);
    if (!cfg) {
        return -1;  // Memory allocation failure
    }

    kiss_fft_cpx in[FFT_SIZE];
    kiss_fft_cpx out[FFT_SIZE];

    // Convert input audio to complex input format
    for (int i = 0; i < FFT_SIZE; i++) {
        if (i < num_samples) {
            in[i].r = (float)audio_samples[i]; // Real part
            in[i].i = 0.0;                    // Imaginary part
        } else {
            in[i].r = in[i].i = 0.0;          // Pad with zeros
        }
    }

    // Perform FFT
    kiss_fft(cfg, in, out);

    // Calculate magnitude and sum energy in bass range
    float bass_energy = 0.0;
    int low_idx = 20 * FFT_SIZE / 20000;  // Assuming 44.1 kHz sampling rate
    int high_idx = 200 * FFT_SIZE / 20000;
    for (int i = low_idx; i <= high_idx; i++) {
        bass_energy += (out[i].r * out[i].r) + (out[i].i * out[i].i);
    }

    // Free FFT configuration memory
    free(cfg);

    return bass_energy;
}