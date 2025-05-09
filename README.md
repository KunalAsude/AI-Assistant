# AI-Assistant
A modular and intelligent Python-based voice assistant with advanced features

## Features

- **Voice Recognition & Text-to-Speech**: Understands your voice commands and responds with natural speech
- **Wikipedia Search**: Searches Wikipedia and provides summaries
- **Web Browsing**: Opens websites on command
- **Email**: Securely sends emails using environment variables for credentials
- **Time & Date**: Provides current time and date information
- **Music Player**: Plays songs from local directories or YouTube
- **Application Launch**: Opens your favorite applications
- **Weather Updates**: Gets real-time weather information for any city
- **News Updates**: Retrieves latest news by category
- **Jokes**: Tells random jokes for entertainment
- **ChatGPT Integration**: Uses AI to answer questions on any topic
- **Memory System**: Remembers preferences and conversations using JSON files
- **Task Reminders**: Sets and manages reminders
- **Hotword Activation**: Activates with a wake word ("Hey Jarvis")

## Project Structure

- `Assistant.py`: Main script with the core VoiceAssistant class
- `speech.py`: Handles speech recognition and text-to-speech
- `memory.py`: Manages memory storage using JSON
- `reminders.py`: Implements the reminder system
- `api_services.py`: Connects to external APIs (weather, news, jokes, ChatGPT)
- `email_service.py`: Provides secure email functionality
- `utils.py`: Contains utility functions
- `config.py`: Stores configuration settings

## Setup Instructions

### 1. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root directory with the following variables (see `.env.example`):

```
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
NEWS_API_KEY=your_newsapi_api_key_here

# Email Configuration
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here

# Paths
MUSIC_DIR=C:\Music
VS_CODE_PATH=C:\Users\username\AppData\Local\Programs\Microsoft VS Code\Code.exe
```

### 3. Running the Assistant

Start in normal mode:
```bash
python Assistant.py
```

Start with hotword activation:
```bash
python Assistant.py --hotword
```

## Voice Commands

Here are some example commands you can use:

- "Search Wikipedia for artificial intelligence"
- "Open YouTube"
- "What's the time?"
- "What's today's date?"
- "Play music"
- "Play Bohemian Rhapsody"
- "Open Visual Studio Code"
- "Send email"
- "What's the weather in New York?"
- "Tell me the latest news"
- "Tell me a joke"
- "Set a reminder"
- "List my reminders"
- "Remember this"
- "What do you remember about..."
- "Change voice"
- "Enable hot word"

## Customization

You can customize the assistant by modifying the settings in `config.py`:

- Change the assistant name
- Modify the wake word
- Choose a different voice
- Add more application paths

## Dependencies

- pyttsx3: Text-to-speech conversion
- speech_recognition: Speech recognition
- openai: ChatGPT integration
- requests: API calls
- python-dotenv: Environment variable management
- wikipedia: Wikipedia searches
- playsound: Audio playback
- pywhatkit: YouTube music playing
