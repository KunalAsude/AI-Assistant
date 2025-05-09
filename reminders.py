"""
Reminder system for the voice assistant
"""
import json
import os
import datetime
import threading
import time
from typing import Dict, List, Any, Optional, Callable
import config
from utils import save_to_json, load_from_json

class ReminderSystem:
    def __init__(self, callback: Callable[[str], None]):
        """
        Initialize the reminder system
        
        Args:
            callback: Function to call when a reminder is due
        """
        self.reminders_file = config.REMINDERS_FILE
        self.reminders = self._load_reminders()
        self.callback = callback
        self.reminder_thread = None
        self.running = False
        
    def _load_reminders(self) -> List[Dict]:
        """Load reminders from file or create a new reminders list"""
        reminders = load_from_json(self.reminders_file)
        if not isinstance(reminders, list):
            reminders = []
            self._save_reminders(reminders)
        return reminders
    
    def _save_reminders(self, reminders: Optional[List] = None) -> bool:
        """Save reminders to file"""
        if reminders is None:
            reminders = self.reminders
        return save_to_json(reminders, self.reminders_file)
    
    def add_reminder(self, title: str, datetime_str: str, note: str = "") -> bool:
        """
        Add a new reminder
        
        Args:
            title: Title of the reminder
            datetime_str: When the reminder is due in 'YYYY-MM-DD HH:MM' format
            note: Additional notes for the reminder
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            due_date = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            reminder = {
                "id": str(int(time.time())),
                "title": title,
                "due_date": datetime_str,
                "note": note,
                "completed": False
            }
            
            self.reminders.append(reminder)
            self._save_reminders()
            
            # Restart the reminder thread to pick up the new reminder
            if self.running:
                self.stop()
                self.start()
                
            return True
        except Exception as e:
            print(f"Error adding reminder: {e}")
            return False
    
    def remove_reminder(self, reminder_id: str) -> bool:
        """Remove a reminder by ID"""
        for i, reminder in enumerate(self.reminders):
            if reminder.get("id") == reminder_id:
                self.reminders.pop(i)
                self._save_reminders()
                return True
        return False
    
    def mark_completed(self, reminder_id: str) -> bool:
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                self._save_reminders()
                return True
        return False
    
    def get_reminders(self, include_completed: bool = False) -> List[Dict]:
        """Get all reminders"""
        if include_completed:
            return self.reminders
        return [r for r in self.reminders if not r.get("completed", False)]
    
    def get_due_reminders(self) -> List[Dict]:
        """Get reminders that are due now"""
        now = datetime.datetime.now()
        due_reminders = []
        
        for reminder in self.reminders:
            if reminder.get("completed", False):
                continue
                
            try:
                due_date = datetime.datetime.strptime(reminder["due_date"], "%Y-%m-%d %H:%M")
                if due_date <= now:
                    due_reminders.append(reminder)
            except:
                continue
                
        return due_reminders
    
    def _check_reminders(self):
        """Background thread that checks for due reminders"""
        while self.running:
            due_reminders = self.get_due_reminders()
            
            for reminder in due_reminders:
                message = f"Reminder: {reminder['title']}"
                if reminder.get("note"):
                    message += f" - {reminder['note']}"
                
                self.callback(message)
                self.mark_completed(reminder["id"])
            
            # Sleep for 60 seconds before checking again
            time.sleep(60)
    
    def start(self):
        """Start the reminder checking thread"""
        if not self.running:
            self.running = True
            self.reminder_thread = threading.Thread(target=self._check_reminders)
            self.reminder_thread.daemon = True
            self.reminder_thread.start()
    
    def stop(self):
        """Stop the reminder checking thread"""
        self.running = False
        if self.reminder_thread:
            self.reminder_thread.join(timeout=1)
