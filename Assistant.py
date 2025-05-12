#!/usr/bin/env python3
"""
Intelligent Voice Assistant with modular design and advanced features

Features:
- Voice recognition and text-to-speech
- Wikipedia searches
- Website opening
- Email sending with secure credentials
- Current time and date information
- Music playing
- Application launching
- Weather, news and jokes from external APIs
- ChatGPT integration for answering questions
- Task reminder system
- Memory system using JSON files
- Hotword activation
"""

import os
import sys
import time
import threading
import wikipedia
import pywhatkit
from datetime import datetime

# Import our modules
from speech import SpeechEngine
from utils import get_greeting, get_current_time, get_current_date, open_website, open_application
from memory import Memory
from reminders import ReminderSystem
from api_services import APIServices
from email_service import EmailService
import config

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant"""
        print(f"Initializing {config.ASSISTANT_NAME}...")
        
        # Initialize components
        self.speech = SpeechEngine()
        self.memory = Memory()
        self.apis = APIServices()
        self.email = EmailService()
        self.reminders = ReminderSystem(self.speech.speak)
        
        # Start reminder checking in background
        self.reminders.start()
        
        # Set running state
        self.is_running = False
        self.is_listening_for_wake_word = False
        
    def start(self):
        """Start the voice assistant"""
        self.is_running = True
        self.wish_user()
        
        # Start main loop
        while self.is_running:
            success, query = self.speech.listen()
            
            if success:
                self.process_command(query)
            else:
                # If error is not just timeout
                if query != "Timeout":
                    self.speech.speak("I couldn't understand. Please try again.")
    
    def start_with_hotword(self):
        """Start with hotword activation mode"""
        self.is_listening_for_wake_word = True
        self.speech.speak(f"I'm ready. Say '{config.WAKE_WORD}' to activate me.")
        
        while self.is_listening_for_wake_word:
            if self.speech.listen_for_wake_word():
                self.speech.speak("I'm listening.")
                success, query = self.speech.listen()
                
                if success:
                    self.process_command(query)
                else:
                    if query != "Timeout":
                        self.speech.speak("I couldn't understand. Please try again.")
            
            # Prevent high CPU usage
            time.sleep(0.1)
    
    def wish_user(self):
        """Greet the user based on time of day"""
        greeting = get_greeting()
        self.speech.speak(f"{greeting} I am {config.ASSISTANT_NAME}, your personal voice assistant.")
        self.speech.speak("How may I help you today?")
    
    def process_command(self, query):
        """Process user commands"""
        # Store in memory
        response = ""
        
        # Check for custom commands first
        custom_action = self.memory.get_custom_command(query)
        if custom_action:
            self.speech.speak(f"Executing custom command: {query}")
            response = f"Executed custom command: {custom_action}"
            # Here you could implement custom command execution
            
        # Wikipedia search
        elif 'wikipedia' in query:
            self.speech.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query.strip(), sentences=2)
                self.speech.speak("According to Wikipedia")
                print(results)
                self.speech.speak(results)
                response = results
            except Exception as e:
                response = f"Error searching Wikipedia: {str(e)}"
                self.speech.speak(response)
        
        # Website opening commands
        elif 'open youtube' in query:
            self.speech.speak("Opening YouTube")
            open_website("youtube.com")
            response = "Opened YouTube"
            
        elif 'open google' in query:
            self.speech.speak("Opening Google")
            open_website("google.com")
            response = "Opened Google"
            
        elif 'open stackoverflow' in query:
            self.speech.speak("Opening Stack Overflow")
            open_website("stackoverflow.com")
            response = "Opened Stack Overflow"
            
        # Time and date commands
        elif 'the time' in query:
            time_str = get_current_time()
            self.speech.speak(f"The current time is {time_str}")
            response = f"Current time: {time_str}"
            
        elif 'the date' in query or 'today\'s date' in query:
            date_str = get_current_date()
            self.speech.speak(f"Today is {date_str}")
            response = f"Current date: {date_str}"
            
        # Application commands
        elif 'open code' in query or 'open visual studio code' in query:
            self.speech.speak("Opening Visual Studio Code")
            success = open_application(config.VS_CODE_PATH)
            response = "Opened Visual Studio Code" if success else "Failed to open VS Code"
            
        # Music commands
        elif 'play music' in query or 'play a song' in query:
            try:
                if 'play music' in query and len(query.split()) > 2:
                    song = query.replace('play music', '').strip()
                    self.speech.speak(f"Playing {song} on YouTube")
                    pywhatkit.playonyt(song)
                    response = f"Playing {song} on YouTube"
                else:
                    music_dir = config.MUSIC_DIR
                    if os.path.exists(music_dir) and os.path.isdir(music_dir):
                        songs = os.listdir(music_dir)
                        if songs:
                            os.startfile(os.path.join(music_dir, songs[0]))
                            self.speech.speak(f"Playing {songs[0]}")
                            response = f"Playing {songs[0]}"
                        else:
                            self.speech.speak("No music files found")
                            response = "No music files found"
                    else:
                        self.speech.speak("Music directory not found")
                        response = "Music directory not found"
            except Exception as e:
                self.speech.speak(f"Error playing music: {str(e)}")
                response = f"Error playing music: {str(e)}"
                
        # Email commands
        elif 'send email' in query or 'send an email' in query:
            # Get recipient
            self.speech.speak("Who would you like to send the email to?")
            success, recipient = self.speech.listen()
            
            if success:
                # Try to get contact from memory
                email_addr = self.memory.get_contact(recipient)
                
                if not email_addr:
                    self.speech.speak(f"I don't have {recipient}'s email address. Please provide it.")
                    success, email_addr = self.speech.listen()
                    if not success:
                        self.speech.speak("Sorry, I couldn't understand the email address.")
                        response = "Failed to get email address"
                        return
                
                # Get subject
                self.speech.speak("What should be the subject of the email?")
                success, subject = self.speech.listen()
                if not success:
                    self.speech.speak("Sorry, I couldn't understand the subject.")
                    response = "Failed to get email subject"
                    return
                
                # Get content
                self.speech.speak("What should I say in the email?")
                success, content = self.speech.listen()
                if not success:
                    self.speech.speak("Sorry, I couldn't understand the content.")
                    response = "Failed to get email content"
                    return
                
                # Send email
                success, message = self.email.send_email(email_addr, subject, content)
                self.speech.speak(message)
                response = message
                
                # Save contact if new
                if success and not self.memory.get_contact(recipient):
                    self.memory.add_contact(recipient, email_addr)
            else:
                self.speech.speak("Sorry, I couldn't understand the recipient.")
                response = "Failed to get email recipient"
        
        # Weather command
        elif 'weather' in query:
            # Extract city
            city = "New York"  # Default
            if 'in' in query:
                city = query.split('in')[1].strip()
            
            self.speech.speak(f"Getting weather for {city}")
            success, weather_info = self.apis.get_weather(city)
            self.speech.speak(weather_info)
            response = weather_info
            
        # News command
        elif 'news' in query:
            category = "general"  # Default
            if 'business' in query: category = "business"
            elif 'technology' in query: category = "technology"
            elif 'entertainment' in query: category = "entertainment"
            elif 'sports' in query: category = "sports"
            elif 'science' in query: category = "science"
            elif 'health' in query: category = "health"
            
            self.speech.speak(f"Getting {category} news")
            success, news_info = self.apis.get_news(category)
            self.speech.speak(news_info)
            response = news_info
            
        # Joke command
        elif 'joke' in query or 'tell me a joke' in query:
            self.speech.speak("Here's a joke for you")
            success, joke = self.apis.get_joke()
            self.speech.speak(joke)
            response = joke
            
        # Reminder commands
        elif 'reminder' in query or 'remind me' in query:
            if 'set a reminder' in query or 'remind me' in query:
                # Getting reminder details
                self.speech.speak("What should I remind you about?")
                success, title = self.speech.listen()
                if not success:
                    self.speech.speak("Sorry, I couldn't understand the reminder title.")
                    response = "Failed to get reminder title"
                    return
                
                self.speech.speak("When should I remind you? Please specify the date and time in YYYY-MM-DD HH:MM format.")
                success, datetime_str = self.speech.listen()
                if not success:
                    self.speech.speak("Sorry, I couldn't understand the date and time.")
                    response = "Failed to get reminder date/time"
                    return
                
                self.speech.speak("Any additional notes for this reminder?")
                success, note = self.speech.listen()
                note = note if success else ""
                
                success = self.reminders.add_reminder(title, datetime_str, note)
                if success:
                    self.speech.speak(f"Reminder set for {datetime_str}: {title}")
                    response = f"Reminder set for {datetime_str}: {title}"
                else:
                    self.speech.speak("Failed to set reminder. Please provide date and time in YYYY-MM-DD HH:MM format.")
                    response = "Failed to set reminder"
            
            elif 'list reminders' in query or 'show reminders' in query or 'my reminders' in query:
                reminders = self.reminders.get_reminders()
                if reminders:
                    self.speech.speak(f"You have {len(reminders)} reminders:")
                    for i, reminder in enumerate(reminders):
                        self.speech.speak(f"{i+1}. {reminder['title']} at {reminder['due_date']}")
                    response = f"Listed {len(reminders)} reminders"
                else:
                    self.speech.speak("You don't have any active reminders.")
                    response = "No active reminders"
        
        # Memory commands
        elif 'remember this' in query:
            self.speech.speak("What would you like me to remember?")
            success, memory_text = self.speech.listen()
            if success:
                self.speech.speak("How should I categorize this memory?")
                success, category = self.speech.listen()
                category = category if success else "general"
                
                self.memory.set_preference(category, memory_text)
                self.speech.speak(f"I'll remember that {category}: {memory_text}")
                response = f"Stored memory: {category}: {memory_text}"
            else:
                self.speech.speak("Sorry, I couldn't understand what to remember.")
                response = "Failed to store memory"
        
        elif 'what do you remember about' in query or 'recall' in query:
            category = query.replace('what do you remember about', '').replace('recall', '').strip()
            memory_text = self.memory.get_preference(category)
            
            if memory_text:
                self.speech.speak(f"I remember that {category}: {memory_text}")
                response = f"Retrieved memory: {category}: {memory_text}"
            else:
                self.speech.speak(f"I don't have any memory about {category}")
                response = f"No memory found for: {category}"
        
        # Voice settings
        elif 'change voice' in query:
            current_voice = self.memory.get_preference('voice_id', 0)
            new_voice = 1 if current_voice == 0 else 0
            self.speech.set_voice(new_voice)
            self.memory.set_preference('voice_id', new_voice)
            self.speech.speak("I've changed my voice. How does this sound?")
            response = f"Changed voice to ID: {new_voice}"
        
        # Hot word settings
        elif 'enable hot word' in query or 'use wake word' in query:
            self.speech.speak(f"Enabling hot word activation. Say '{config.WAKE_WORD}' to activate me.")
            response = "Enabled hot word activation"
            self.is_running = False
            threading.Thread(target=self.start_with_hotword, daemon=True).start()
        
        # Exit command
        elif 'terminate' in query or 'exit' in query or 'quit' in query or 'goodbye' in query:
            self.speech.speak("Goodbye! Have a great day!")
            response = "Terminated voice assistant"
            self.is_running = False
            self.is_listening_for_wake_word = False
            self.reminders.stop()
            sys.exit()
        
        # If none of the specific commands matched, use Llama 3
        else:
            self.speech.speak("Let me think about that...")
            success, answer = self.apis.ask_chatgpt(query)
            if success:
                self.speech.speak(answer)
                response = answer
            else:
                self.speech.speak("I'm sorry, I couldn't find an answer to that.")
                response = "Failed to get response from Llama 3"
        
        # Store conversation in memory
        if query and response:
            self.memory.add_conversation(query, response)


if __name__ == "__main__":
    # Create a .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Warning: .env file not found. See .env.example for required environment variables.")
    
    assistant = VoiceAssistant()
    
    # Check command line arguments for hotword activation
    if len(sys.argv) > 1 and sys.argv[1] == "--hotword":
        assistant.start_with_hotword()
    else:
        assistant.start()
