import sounddevice as sd
import numpy as np
import speech_recognition as sr
import io
import wave

def startStt(duration=5, samplerate=16000):
    """
    Listens to the microphone using sounddevice and converts speech to text.
    """
    print("\nListening for your command...")
    try:
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        wav_io.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
    except Exception as e:
        print(f"Could not understand audio or recognition error: {e}")
        return ""