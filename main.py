import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import datetime
import random
import requests
import re
import string
from key import weatherKey

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def speak(text):
    """Function to convert text to speech"""
    engine = pyttsx3.init('nsss')  # Use 'sapi5' for Windows
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Male voice
    engine.setProperty('rate', 175)  # Speed of speech
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I didn't understand. Please say that again.")
        return "None"
    except sr.RequestError:
        print("Speech Recognition service is unavailable.")
        return "None"

    return query.lower()


class AIAssistant:
    def __init__(self):
        self.history = []
        self.history_length = 3

        self.response_categories = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
                'responses': [
                    'Hello! How can I assist you today?',
                    'Hi there! How may I help you?',
                    'Greetings! What can I do for you?',
                    'Hello! I\'m listening. What do you need?'
                ]
            },

            'identity': {
                'patterns': ['who are you', 'what are you', 'your name', 'tell me about yourself'],
                'responses': [
                    'I am your AI assistant, designed to help with various tasks.',
                    'I\'m your personal assistant, ready to help with information and tasks.',
                    'I\'m a voice-enabled assistant created to make your life easier.',
                    'I\'m an AI assistant programmed to assist you with information and daily tasks.'
                ]
            },

            'status': {
                'patterns': ['how are you', 'how are you doing', 'how do you feel'],
                'responses': [
                    'I am functioning perfectly, thank you for asking.',
                    'All systems operational and ready to serve.',
                    'I\'m doing well, thank you. How can I help you?',
                    'I\'m running smoothly and ready to assist you.'
                ]
            },

            # Thanks
            'thanks': {
                'patterns': ['thank you', 'thanks', 'appreciate it', 'thank you so much'],
                'responses': [
                    'You\'re welcome!',
                    'Happy to be of service.',
                    'My pleasure.',
                    'Glad I could help.'
                ]
            },

            'creation': {
                'patterns': ['who made you', 'who created you', 'who built you', 'your creator'],
                'responses': [
                    'I was created using Python programming.',
                    'I\'m an AI assistant built with Python and various libraries.',
                    'I\'m a voice-enabled assistant created with Python.',
                    'I was programmed using Python and speech recognition technology.'
                ]
            },

            'capabilities': {
                'patterns': ['what can you do', 'your abilities', 'your capabilities', 'help me with',
                             'what do you do'],
                'responses': [
                    'I can search information, open websites, tell the time, and answer questions.',
                    'I can assist with various tasks like web searches, telling the time, and providing information.',
                    'I can help you with information, open websites, and perform various assistant tasks.',
                    'I can tell you the time, date, weather, search the web, and assist with basic information.'
                ]
            },

            'weather': {
                'patterns': ['weather', 'temperature', 'forecast', 'is it going to rain', 'is it sunny'],
                'responses': [
                    'Would you like to know the weather for a specific location?',
                    'I can check the weather for you. Which city are you interested in?',
                    'To provide accurate weather information, I need to know which city you\'re asking about.'
                ]
            },

            'time': {
                'patterns': ['time', 'current time', 'what time is it', 'tell me the time'],
                'responses': None  # Will be handled by specific function
            },

            'date': {
                'patterns': ['date', 'what day is it', 'what is today', 'current date', 'what is the date'],
                'responses': None  # Will be handled by specific function
            },

            'search': {
                'patterns': ['search for', 'look up', 'find information about', 'search', 'google'],
                'responses': None  # Will be handled by specific function
            },

            'web_nav': {
                'patterns': ['open website', 'go to website', 'visit website', 'open', 'browse to'],
                'responses': None  # Will be handled by specific function
            },

            'joke': {
                'patterns': ['tell me a joke', 'joke', 'make me laugh', 'be funny'],
                'responses': [
                    'Why don\'t scientists trust atoms? Because they make up everything!',
                    'What do you call a fake noodle? An impasta!',
                    'Why did the scarecrow win an award? Because he was outstanding in his field!',
                    'What do you call a computer that sings? A Dell!',
                    'Why couldn\'t the bicycle stand up by itself? It was two tired!',
                    'How do you organize a space party? You planet!',
                    'Why did the coffee file a police report? It got mugged!',
                    'What\'s the best thing about Switzerland? I don\'t know, but the flag is a big plus!'
                ]
            },

            'help': {
                'patterns': ['help', 'how do I use you', 'what commands', 'instructions'],
                'responses': [
                    'I can help with various tasks. You can ask me about the time, date, weather, search the web, open websites, or just chat with me. Just speak naturally!',
                    'You can ask me questions, request information, or give me commands like "tell me the time" or "search for something". I\'m here to assist you.',
                    'Try asking me things like "what time is it", "what\'s the weather in New York", "search for pasta recipes", or "open YouTube".'
                ]
            }
        }

        self.inappropriate_patterns = [
            r'sexy', r'sex', r'porn', r'naked', r'nude', r'explicit',
            r'f.{0,3}ck', r'sh.{0,3}t', r'b.{0,3}tch', r'a.{0,3}hole',
            r'd.{0,3}ck', r'p.{0,3}ssy', r'c.{0,3}nt', r'ass(?!ist)'
        ]

        self.repetition_pattern = r'(\b\w+\b)(\s+\1){3,}'

    def get_response(self, user_input):
        self.history.append({"user": user_input})
        if len(self.history) > self.history_length * 2:
            self.history = self.history[-self.history_length * 2:]

        response = self._generate_response(user_input)

        if self._contains_inappropriate_content(response) or self._contains_repetitions(response):
            response = self._get_safe_response()

        if len(response.strip()) <= 2 or response.lower() == user_input.lower():
            response = self._get_safe_response()

        self.history.append({"assistant": response})
        return response

    def _generate_response(self, user_input):
        user_input = user_input.lower()

        for category, data in self.response_categories.items():
            if any(pattern in user_input for pattern in data['patterns']):
                if data['responses'] is None:
                    return None

                return random.choice(data['responses'])

        if any(q_word in user_input for q_word in ["what", "when", "where", "who", "why", "how"]):
            return self._get_informational_response(user_input)

        if any(word in user_input for word in
               ["not", "doesn't", "don't", "wrong", "incorrect", "that doesn't", "that's not"]):
            for i in range(len(self.history) - 1, -1, -1):
                if "assistant" in self.history[i]:
                    return "I apologize for the confusion. How else can I assist you today?"

        default_responses = [
            "I'll do my best to help you with that.",
            "How can I assist you with that request?",
            "I'm here to help. Could you provide more details?",
            "I'd be happy to help with that. What specifically would you like to know?",
            "I'm ready to assist you with that request."
        ]

        return random.choice(default_responses)

    def _get_informational_response(self, query):
        # Topic-based templated responses
        if "weather" in query:
            return "I can check the weather for you. Which city are you interested in?"

        if any(word in query for word in ["capital", "city"]):
            if "united states" in query or "us" in query or "america" in query:
                return "The capital of the United States is Washington, D.C."
            if "uk" in query or "united kingdom" in query or "britain" in query:
                return "The capital of the United Kingdom is London."
            return "To answer questions about capitals, I would need specific information about which country you're asking about."

        if "population" in query:
            return "For up-to-date population information, I would recommend checking an online source with current statistics."

        if "president" in query:
            return "As of March 2025, Donald Trump is the President of the United States."

        if "tallest" in query and ("building" in query or "structure" in query):
            return "As of my last update, the Burj Khalifa in Dubai is the tallest building in the world, standing at 828 meters (2,717 feet)."

        # Generic information response
        return "That's an interesting question. To get accurate information on this topic, I would recommend a quick web search for the most current details."

    def _get_safe_response(self):
        """Return a safe, generic response when needed"""
        safe_responses = [
            "I'm here to assist you. How can I help?",
            "How else can I assist you today?",
            "Is there something specific you'd like help with?",
            "I'm your assistant. What would you like to know?",
            "I'm listening. What can I do for you?"
        ]
        return random.choice(safe_responses)

    def _contains_inappropriate_content(self, text):
        if not text:
            return False

        text_lower = text.lower()
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, text_lower):
                return True
        return False

    def _contains_repetitions(self, text):
        if not text:
            return False

        if re.search(self.repetition_pattern, text):
            return True

        for char in string.ascii_letters:
            if char * 5 in text:
                return True

        return False


def search_wikipedia(query):
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "").strip()
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        return results
    except Exception as e:
        return f"Sorry, I couldn't find information about {query} on Wikipedia."


def get_weather(city='your city'):
    API_KEY = weatherKey #add key here

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            weather_data = data["weather"][0]

            temp = main_data["temp"]
            humidity = main_data["humidity"]
            desc = weather_data["description"]

            return f"The current temperature in {city} is {temp}°C with {desc}. The humidity is {humidity}%."
        else:
            return f"Sorry, I couldn't find weather information for {city}."
    except Exception as e:
        print(f"Weather error: {e}")
        return "I'm unable to get the weather information at the moment."


def extract_city_from_query(query):
    if "in" in query:
        parts = query.split("in")
        if len(parts) > 1:
            return parts[1].strip()

    if "for" in query:
        parts = query.split("for")
        if len(parts) > 1:
            return parts[1].strip()

    return "your city"


def extract_search_query(query):
    search_prefixes = ['search for', 'search', 'look up', 'find', 'google']

    for prefix in search_prefixes:
        if prefix in query:
            search_term = query.split(prefix, 1)[1].strip()
            if search_term:
                return search_term

    return None


def extract_website(query):
    common_sites = {
        'youtube': 'https://youtube.com',
        'google': 'https://google.com',
        'gmail': 'https://gmail.com',
        'map': 'https://maps.google.com',
        'maps': 'https://maps.google.com',
        'facebook': 'https://facebook.com',
        'twitter': 'https://twitter.com',
        'instagram': 'https://instagram.com',
        'amazon': 'https://amazon.com',
        'netflix': 'https://netflix.com',
        'wikipedia': 'https://wikipedia.org',
        'reddit': 'https://reddit.com',
        'stack overflow': 'https://stackoverflow.com',
        'github': 'https://github.com',
        'linkedin': 'https://linkedin.com',
        'howdy': 'https://howdy.tamu.edu',
        'canvas' : 'https://canvas.tamu.edu',
    }

    for site, url in common_sites.items():
        if site in query:
            return site, url

    match = re.search(r'(?:open|go to|visit|browse|navigate to)\s+([a-zA-Z0-9]+\.[a-zA-Z]{2,})', query)
    if match:
        domain = match.group(1)
        return domain, f"https://{domain}"

    return None, None


def main():
    speak("Initializing your personal assistant...")

    ai = AIAssistant()

    speak("Systems online and ready for commands")

    while True:
        query = takeCommand()

        if query == "none":
            continue

        if any(word in query for word in ['quit', 'exit', 'stop', 'shut down', 'bye', 'goodbye']):
            speak("Shutting down. Goodbye, sir.")
            break

        if 'wikipedia' in query:
            result = search_wikipedia(query)
            speak(result)

        elif 'joke' in query:
            joke = random.choice(ai.response_categories['joke']['responses'])
            speak(joke)

        elif any(phrase in query for phrase in ai.response_categories['time']['patterns']):
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {strTime}")

        elif any(phrase in query for phrase in ai.response_categories['date']['patterns']):
            strDate = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {strDate}")

        elif 'weather' in query:
            city = extract_city_from_query(query)
            weather_info = get_weather(city)
            speak(weather_info)

        elif any(phrase in query for phrase in ai.response_categories['search']['patterns']):
            search_term = extract_search_query(query)
            if search_term:
                speak(f"Searching for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                speak("What would you like me to search for?")

        elif 'open' in query or 'go to' in query:
            site_name, site_url = extract_website(query)
            if site_name and site_url:
                speak(f"Opening {site_name}")
                webbrowser.open(site_url)
            else:
                speak("I'm not sure which website you want me to open. Could you specify?")

        elif any(phrase in query for phrase in ['play music', 'play song', 'play some music']):
            speak("Playing music")
            # Replace with path to your music directory
            music_dir = "C:\\Users\\YourUsername\\Music"
            try:
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, random.choice(songs)))
                else:
                    speak("No music files found")
            except Exception as e:
                print(f"Music error: {e}")
                speak("I couldn't access the music directory")

        elif any(phrase in query for phrase in ['open code', 'open visual studio', 'launch visual studio code']):
            speak("Opening Visual Studio Code")
            codePath = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            try:
                os.startfile(codePath)
            except Exception as e:
                print(f"VS Code error: {e}")
                speak("I couldn't find Visual Studio Code on your system")

        else:
            response = ai.get_response(query)
            if response:
                speak(response)
            else:
                speak("I'm not sure how to respond to that. Can you try asking differently?")


if __name__ == '__main__':
    main()