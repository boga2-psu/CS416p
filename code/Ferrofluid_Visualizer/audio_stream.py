import socket
import time
import pygame

# Server details (Pico's IP address and port)
pico_ip = '192.168.1.105'
pico_port = 8080

# Hard coded audio path
audio_file_path = "./wavs/collectathon.wav"

# Hard coded sample rate
sample_rate = 25000

# Establishes a socket connection with Pico
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((pico_ip, pico_port))

# Open and play the audio file while streaming
pygame.mixer.init()
with open(audio_file_path, 'rb') as audio_file:
    print(f"Starting to stream and playback {audio_file_path}...")

    # Sends 1 initial chunk to help with startup lag
    chunk_size = 1024
    for _ in range(2):
        chunk = audio_file.read(chunk_size)
        if not chunk:
            break
        client_socket.sendall(chunk)

    # Sleeps for 1 second and  80 milliseconds to let the streaming buffer ahead of the playback
    # This value was found arbitrarily to work the best through qualitative testing
    time.sleep(1.08)

    # Starts audio playback
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    # Keeps track of the total bytes sent
    total_sent = 0
    prev_time = time.time()

    while True:
        # Gets the current playback position in milliseconds
        current_playback_pos = pygame.mixer.music.get_pos()

        # Converts the current playback from milliseconds to samples
        current_playback_samples = (current_playback_pos / 1000) * sample_rate  
        current_playback_bytes = int(current_playback_samples * 2) 

        # Send the next chunk of data to Pico
        chunk = audio_file.read(chunk_size)

        if not chunk:
            break

        # Send the chunk to Pico
        client_socket.sendall(chunk)

        # If the playback is ahead of the streaming, we can skip some chunks to stay in sync
        if current_playback_bytes > total_sent:
            skip_bytes = current_playback_bytes - total_sent
            skip_chunks = skip_bytes // chunk_size
            for _ in range(skip_chunks):
                audio_file.read(chunk_size)  # Skip enough chunks to stay in sync
                total_sent += chunk_size  # Update total_sent to reflect skipped data

        # Update total bytes sent
        total_sent += len(chunk)

client_socket.close()