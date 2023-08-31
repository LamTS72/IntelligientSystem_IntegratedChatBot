import os
import playsound
import pyttsx3
import speech_recognition as sr
from gtts import gTTS


def text2speech(text, language):
    print("ChatBot:  ", text)
    langs = ""
    if language is True:
        langs = "vi"
    else:
        langs = "en"
    try:
        tts = gTTS(text=text, lang=langs, slow=False)
        tts.save("sound.mp3")
        playsound.playsound("sound.mp3", True)
        os.remove("sound.mp3")
    except Exception as ex:
        text2_speech(text, language)

def text2_speech(text, language):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume - 0.0)  # tu 0.0 -> 1.0
    engine.setProperty('rate', rate - 50)
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def get_audio(languages):
    if languages is True:
        langs = "vi-VN"
    else:
        langs = "en-IN"
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        audio = ear_robot.record(source, duration=8)
        #audio = ear_robot.listen(source, phrase_time_limit=8)
        try:

            text = ear_robot.recognize_google(audio, language=langs)
            print("You:  ", text)
            return text
        except Exception as ex:
            string_speak = ""
            if languages is True:
                string_speak = "Có vấn đề gì đó với server, hãy thử lại"
            else:
                string_speak = "Have some problems with server , please try again"
            print(string_speak)
            text2speech(string_speak, languages)
            return 0
