"""
Llama 3 Integration Service for the Voice Assistant

This module provides integration with Together AI's Llama 3 model for advanced
natural language processing capabilities.
"""

import os
import json
import together
from typing import Dict, List, Optional, Union
import config

class LlamaService:
    def __init__(self):
        """Initialize the Llama 3 service with the Together AI API"""
        self.api_key = config.TOGETHER_API_KEY
        together.api_key = self.api_key
        self.model = config.LLAMA_MODEL
        self.system_prompt = config.SYSTEM_PROMPT
        self.chat_history = []
        
    def reset_chat(self):
        """Reset the chat history"""
        self.chat_history = []
        
    def add_message(self, role: str, content: str):
        """Add a message to the chat history"""
        self.chat_history.append({"role": role, "content": content})
        
    def get_response(self, query: str, system_prompt: Optional[str] = None) -> str:
        """
        Get a response from the Llama 3 model
        
        Args:
            query: The user's query
            system_prompt: Optional custom system prompt to override the default
            
        Returns:
            The model's response as a string
        """
        try:
            # Add user message to history
            self.add_message("user", query)
            
            # Use custom system prompt if provided
            prompt = system_prompt if system_prompt else self.system_prompt
            
            # Use the Together Complete API with the Llama 3 chat format
            formatted_messages = self._format_messages(prompt)
            
            # Complete API call
            response = together.Complete.create(
                model=self.model,
                prompt=self._format_prompt_for_complete(formatted_messages),
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9,
                top_k=50
            )
            
            # Extract response text
            response_text = response['output']['choices'][0]['text']
            
            # Add assistant message to history
            self.add_message("assistant", response_text)
            
            return response_text
            
        except Exception as e:
            print(f"Error in LlamaService.get_response: {str(e)}")
            return f"I encountered an error: {str(e)}"

    def _format_messages(self, system_prompt: str) -> List[Dict[str, str]]:
        """
        Format the messages for the Llama 3 model based on chat history
        
        Args:
            system_prompt: The system prompt to use
            
        Returns:
            Formatted messages list for Together AI Chat API
        """
        # Start with the system message
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add all messages from chat history
        for message in self.chat_history:
            messages.append({
                "role": message["role"],
                "content": message["content"]
            })
            
        return messages
