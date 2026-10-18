import pyttsx3

def setupTts(rate=250):
    """Initializes the text-to-speech engine."""
    global engine
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    
    # Optional: Select a voice (index 0 for male/default, index 1 for alternative)
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)

def startTts(text):
    """Speaks out the provided text string."""
    if not text:
        return
    print(f"Jarvis: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")