"""
Memory system for the voice assistant
"""
import json
import os
from typing import Dict, List, Any, Optional
import config
from utils import save_to_json, load_from_json

class Memory:
    def __init__(self):
        """Initialize the memory system"""
        self.memory_file = config.MEMORY_FILE
        self.memory = self._load_memory()
        
    def _load_memory(self) -> Dict:
        """Load memory from file or create a new memory structure"""
        memory = load_from_json(self.memory_file)
        if not memory:
            memory = {
                "user_preferences": {},
                "conversations": [],
                "contacts": {},
                "custom_commands": {}
            }
            self._save_memory(memory)
        return memory
    
    def _save_memory(self, memory: Optional[Dict] = None) -> bool:
        """Save memory to file"""
        if memory is None:
            memory = self.memory
        return save_to_json(memory, self.memory_file)
    
    def add_conversation(self, query: str, response: str) -> None:
        """Add a conversation exchange to memory"""
        if 'conversations' not in self.memory:
            self.memory['conversations'] = []
            
        # Keep only the last 20 conversations
        if len(self.memory['conversations']) > 20:
            self.memory['conversations'].pop(0)
            
        self.memory['conversations'].append({
            "query": query,
            "response": response,
            "timestamp": str(os.path.getmtime(self.memory_file))
        })
        self._save_memory()
    
    def set_preference(self, key: str, value: Any) -> None:
        """Set a user preference"""
        if 'user_preferences' not in self.memory:
            self.memory['user_preferences'] = {}
        self.memory['user_preferences'][key] = value
        self._save_memory()
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        if 'user_preferences' not in self.memory:
            return default
        return self.memory['user_preferences'].get(key, default)
    
    def add_contact(self, name: str, email: str) -> None:
        """Add a contact to memory"""
        if 'contacts' not in self.memory:
            self.memory['contacts'] = {}
        self.memory['contacts'][name.lower()] = email
        self._save_memory()
    
    def get_contact(self, name: str) -> Optional[str]:
        """Get a contact's email from memory"""
        if 'contacts' not in self.memory:
            return None
        return self.memory['contacts'].get(name.lower())
    
    def add_custom_command(self, command: str, action: str) -> None:
        """Add a custom command to memory"""
        if 'custom_commands' not in self.memory:
            self.memory['custom_commands'] = {}
        self.memory['custom_commands'][command.lower()] = action
        self._save_memory()
    
    def get_custom_command(self, command: str) -> Optional[str]:
        """Get a custom command's action from memory"""
        if 'custom_commands' not in self.memory:
            return None
        return self.memory['custom_commands'].get(command.lower())
    
    def get_recent_conversations(self, count: int = 5) -> List[Dict]:
        """Get recent conversations from memory"""
        if 'conversations' not in self.memory:
            return []
        return self.memory['conversations'][-count:]
