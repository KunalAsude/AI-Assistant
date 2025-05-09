"""
Utility functions for the voice assistant
"""
import datetime
import os
import json
import webbrowser
from typing import Dict, List, Any, Optional

def get_current_time() -> str:
    """Returns current time in HH:MM format"""
    return datetime.datetime.now().strftime("%H:%M")

def get_current_date() -> str:
    """Returns current date in Day, Month Date Year format"""
    return datetime.datetime.now().strftime("%A, %B %d %Y")

def get_greeting() -> str:
    """Returns appropriate greeting based on time of day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return 'Good Morning!'
    elif 12 <= hour < 18:
        return 'Good Afternoon!'
    else:
        return 'Good Evening!'

def open_website(url: str) -> None:
    """Opens the specified website in default browser"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    webbrowser.open(url)

def open_application(path: str) -> bool:
    """Opens an application at the specified path"""
    try:
        os.startfile(path)
        return True
    except Exception as e:
        print(f"Error opening application: {e}")
        return False

def save_to_json(data: Dict, filepath: str) -> bool:
    """Saves dictionary data to a JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False

def load_from_json(filepath: str) -> Optional[Dict]:
    """Loads data from a JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading from JSON: {e}")
        return {}

def extract_name_from_query(query: str) -> Optional[str]:
    """Extract name from a query like 'email to John'"""
    words = query.split()
    if len(words) >= 3 and words[-2] == "to":
        return words[-1]
    return None
