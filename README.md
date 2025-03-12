# Personal Voice Assistant

A Python-based voice assistant that responds to spoken commands, provides information, and performs various tasks through speech recognition and synthesis.

## Features

- **Voice Interaction**: Listens to voice commands and responds with synthesized speech
- **Information Queries**: Provides information on time, date, weather, and basic facts
- **Web Integration**: Searches Wikipedia, opens websites, and performs Google searches
- **Conversation Skills**: Responds to greetings, questions, and casual conversation
- **Entertainment**: Tells jokes upon request

## Requirements

- Python 3.6+
- Internet connection (for web searches, Wikipedia, and weather information)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

   Or install dependencies individually:
   ```
   pip install pyttsx3 SpeechRecognition wikipedia requests
   ```

3. For speech recognition, you will need PyAudio:
   - On Windows: `pip install pyaudio`
   - On macOS: `brew install portaudio` then `pip install pyaudio`
   - On Linux: `sudo apt-get install python3-pyaudio` or equivalent for your distribution

## Usage

Run the assistant:
```
python assistant.py
```

Speak commands after the "Listening..." prompt appears.

### Sample Commands

- "What time is it?"
- "What's today's date?"
- "What's the weather in New York?"
- "Search for pasta recipes"
- "Open YouTube"
- "Tell me a joke"
- "Who are you?"
- "Exit" or "Goodbye" (to close the application)

## Configuration

### Weather API

The assistant uses OpenWeatherMap for weather data. Replace the API key in the `get_weather()` function with your own:

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Replace the existing key in the code:
   ```python
   API_KEY = "your_api_key_here"
   ```

### File Paths

For features that access local files, update the paths in the code:

- Music directory: Update the `music_dir` variable
- Application paths: Update paths like `codePath` for VS Code

## How It Works

1. The assistant listens for commands using the device microphone
2. Speech is converted to text using Google's Speech Recognition API
3. The text is processed to determine the appropriate response or action
4. Responses are converted back to speech using pyttsx3
5. Actions like web searches or opening applications are performed as requested

## Extending the Assistant

### Adding New Response Categories

Add new categories to the `response_categories` dictionary in the `AIAssistant` class:

```python
'new_category': {
    'patterns': ['trigger word 1', 'trigger word 2'],
    'responses': [
        'Response 1',
        'Response 2'
    ]
}
```

### Adding New Functionality

To add new capabilities:
1. Create a function for the new feature
2. Add relevant trigger patterns to `response_categories`
3. Update the main loop to call your function when triggered

## Troubleshooting

- **Microphone not working**: Ensure your microphone is properly connected and has the necessary permissions
- **Speech recognition errors**: Check your internet connection or try speaking more clearly
- **Text-to-speech issues**: Try changing the voice by modifying the voice ID in the `speak()` function

## Acknowledgments

- Built with Python and various open-source libraries
- Uses Google's Speech Recognition for voice input
- Uses OpenWeatherMap API for weather data
- Uses Wikipedia API for information retrieval
