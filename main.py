from gradio_client import Client
import requests
import pygame
import io

client = Client("https://facebook-musicgen--nnzbb.hf.space/")
result = client.predict(
    "Today is a bad day!",
    "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",
    fn_index=0
)

# Assuming the API returns the audio data directly as bytes
generated_music_data = result['generated_music']

# Play the generated music using pygame
pygame.mixer.init()
generated_music_stream = io.BytesIO(generated_music_data)
pygame.mixer.music.load(generated_music_stream)
pygame.mixer.music.play()

# Keep the script running while the music is playing
while pygame.mixer.music.get_busy():
    continue
