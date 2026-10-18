import os
import random
import winsound

def startPlaymusic(asset_path):
    """
    Selects and plays a random track from the music folder.
    """
    try:
        files = [f for f in os.listdir(asset_path) if f.lower().endswith(('.wav', '.mp3'))]
        if not files:
            print("No music files found in the directory.")
            return
        
        chosen_file = os.path.join(asset_path, files[random.randint(0, len(files) - 1)])
        
        if chosen_file.endswith('.wav'):
            winsound.PlaySound(chosen_file, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            os.startfile(chosen_file)
            
    except Exception as e:
        print(f"Error playing music: {e}")

def stopMusic():
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except Exception:
        pass

def pauseMusic():
    stopMusic()
    
def unpauseMusic():
    print("Please play music again.")