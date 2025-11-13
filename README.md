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

#### Opening Apps (Any Installed Application)
- "Open Chrome"
- "Start Calculator"
- "Launch Notepad"
- "Run Paint"
- "Open Visual Studio Code"
- "Start Microsoft Word"
- "Launch Spotify"

#### Closing Apps
- "Close Chrome"
- "Exit Calculator"
- "Stop Notepad"

#### App Discovery & Search
- "Find app Chrome"
- "Search app Visual Studio"
- "Show apps"
- "List all apps"

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

### 🧠 Advanced AI & Learning Commands

#### Contextual AI & Smart Questions
- **"Question pucho"** - Ask intelligent questions based on current activity
- **"Kya puchna chahte ho"** - Get contextual questions
- **"Ask question"** - Request AI-powered contextual questions

#### Learning & Training System
- **"Learning stats"** - Show AI learning statistics
- **"Adaptive stats"** - Display machine learning performance
- **"Test learning"** - Test if learning system is working
- **"Clean memory"** - Clean duplicate learning data
- **"ML test"** - Test machine learning model performance

#### Work Pattern Analysis
- **"Work pattern"** - Analyze your work habits and patterns
- **"Pattern analysis"** - Get detailed work pattern insights
- **"Kaam ka analysis"** - Hindi work pattern analysis
- **"Analyze mistakes"** - Analyze productivity issues from monitoring
- **"Meri galtiyan"** - Hindi mistake analysis

#### Productivity & Improvement
- **"Improvement suggestions"** - Get personalized productivity tips
- **"Productivity tips"** - Receive work efficiency suggestions
- **"Work better"** - Get improvement recommendations
- **"Improve kaise"** - Hindi improvement suggestions

### 🖥️ Desktop Monitoring & Activity Tracking

#### Monitoring Control
- **"Start monitoring"** - Begin desktop activity tracking
- **"Stop monitoring"** - End activity monitoring
- **"Monitoring shuru"** - Hindi start monitoring
- **"Monitoring band"** - Hindi stop monitoring

#### Activity Reports
- **"Activity report"** - Get detailed activity summary
- **"Current activity"** - See what you're currently doing
- **"Main kya kar raha hun"** - Hindi current activity check
- **"What am I doing"** - Current activity status
- **"Kya update hai"** - System and activity status update
- **"Status kya hai"** - Current system status

#### Smart Suggestions
- **"Suggestions"** - Get activity-based suggestions
- **"Recommend"** - Request recommendations
- **"Tips"** - Get productivity tips
- **"Sujhav"** - Hindi suggestions

### 🤖 Smart Automation System

#### Automation Suggestions
- **"Automation suggestions"** - Get workflow optimization suggestions
- **"Smart suggestions"** - Intelligent automation recommendations
- **"Workflow tips"** - Workflow improvement suggestions
- **"Optimize workflow"** - Get workflow optimization help

#### Execute Automation
- **"Execute automation browser"** - Run browser cleanup automation
- **"Execute automation focus"** - Apply focus mode setup
- **"Execute automation split screen"** - Set up split screen workflow
- **"Automation chalao"** - Hindi execute automation

#### Automation Statistics
- **"Automation stats"** - View automation usage statistics
- **"Automation statistics"** - Detailed automation analytics
- **"Workflow stats"** - Workflow optimization statistics

### 🆘 Real Help & Problem Solving

#### Get Help
- **"Help me"** - Get contextual help options
- **"Help karo"** - Hindi help request
- **"Madad karo"** - Hindi assistance request
- **"Solve karo"** - Request problem solving
- **"Fix karo"** - Request issue fixing

#### Execute Help Actions
- **"Google search [topic]"** - Instant Google search for any topic
- **"Search karo [topic]"** - Hindi Google search
- **"StackOverflow [error]"** - Direct StackOverflow search
- **"Documentation [language]"** - Open programming documentation

#### Help Examples
```
"help me" → Shows available help options
"google search python error" → Opens Google with search results
"stackoverflow import error" → Opens StackOverflow search
"documentation python" → Opens Python documentation
```

## 🚀 Advanced Usage Examples

### Contextual AI Learning
```
You: "Jarvis"
JARVIS: "Haan Sir?"
You: "Question pucho"
JARVIS: "Kya Python code mein koi error aa raha hai?" (based on current VS Code activity)
You: "Haan, import error hai"
JARVIS: [Learns this pattern for future contextual questions]
```

### Real-Time Help
```
You: "Jarvis"
JARVIS: "Yes Sir?"
You: "Help me"
JARVIS: "Real Help Available:
1. Google search karu problem ke liye?
2. StackOverflow solution dhundu?
3. Documentation kholu?"
You: "Google search python import error"
JARVIS: "Google search opened for: python import error" [Browser opens automatically]
```

### Smart Monitoring & Analysis
```
You: "Jarvis"
JARVIS: "Yes Sir?"
You: "Start monitoring"
JARVIS: "Desktop monitoring started, Sir. I'm now tracking your activities."
[After some work...]
You: "Work pattern"
JARVIS: "Work Pattern Analysis:
Most Common Activity: coding (15 times)
Main Improvement Area: efficiency
Total Learning Entries: 25"
```

### Automation Suggestions
```
You: "Jarvis"
JARVIS: "Yes Sir?"
You: "Automation suggestions"
JARVIS: "Smart Automation Suggestions:
1. [High] Browser cleanup - 12 tabs open, organize kariye
2. [Medium] Split screen setup for coding workflow
3. [Low] Focus mode for distraction-free work"
You: "Execute automation browser"
JARVIS: "Automation executed: Browser tabs organized and duplicates closed"
```

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

### Example 4: App Discovery
```
You: "Jarvis"
JARVIS: "Yes, Sir?"
You: "Find app Visual Studio"
JARVIS: "Found applications matching 'Visual Studio': Visual Studio Code, Visual Studio 2022"
You: "Open Visual Studio Code"
JARVIS: "Opening Visual Studio Code, Sir."
```

### Example 5: Mixed Commands
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

**JARVIS automatically discovers ALL installed applications on your PC including:**

### Built-in Windows Apps
- **Calculator** - Windows calculator
- **Notepad** - Text editor
- **Paint** - Image editor
- **Explorer** - File manager
- **CMD** - Command prompt
- **WordPad** - Rich text editor

### Installed Applications
- **Chrome** - Web browser
- **Edge** - Microsoft Edge browser
- **Visual Studio Code** - Code editor
- **Microsoft Office** - Word, Excel, PowerPoint
- **Spotify** - Music streaming
- **Discord** - Communication
- **Steam** - Gaming platform
- **And ANY other installed application!**

**Note**: JARVIS scans your system to find all installed applications automatically. Just say "Open [App Name]" for any application on your PC.

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

## 🔥 Latest Updates

### 🧠 Advanced Contextual AI System (NEWEST!)
- **Real-time Activity Understanding**: AI analyzes what you're doing and asks relevant questions
- **Machine Learning Integration**: TensorFlow + scikit-learn for intelligent pattern recognition
- **Self-Learning System**: Learns from your responses and improves over time
- **Contextual Question Generation**: Smart questions based on current app, file type, and activity duration
- **Personalized Responses**: Adapts to your work patterns and preferences

### 🆘 Real Help Engine (MAJOR UPDATE!)
- **Actionable Assistance**: Not just questions - actual problem solving
- **Instant Google Search**: "google search [topic]" opens browser automatically
- **StackOverflow Integration**: Direct search for programming problems
- **Documentation Access**: Quick access to official programming docs
- **Context-Aware Help**: Different help based on what you're currently doing
- **Error Solution Database**: Common programming error fixes and explanations

### 🖥️ Advanced Desktop Monitoring
- **Real-time Activity Tracking**: Monitors apps, windows, and usage patterns
- **Smart Activity Classification**: Coding, research, learning, communication detection
- **Session Persistence**: Remembers monitoring state between restarts
- **Activity Pattern Analysis**: Identifies work habits and productivity patterns
- **Intelligent Suggestions**: Context-aware productivity recommendations

### 🤖 Smart Automation System
- **Workflow Optimization**: Analyzes patterns and suggests automations
- **Browser Management**: Automatic tab cleanup and organization
- **Split Screen Setup**: Intelligent window arrangement for productivity
- **Focus Mode**: Distraction elimination and work environment optimization
- **User Preference Learning**: Remembers which automations you prefer

### 📊 Advanced Analytics & Learning
- **Work Pattern Analysis**: Detailed insights into your productivity habits
- **Learning Statistics**: Track AI improvement and learning progress
- **Adaptive Intent Recognition**: ML-powered command understanding
- **Conversation Style Learning**: Adapts to your natural speaking patterns
- **Improvement Suggestions**: Personalized productivity enhancement tips

## Recent Updates

### 🧠 Advanced Conversation System (LATEST!)
- **Human-like Conversations**: Contextual memory and intelligent follow-up questions
- **Real-time Learning**: Learns from every conversation and builds user profiles
- **Emotional Intelligence**: Adapts responses based on user emotional patterns
- **Problem Solving**: Provides intelligent suggestions and analytical responses
- **Conversation Context**: Maintains conversation flow and remembers topics
- **Neural Network Training**: Advanced TensorFlow model for conversation patterns

### Learning & AI System
- **Machine Learning Integration**: Added TensorFlow LSTM model with neural network foundation
- **Custom Response System**: Create personalized responses in `custom_responses.json`
- **Memory Management**: Intelligent pattern learning with duplicate prevention
- **Smart Conversations**: Context-aware responses with interesting facts
- **Learning Stats**: Track AI learning progress with `learning stats` command
- **Conversation Training**: Automated training data generation and model improvement

### Custom Response Editor
- **JSON-based Editing**: Edit responses in `custom_responses.json` file
- **Pattern Mapping**: Custom responses override default AI responses
- **Priority System**: Contextual → Custom → User-taught → TensorFlow → Neural Network
- **Training Integration**: Custom responses automatically train TensorFlow model

### Enhanced Voice & Language
- **Improved Hindi Pronunciation**: Better phonetic processing for Hindi responses
- **JARVIS Voice Selection**: Automatic selection of best available voice
- **Threading Fixes**: Resolved TTS threading issues for smoother speech
- **Bilingual Learning**: AI learns patterns in both Hindi and English
- **Contextual Language**: Responds in appropriate language based on conversation context

### Application Discovery
- **Dynamic App Scanning**: Automatically discovers ALL installed applications
- **Registry Integration**: Scans Windows registry for comprehensive app list
- **Smart App Matching**: Fuzzy matching for application names
- **Enhanced Commands**: `list apps`, `find app [name]`, `show apps`

### Web & YouTube Enhancements
- **Video Control**: Pause, resume, and stop YouTube videos
- **Fallback Modes**: Graceful handling when Chrome automation fails
- **Result Navigation**: Click results, go back, show results
- **Search Optimization**: Better query extraction and result presentation

### Memory & Learning Files
- **jarvis_memory.json**: Stores learned patterns and word associations
- **custom_responses.json**: User-defined custom responses
- **conversation_context.json**: Conversation history and user profiles
- **jarvis_conversation_training.json**: Training dataset for conversation patterns
- **user_conversations.json**: Real user interactions for continuous learning
- **TensorFlow Models**: Advanced ML models for conversation improvement
- **Duplicate Prevention**: Smart learning prevents memory file bloat

## 🧠 Advanced AI Systems

### Contextual AI Features
- **Activity Classification**: Automatically detects coding, research, learning, communication
- **Smart Question Generation**: Context-aware questions based on current work
- **Pattern Recognition**: Learns your work habits and preferences
- **Real-time Analysis**: Continuous activity monitoring and analysis
- **Confidence Scoring**: AI rates its understanding accuracy
- **Multi-language Support**: Works in both Hindi and English contexts

### Learning & Training
- **Response Learning**: Trains from your answers to improve future questions
- **Pattern Memory**: Remembers successful interaction patterns
- **Improvement Tracking**: Identifies areas where you need help
- **Personalization**: Adapts to your individual work style
- **Continuous Improvement**: Gets smarter with every interaction

### Help Engine Capabilities
- **Instant Web Search**: Automated Google and StackOverflow searches
- **Documentation Access**: Quick links to programming documentation
- **Error Solutions**: Database of common programming fixes
- **Productivity Tips**: Contextual efficiency suggestions
- **Code Analysis**: Basic code structure and quality assessment

## 🧠 Advanced Conversation System (ENHANCED!)

JARVIS now features advanced AI-powered assistance with:

### 🎯 Intelligent Features
- **Contextual Understanding**: Analyzes current activity and provides relevant help
- **Smart Questioning**: Asks intelligent questions based on what you're doing
- **Real Problem Solving**: Actually opens resources and provides solutions
- **Pattern Learning**: Learns your work habits and improvement areas
- **Adaptive Responses**: Personalizes suggestions based on your patterns
- **Actionable Assistance**: Executes help actions, not just suggestions

### 📊 Model Statistics
- **Training Samples**: Comprehensive conversation patterns
- **Contextual Responses**: Situational response patterns
- **Follow-up Chains**: Multi-turn conversation sequences
- **Intelligent Responses**: Problem-solving and analytical variations
- **Neural Network**: TensorFlow-powered conversation model
- **User Conversations**: Continuously learning from real interactions

### 💬 AI Interaction Examples

#### Contextual Help
```
[You're coding in VS Code with Python file open]
You: "question pucho"
JARVIS: "Kya Python code mein koi error aa raha hai?"
You: "haan import error"
JARVIS: "Google search karu 'python import error solution'?"
You: "haan"
JARVIS: [Opens Google search automatically]
```

#### Real Problem Solving
```
You: "help me"
JARVIS: "Real Help Available:
1. Google search karu problem ke liye?
2. StackOverflow solution dhundu?
3. Documentation kholu?"
You: "google search react hooks error"
JARVIS: "Google search opened for: react hooks error"
```

#### Pattern Learning
```
[After multiple coding sessions]
You: "work pattern"
JARVIS: "Work Pattern Analysis:
Most Common Activity: coding (debugging: 60%)
Main Improvement Area: needs_help
Suggestion: Debugging tools use karne ka suggestion du?"
```

### 🚀 How Advanced AI Works
1. **Activity Monitoring**: Real-time tracking of apps, windows, and work patterns
2. **Context Analysis**: ML-powered understanding of current work context
3. **Smart Question Generation**: AI creates relevant questions based on activity
4. **Response Learning**: Learns from your answers to improve future interactions
5. **Actionable Help**: Executes real help actions like opening searches and documentation
6. **Pattern Recognition**: Identifies work habits and suggests improvements

### 🔧 AI Training & Learning
The system automatically:
- **Monitors Your Activity**: Tracks apps, files, and work patterns
- **Learns from Responses**: Improves based on your answers to questions
- **Builds User Profile**: Creates personalized work pattern analysis
- **Generates Improvements**: Suggests productivity enhancements
- **Executes Help Actions**: Actually opens resources and provides solutions
- **Saves Learning Data**: Stores patterns in `contextual_training.json`

### 📊 Available Analytics
```bash
"learning stats" - AI learning progress
"adaptive stats" - ML model performance
"work pattern" - Your work habit analysis
"improvement suggestions" - Personalized productivity tips
```

## 🎯 Command Quick Reference

### Essential Commands
- `"help me"` - Get contextual help options
- `"google search [topic]"` - Instant web search
- `"question pucho"` - Get smart contextual questions
- `"start monitoring"` - Begin activity tracking
- `"work pattern"` - Analyze your productivity
- `"improvement suggestions"` - Get personalized tips
- `"automation suggestions"` - Get workflow optimizations

### Learning Commands
- `"learning stats"` - View AI learning progress
- `"adaptive stats"` - ML model performance
- `"test learning"` - Test learning system
- `"analyze mistakes"` - Productivity issue analysis

### Help Commands
- `"stackoverflow [error]"` - Direct StackOverflow search
- `"documentation [language]"` - Open programming docs
- `"execute automation [type]"` - Run workflow automation

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
- Built with Python, Selenium, TensorFlow, scikit-learn, and advanced NLP libraries
- Voice processing using SpeechRecognition and pyttsx3 with Hindi TTS support
- Machine learning with TensorFlow, scikit-learn, and custom neural networks
- Advanced contextual AI system with real-time activity understanding
- Smart automation and workflow optimization capabilities
- Real help engine with actionable problem-solving features
- Desktop monitoring and productivity analysis system
- Self-learning AI that improves from user interactions