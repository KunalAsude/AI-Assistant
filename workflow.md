# Voice Assistant Workflow Documentation

## System Overview

This document outlines the workflow and interaction between different components of the intelligent voice assistant system.

![Voice Assistant Architecture](https://mermaid.ink/img/pako:eNqNVE1v2zAM_SuETkUyZPaS9JIdOmCHYhja7VAUxWDLdIzKkkfRK4Ki_31Ukq7ptk2LEBmkH4_kI8ldFN0YGMXROVuLlVA0qkBCuYl0mZAusRdZf_ZIQXrr4XqeIsFXtDwkAu0U4G01TU56X6_Xo5H9wLGM4tlotCiwRFPaBNzPYYmiQ1LUkxeYvKDV1TzxPuH-UvFNqRnJr_HL89-J_vL7LDNe3lAe8nWLhjGGxqZZMj0LJXz6Pfm7tO-bBeTH-UKm8fLz0xPb91lxQMq5w8O7wXqvlr5R3X8f0XjdauQ2tSZWqDYVGUfWP4t0gfYYbCfZrfQlJoJ85r8Oj38d_mEzD9bLAaYOvr1mYzuJ_eGHWU-9SYE1PxGbONT_aWbqtMamrIRXWFY-eBrV1SStlcvMgdHYMwDC3DXxmlHGz0rtBaPZFhY3gkR8sEYrWKvARv-n4UFh04a3vKwpxIluCbJ_tNdLZrwUDyQRTw92gvw5OTrvQ3txkWRFAD0OXr4hXN2C-qLNkrklcQRtBcw5sFXF3ORxE5W4DGiCxYXcO8-x8-1oCmGCMUYcBxQeQsaWqswXVPNu9y2dn-4G1DjnhbTJKBFj3K0oihJsYlKrRBBF-BDFmzmHpPMCeOqzE1r6JNm0Rb8t5y6uiTuiKU9ZRxlr2sZcnRmJPYoTQwk5l2Ebgre8G57m3fDsn-Edzx3rH5_uKNyKt5X9Z0JVSzejkR8JNFblUXwXcQ0rLWC21LdwDJYuwYKYVZYrwdjTSEhbFzxCa5l70TDuIrBXZpNhvbOkbIGXWM0rvgMhHjt2b2g_0Q_v_wbWvt4sS5xSLJFnq_vX2lrtHMbS-XT_BlbH_yA)

## Core Components

1. **Main Controller (Assistant.py)**
   - Initializes all components
   - Manages the main interaction loop
   - Processes user commands
   - Coordinates between different modules

2. **Speech Engine (speech.py)**
   - Handles text-to-speech conversion
   - Manages speech recognition
   - Listens for wake words
   - Adjusts for ambient noise

3. **Memory System (memory.py)**
   - Stores user preferences
   - Records conversation history
   - Manages contact information
   - Remembers custom commands

4. **Reminder System (reminders.py)**
   - Schedules and tracks reminders
   - Runs background monitoring thread
   - Notifies when reminders are due
   - Manages reminder completion status

5. **API Services (api_services.py)**
   - Connects to ChatGPT for answering questions
   - Retrieves weather information
   - Fetches news updates
   - Gets random jokes

6. **Email Service (email_service.py)**
   - Manages secure email sending
   - Handles SMTP connection
   - Uses environment variables for credentials

7. **Utilities (utils.py)**
   - Provides helper functions
   - Manages file operations
   - Handles website and application opening

## Workflow Sequence

### 1. Initialization Process

```mermaid
sequenceDiagram
    participant User
    participant Main as Assistant.py
    participant Speech as speech.py
    participant Memory as memory.py
    participant Reminders as reminders.py
    
    User->>Main: Start application
    Main->>Speech: Initialize speech engine
    Main->>Memory: Load saved preferences
    Main->>Reminders: Start reminder checking thread
    Main->>User: Greet user with time-appropriate message
```

### 2. Command Processing

```mermaid
sequenceDiagram
    participant User
    participant Main as Assistant.py
    participant Speech as speech.py
    participant APIs as api_services.py
    participant Memory as memory.py
    
    User->>Speech: Speak command
    Speech->>Main: Convert speech to text
    Main->>Main: Identify command type
    alt Wikipedia Search
        Main->>APIs: Search Wikipedia
        APIs->>Main: Return results
    else Website Opening
        Main->>Utils: Open website
    else Email Sending
        Main->>Email: Send email
    else Weather Request
        Main->>APIs: Get weather data
        APIs->>Main: Return weather info
    else General Question
        Main->>APIs: Query ChatGPT
        APIs->>Main: Return answer
    end
    Main->>Speech: Convert response to speech
    Speech->>User: Speak response
    Main->>Memory: Store interaction
```

### 3. Hotword Activation Mode

```mermaid
sequenceDiagram
    participant User
    participant Main as Assistant.py
    participant Speech as speech.py
    
    Main->>Speech: Start listening for wake word
    User->>Speech: Say "Hey Jarvis"
    Speech->>Main: Wake word detected
    Main->>Speech: Active listening mode
    User->>Speech: Speak command
    Speech->>Main: Process command normally
```

### 4. Reminder Processing

```mermaid
sequenceDiagram
    participant User
    participant Main as Assistant.py
    participant Reminders as reminders.py
    participant Speech as speech.py
    
    User->>Main: "Set a reminder"
    Main->>Speech: Ask for reminder details
    User->>Speech: Provide title, time, notes
    Main->>Reminders: Add reminder to system
    Reminders->>Reminders: Background checking
    Note over Reminders: When reminder is due
    Reminders->>Speech: Notification message
    Speech->>User: Speak reminder alert
```

## Data Flow

### User Interaction Flow
1. User speaks a command
2. Speech recognition converts audio to text
3. Command processor identifies intent
4. Appropriate module handles the request
5. Response is generated
6. Text-to-speech converts response to audio
7. User hears the response
8. Interaction is stored in memory

### Memory Storage Flow
1. User preferences are saved to JSON
2. Conversations are recorded with timestamps
3. Contact information is stored for email functionality
4. Custom commands are saved for future use
5. Memory persists between sessions

## Setup and Requirements

### Environment Setup
1. Install required Python packages
2. Configure environment variables
3. Set up API keys (OpenAI, Weather, News)
4. Configure email credentials
5. Customize assistant settings in config.py

### Running the System
1. Standard mode: `python Assistant.py`
2. Hotword activation: `python Assistant.py --hotword`

## System Requirements

- Python 3.6+
- Internet connection for API services
- Microphone for speech input
- Speakers for audio output
- API keys for external services

## Troubleshooting

### Common Issues:
1. **Speech recognition fails**
   - Check microphone connection
   - Reduce background noise
   - Verify internet connection

2. **APIs not responding**
   - Verify API keys in .env file
   - Check internet connectivity
   - Ensure rate limits haven't been exceeded

3. **Email sending fails**
   - Verify SMTP settings
   - Check email credentials
   - Enable "Less secure app access" for Gmail

4. **Reminders not triggering**
   - Verify time format (YYYY-MM-DD HH:MM)
   - Check if background thread is running
   - Ensure system time is accurate

## Future Enhancements

1. Multi-language support
2. Voice identification for multiple users
3. Integration with smart home devices
4. Calendar synchronization
5. More sophisticated NLP for complex commands
6. Mobile app companion

---

*Generated for the AI Assistant project documentation*
