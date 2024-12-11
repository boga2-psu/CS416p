import network
import socket
import time
import machine
import struct
import ulab
import math
from machine import Pin
from time import sleep

# This value was decided through qualitative testing
BASS_THRESHOLD = 2200

ssid = 'Sorry you dont get my network name'
password = 'Or the password to it'

gpio_pin = machine.Pin(7, machine.Pin.OUT)

def connect():
    #Connects to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print('Waiting for connection...')
    while wlan.isconnected() == False:
        print('...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')


# Creates the HTTP server
def start_server():
    pico_ip = '192.168.1.105'
    pico_port = 8080

    # Create a socket and bind to the IP and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((pico_ip, pico_port))
    server_socket.listen(1)

    print(f"Server listening on {pico_ip}:{pico_port}")

    while True:
        # Accepts a client connection
        client_socket, addr = server_socket.accept()
        print(f"Client connected from {addr}")

        # Receive the audio data in chunks
        with open("received_audio.wav", "wb") as audio_file:
            while True:
                data = client_socket.recv(1024)  # Receive data in chunks
                if not data:
                    break  # No more data
                data = client_socket.recv(1024)  # Receive data in chunks
                process_audio(data)
        
        client_socket.close()

# Finds the next power of 2 greater than or equal to n
# This makes sure the audio samples are always a power of two
def next_power_of_two(n):
    power = 1
    while power < n:
        power *= 2
    return power

# Process the incoming audio samples
def process_audio(data):
    # Puts the datastream into an array for processing
    # We expect samples are signed 16-bit PCM
    num_samples = len(data) // 2 
    pcm_samples = struct.unpack('<' + 'h' * num_samples, data)
    audio_samples = ulab.numpy.array(pcm_samples)

    desired_length = next_power_of_two(len(audio_samples))
    if len(audio_samples) < desired_length:
        padding = ulab.numpy.zeros(desired_length - len(audio_samples))
        audio_samples = ulab.numpy.concatenate((audio_samples, padding))

    # Applies the FFT to the signal for processing
    fft_result = ulab.numpy.fft.fft(audio_samples)
    bass_frequencies = fft_result[0:10]  

    # Calculates the energy in the bass frequencies (sum of magnitudes)
    bass_energy = ulab.numpy.sqrt(ulab.numpy.sum(ulab.numpy.array([abs(x) for x in bass_frequencies])))
    print("Bass Energy:", bass_energy)

    # Compares the energy to the threshold (value set arbitrarily based on testing)
    # If the energy is higher than the threshold the pin gets set to high and the elctomagnet is turned on
    if bass_energy > BASS_THRESHOLD:
        gpio_pin.on()
    else:
        gpio_pin.off()


try:
    connect()
    start_server()
except KeyboardInterrupt:
    machine.reset()
