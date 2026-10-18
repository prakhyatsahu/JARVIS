from playsound import playsound
import os

def startPlayAudio(filename):
    """
    Plays an audio file using the playsound library.
    """
    try:
        if os.path.exists(filename):
            # playsound handles playback directly
            playsound(filename)
        else:
            print(f"Audio file {filename} not found.")
    except Exception as e:
        print(f"Error playing audio: {e}")