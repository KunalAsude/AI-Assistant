"""
External API services for the voice assistant
"""
import requests
import json
import openai
from typing import Dict, List, Any, Optional, Tuple
import config

class APIServices:
    def __init__(self):
        """Initialize API services"""
        openai.api_key = config.OPENAI_API_KEY
        self.weather_api_key = config.WEATHER_API_KEY
        self.news_api_key = config.NEWS_API_KEY
        
    def get_weather(self, city: str) -> Tuple[bool, str]:
        """
        Get current weather for a city
        
        Args:
            city: The city to get weather for
            
        Returns:
            Tuple[bool, str]: Success status and weather information or error message
        """
        if not self.weather_api_key:
            return False, "Weather API key not configured"
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                return False, f"Error: {data.get('message', 'Unknown error')}"
                
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            weather_info = (
                f"The weather in {city} is {weather_desc}. "
                f"Temperature is {temp}°C, humidity is {humidity}%, "
                f"and wind speed is {wind_speed} meters per second."
            )
            
            return True, weather_info
        except Exception as e:
            return False, f"Error fetching weather data: {str(e)}"
    
    def get_news(self, category: str = "general", count: int = 5) -> Tuple[bool, str]:
        """
        Get latest news headlines
        
        Args:
            category: News category (general, business, entertainment, health, science, sports, technology)
            count: Number of headlines to retrieve
            
        Returns:
            Tuple[bool, str]: Success status and news headlines or error message
        """
        if not self.news_api_key:
            return False, "News API key not configured"
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200 or data.get("status") != "ok":
                return False, f"Error: {data.get('message', 'Unknown error')}"
                
            articles = data.get("articles", [])
            if not articles:
                return False, f"No news found for category: {category}"
                
            news_text = f"Here are the top {min(count, len(articles))} {category} news headlines:\n"
            
            for i, article in enumerate(articles[:count]):
                news_text += f"{i+1}. {article['title']}\n"
                
            return True, news_text
        except Exception as e:
            return False, f"Error fetching news data: {str(e)}"
    
    def get_joke(self) -> Tuple[bool, str]:
        """
        Get a random joke
        
        Returns:
            Tuple[bool, str]: Success status and joke or error message
        """
        try:
            url = "https://official-joke-api.appspot.com/random_joke"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code != 200:
                return False, "Error fetching joke"
                
            setup = data.get("setup", "")
            punchline = data.get("punchline", "")
            
            if not setup or not punchline:
                return False, "Invalid joke format received"
                
            joke = f"{setup} ... {punchline}"
            return True, joke
        except Exception as e:
            return False, f"Error fetching joke: {str(e)}"
    
    def ask_chatgpt(self, query: str) -> Tuple[bool, str]:
        """
        Ask a question to ChatGPT
        
        Args:
            query: The question to ask
            
        Returns:
            Tuple[bool, str]: Success status and answer or error message
        """
        if not config.OPENAI_API_KEY:
            return False, "OpenAI API key not configured"
        
        try:
            response = openai.ChatCompletion.create(
                model=config.CHAT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant providing concise answers."},
                    {"role": "user", "content": query}
                ],
                max_tokens=config.MAX_TOKENS,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            return True, answer
        except Exception as e:
            return False, f"Error with ChatGPT: {str(e)}"
