import simpleaudio as sa
import time
def play_error_sound():
    try:
        wave_obj = sa.WaveObject.from_wave_file('test-8000Hz-le-2ch-1byteu.wav')  # Replace with your actual sound file path
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing
    except Exception as e:
        print(f"Error while playing sound: {e}")

# Call this function when an error occurs
while True:
    play_error_sound()
