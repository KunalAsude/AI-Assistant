"""
Speech recognition and text-to-speech functionality
"""
import pyttsx3
import speech_recognition as sr
from typing import Optional, Tuple
import config

class SpeechEngine:
    def __init__(self):
        """Initialize the speech engine"""
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[config.DEFAULT_VOICE_ID].id)
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = config.PAUSE_THRESHOLD

    def speak(self, text: str) -> None:
        """Convert text to speech and play it"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def set_voice(self, voice_id: int) -> None:
        """Change the voice of the assistant"""
        if voice_id < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_id].id)
            return True
        return False

    def adjust_rate(self, rate: int) -> None:
        """Adjust the speaking rate (default is 200)"""
        self.engine.setProperty('rate', rate)

    def listen(self, timeout: int = 5) -> Tuple[bool, str]:
        """
        Listen for user input and convert speech to text
        Returns (success, text) tuple
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio, language=config.LANGUAGE)
                print(f"User said: {text}")
                return True, text.lower()
            except sr.WaitTimeoutError:
                return False, "Timeout"
            except sr.UnknownValueError:
                return False, "Could not understand audio"
            except sr.RequestError:
                return False, "Could not request results; check your network connection"
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                return False, f"Error: {str(e)}"

    def listen_for_wake_word(self) -> bool:
        """Listen specifically for the wake word"""
        with sr.Microphone() as source:
            print("Listening for wake word...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio, language=config.LANGUAGE).lower()
                print(f"Heard: {text}")
                return config.WAKE_WORD.lower() in text
            except:
                return False
