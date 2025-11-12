# JARVIS - Advanced AI Assistant

JARVIS (Just A Rather Very Intelligent System) is a voice-controlled AI assistant with natural language processing, emotional intelligence, and web automation capabilities.

## Features

- 🎤 **Voice Control** - Wake word activation ("Jarvis")
- 🌐 **Bilingual Support** - English and Hindi responses
- 🧠 **Emotional Intelligence** - Sentiment analysis and contextual responses
- 🖥️ **Application Control** - Open/close Windows applications
- 🌍 **Web Automation** - Chrome browser control and Google search
- 💬 **Natural Conversations** - General chat and Q&A

## Installation

### Prerequisites
- Python 3.8+
- Windows OS
- Chrome browser
- Microphone (for voice input)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd Jarvis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download ChromeDriver:
   - Go to https://chromedriver.chromium.org/
   - Download version matching your Chrome browser
   - Add chromedriver.exe to your system PATH

4. Run JARVIS:
```bash
python main.py
```

## Commands

### Voice Activation
- Say **"Jarvis"** to activate
- Wait for "Yes, Sir?" response
- Give your command

### Language Control
- **"Hindi mein bolo"** - Switch to Hindi responses
- **"English mein bolo"** - Switch to English responses

### General Conversation

#### English
- "How are you?"
- "What's your name?"
- "Who are you?"
- "What can you do?"
- "Thank you"
- "Tell me a joke"

#### Hindi
- "Kaise ho?"
- "Tumhara naam kya hai?"
- "Tum kaun ho?"
- "Tum kya kar sakte ho?"
- "Dhanyawad"
- "Joke sunao"

### Application Control

#### Opening Apps
- "Open Chrome"
- "Start Calculator"
- "Launch Notepad"
- "Run Paint"

#### Closing Apps
- "Close Chrome"
- "Exit Calculator"
- "Stop Notepad"

#### Hindi App Commands
- "Chrome kholo"
- "Calculator band karo"
- "Notepad chalu karo"

### Web Search & Automation

#### Search Commands
- "Search for Python tutorials"
- "Google latest news"
- "Find best restaurants near me"
- "Look up weather today"

#### Navigation Commands
- "Show search results"
- "Open first result"
- "Click first result"
- "Go back"

#### Hindi Web Commands
- "Python tutorials search karo"
- "Aaj ka mausam dhundo"

### YouTube Control

#### YouTube Commands
- "Open YouTube"
- "YouTube search Python tutorials"
- "Search YouTube for music"
- "Play first video"
- "Play second video"
- "Play third video"
- "Show YouTube results"
- "Pause video"
- "Resume video"
- "Stop video"

#### Hindi YouTube Commands
- "YouTube kholo"
- "YouTube mein search karo"
- "Pehla video chalao"
- "Dusra video play karo"
- "Video roko"
- "Video band karo"

### Time & Calculations

#### Time Queries
- "What time is it?"
- "Current time"
- "Samay kya hai?" (Hindi)

#### Math Operations
- "Calculate 5 plus 3"
- "What is 10 + 15?"
- "5 + 7 kitna hota hai?" (Hindi)

### System Control
- "Exit" / "Quit" / "Goodbye" - Shutdown JARVIS
- "Alvida" / "Band karo" - Hindi shutdown commands

## Usage Examples

### Example 1: Web Search
```
You: "Jarvis"
JARVIS: "Yes, Sir?"
You: "Search for Python programming tutorials"
JARVIS: "Searched for 'Python programming tutorials', Sir. Results are displayed. Top search results: 1. Python Tutorial - W3Schools; 2. Learn Python Programming; 3. Python.org Tutorial"
You: "Open first result"
JARVIS: "Opened the first search result, Sir."
```

### Example 2: Hindi Conversation
```
You: "Jarvis"
JARVIS: "Haan Sir?"
You: "Kaise ho?"
JARVIS: "Main bilkul theek hun, Sir! Aapki seva ke liye taiyar hun."
You: "Chrome kholo"
JARVIS: "Chrome khol raha hun, Sir."
```

### Example 3: YouTube Control
```
You: "Jarvis"
JARVIS: "Yes, Sir?"
You: "YouTube search Python tutorials"
JARVIS: "YouTube search results for 'Python tutorials' are ready, Sir. Top YouTube videos: 1. Python Full Course; 2. Learn Python in 1 Hour; 3. Python for Beginners"
You: "Play first video"
JARVIS: "Playing video 1: 'Python Full Course', Sir."
You: "Pause video"
JARVIS: "Video paused/resumed, Sir."
You: "Stop video"
JARVIS: "Stopped video and returned to search results, Sir."
```

### Example 4: Mixed Commands
```
You: "Jarvis"
JARVIS: "Yes, Sir?"
You: "Open calculator"
JARVIS: "Opening calculator, Sir."
You: "Calculate 25 plus 30"
JARVIS: "The answer is 55"
You: "Thank you"
JARVIS: "You're most welcome, Sir!"
```

## Supported Applications

- **Chrome** - Web browser
- **Calculator** - Windows calculator
- **Notepad** - Text editor
- **Paint** - Image editor
- **Explorer** - File manager
- **CMD** - Command prompt
- **Edge** - Microsoft Edge browser

## Troubleshooting

### Voice Input Issues
- Check microphone permissions
- Ensure microphone is working
- Press Ctrl+C to switch to text mode

### ChromeDriver Issues
- Download correct ChromeDriver version
- Add chromedriver.exe to system PATH
- Ensure Chrome browser is installed

### Chrome Automation Detection
- If you see "Chrome is being controlled by automated test software"
- JARVIS automatically falls back to simple browser mode
- Search will open in your default browser instead
- This avoids robot detection while maintaining functionality

### Import Errors
- Install all required packages: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### TTS Not Working
- Check system volume
- Verify audio output device
- Try text mode for testing

### Web Search Issues
- If Selenium fails, JARVIS uses simple browser mode
- Search opens in default browser (Chrome/Edge/Firefox)
- No advanced features (clicking results) in simple mode
- Install ChromeDriver properly for full automation

## Architecture

```
JARVIS/
├── main.py                 # Entry point
├── core/
│   └── brain.py           # Main decision engine
├── modules/
│   ├── voice/             # Speech processing
│   │   ├── speaker.py     # Text-to-Speech
│   │   └── listener.py    # Speech-to-Text
│   ├── nlp/               # Natural Language Processing
│   │   ├── emotion_engine.py      # Sentiment & Intent
│   │   ├── language_support.py   # Multilingual support
│   │   └── conversation_engine.py # Conversations
│   ├── apps/              # Application control
│   │   └── app_controller.py
│   └── web/               # Web automation
│       └── web_controller.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Inspired by Marvel's JARVIS
- Built with Python, Selenium, and various NLP libraries
- Voice processing using SpeechRecognition and pyttsx3