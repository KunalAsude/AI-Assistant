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

    def listen(self, timeout: int = 8, retries: int = 1) -> Tuple[bool, str]:
        """
        Listen for user input and convert speech to text
        Returns (success, text) tuple
        
        Args:
            timeout: How long to wait for a command (seconds)
            retries: Number of times to retry if recognition fails
        """
        for attempt in range(retries + 1):
            with sr.Microphone() as source:
                print("Listening...")
                # More extensive ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
                # Lower energy threshold to make it more sensitive
                self.recognizer.energy_threshold = 300  # Default is usually 300-500
                try:
                    audio = self.recognizer.listen(source, timeout=timeout)
                    print("Recognizing...")
                    # Try Google first, with both language options
                    try:
                        text = self.recognizer.recognize_google(audio, language=config.LANGUAGE)
                    except:
                        # Fallback to English if regional language fails
                        text = self.recognizer.recognize_google(audio, language="en-US")
                        
                    print(f"User said: {text}")
                    return True, text.lower()
                except sr.WaitTimeoutError:
                    if attempt < retries:
                        print("Timeout, retrying...")
                        continue
                    return False, "Timeout"
                except sr.UnknownValueError:
                    if attempt < retries:
                        print("Could not understand, retrying...")
                        continue
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
