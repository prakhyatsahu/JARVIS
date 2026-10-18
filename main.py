import importlib
from types import SimpleNamespace
import datetime
import os
import sys
import random
import cv2
import webbrowser
import psutil
import pyjokes
import pyautogui
import wolframalpha

# Custom module imports
from playsounds import startPlayAudio
from text2speech import setupTts, startTts
from speech2text import startStt
import take_screenshot
import tell_joke
import take_notes
import power_options
import greet_startup
import get_weather
import check_hardware
import wolfram
import google_calendar
from playmusic import *

# Global variables
asset_path = "C:\\Users\\skili\\Documents\\GitHub\\J.A.R.V.I.S\\assets"
WAKE_CMD = "jarvis"
CITY = "gorakhpur"
INIT_SEQ = True

def randomize(l):
    if not l:
        return ""
    return l[random.randint(0, len(l) - 1)]

def init():
    setupTts(250)
    try:
        wolfram.setupWolfram()
        google_calendar.setupCalendar()
    except Exception:
        pass
    startPlayAudio(os.path.join(asset_path, 'jarvisworking.wav'))
    startTts(greet_startup.greet())
    startTts(get_weather.weather(CITY))
    startTts("All systems nominal. Call me if you need me.")

def matchCommand(CMD):
    if not CMD:
        return

    if 'play music' in CMD:
        startTts("Playing music sir.")
        startPlaymusic(os.path.join(asset_path, "music"))
    elif 'stop music' in CMD:
        stopMusic()
    elif 'open youtube' in CMD:
        webbrowser.open('https://youtube.com')
    elif 'open google' in CMD:
        webbrowser.open('https://google.com')
    elif 'battery' in CMD:
        startTts(check_hardware.getbattery())
    elif 'ram' in CMD or 'memory' in CMD:
        startTts(check_hardware.getram())
    elif 'screenshot' in CMD:
        startTts("Taking screenshot")
        take_screenshot.takeScreenshot(str(random.randint(0, 99999)), os.path.join(asset_path, "screenshots"))
    elif 'shutdown' in CMD:
        startTts("Shutting down the system sir.")
        power_options.shutdown()
    else:
        try:
            wolfram_result = wolfram.startWolfram(CMD)
            if wolfram_result is None:
                startTts("Sorry sir, I could not understand that query.")
            else:
                startTts(str(wolfram_result))
        except Exception:
            startTts("Query processing failed.")

def wakeUpJARVIS():
    if INIT_SEQ:
        init()
    while True:
        wake = startStt()
        if wake and WAKE_CMD in wake.lower():
            CMD = wake.lower().replace(WAKE_CMD, "").strip()
            matchCommand(CMD)

if __name__ == '__main__':
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('./Face-Recognition/trainer/trainer.yml')
        faceCascade = cv2.CascadeClassifier("./Face-Recognition/haarcascade_frontalface_default.xml")
        
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)

        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        face_recognized = False
        print("Initializing Optical Face Recognition...")

        while not face_recognized:
            ret, img = cam.read()
            if not ret:
                break
            converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(converted_image, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

            for (x, y, w, h) in faces:
                id_predicted, accuracy = recognizer.predict(converted_image[y:y+h, x:x+w])
                if accuracy < 100:
                    print("Face Recognized!")
                    cam.release()
                    cv2.destroyAllWindows()
                    face_recognized = True
                    wakeUpJARVIS()
                    break
                else:
                    print("Face mismatch. Access denied.")
                    cam.release()
                    cv2.destroyAllWindows()
                    break
        
        if not face_recognized:
            wakeUpJARVIS()

    except Exception as e:
        print(f"Face recognition skipped (missing files/camera): {e}")
        wakeUpJARVIS()