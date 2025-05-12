"""
Configuration settings for the voice assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Assistant settings
ASSISTANT_NAME = "Buddy"
DEFAULT_VOICE_ID = 0  # 0 for male, 1 for female
WAKE_WORD = "hey buddy"

# API Keys (loaded from .env file)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Email settings
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# File paths
MEMORY_FILE = "memory.json"
REMINDERS_FILE = "reminders.json"
MUSIC_DIR = os.getenv("MUSIC_DIR", "C:\\Music")

# Application paths
VS_CODE_PATH = os.getenv("VS_CODE_PATH", "C:\\Users\\kunal\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

# ChatGPT settings
CHAT_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 150

# Voice recognition settings
LANGUAGE = "en-in"
PAUSE_THRESHOLD = 1

# Llama 3 settings (Together AI)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
LLAMA_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
SYSTEM_PROMPT = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question is asked that is nonsensical, controversial, or out-of-scope for the voice assistant, explain why rather than answering the question directly."
