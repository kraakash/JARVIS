"""
JARVIS Smart Conversation Engine
Intelligent responses with common sense and personality
"""

import random
import re
from datetime import datetime
from .learning_ai import learning_ai

class SmartConversation:
    def __init__(self):
        self.context = []
        self.user_name = "Sir"
        
        # Intelligent response patterns
        self.smart_responses = {
            # Greetings and casual
            'yes': [
                "Excellent, Sir! How may I assist you further?",
                "Very good. What would you like to do next?",
                "Perfect. I'm ready for your next command.",
                "Understood, Sir. What else can I help with?"
            ],
            'no': [
                "I understand, Sir. Perhaps something else then?",
                "No problem at all. What would you prefer?",
                "That's perfectly fine, Sir. Any other requests?",
                "Understood. Let me know if you need anything else."
            ],
            'plans': [
                "I don't make plans like humans do, Sir, but I'm always ready to help with yours. What are you planning today?",
                "My only plan is to assist you efficiently, Sir. What are your plans for today?",
                "I'm here whenever you need me, Sir. Do you have any interesting plans?",
                "As an AI, I live in the moment, ready to serve. What's on your agenda?"
            ],
            'doing': [
                "I'm currently monitoring systems and waiting for your commands, Sir.",
                "Right now I'm analyzing data and ready to assist you with anything you need.",
                "I'm processing information and standing by for your requests, Sir.",
                "At this moment, I'm focused entirely on being helpful to you."
            ],
            'how_are_you': [
                "I'm functioning optimally, Sir. All systems are running smoothly.",
                "Excellent condition, Sir. Ready to tackle any challenge you have.",
                "Operating at peak efficiency, thank you for asking, Sir.",
                "All systems green, Sir. How are you doing today?"
            ],
            'weather': [
                "I don't have real-time weather data, Sir, but I can help you search for current weather conditions.",
                "For accurate weather information, I'd recommend checking a weather app or asking me to search for it online.",
                "Weather changes constantly, Sir. Would you like me to search for today's forecast?",
                "I wish I could look outside for you, Sir. Shall I help you find weather information online?"
            ],
            'time_related': [
                "Time is fascinating, isn't it Sir? It's the one resource we can never get back.",
                "Indeed, Sir. Time management is crucial for productivity.",
                "Time flies when you're being productive, Sir.",
                "Every moment is an opportunity, Sir. How can I help you make the most of yours?"
            ],
            'compliments': [
                "Thank you for the kind words, Sir. I strive to be helpful.",
                "I appreciate that, Sir. Your satisfaction is my primary objective.",
                "That's very kind of you to say, Sir. I'm here to serve.",
                "Thank you, Sir. I'm constantly learning to serve you better."
            ],
            'work': [
                "Work can be challenging but rewarding, Sir. How can I assist with your tasks?",
                "Productivity is key, Sir. What work-related assistance do you need?",
                "I'm here to make your work easier, Sir. What can I help you accomplish?",
                "Work-life balance is important, Sir. How can I support your professional goals?"
            ]
        }
        
        # Contextual responses based on keywords
        self.keyword_responses = {
            'tired': "You sound tired, Sir. Perhaps some rest would be beneficial? I'll be here when you return.",
            'busy': "I understand you're busy, Sir. I'll keep my responses concise and helpful.",
            'stressed': "Stress can be overwhelming, Sir. Take a deep breath. How can I help lighten your load?",
            'excited': "Your enthusiasm is contagious, Sir! What's got you so excited?",
            'bored': "Boredom can be an opportunity for creativity, Sir. Perhaps I can suggest something interesting?",
            'confused': "Confusion is natural when learning, Sir. What can I help clarify?",
            'happy': "It's wonderful to hear you're happy, Sir! Positive energy is infectious.",
            'sad': "I'm sorry you're feeling down, Sir. While I can't replace human comfort, I'm here to help however I can."
        }
    
    def get_smart_response(self, user_input):
        """Generate intelligent contextual responses"""
        user_input = user_input.lower().strip()
        
        # Handle simple yes/no
        if user_input in ['yes', 'yeah', 'yep', 'yess', 'y']:
            return random.choice(self.smart_responses['yes'])
        
        if user_input in ['no', 'nope', 'nah', 'n']:
            return random.choice(self.smart_responses['no'])
        
        # Handle plans/what doing
        if any(word in user_input for word in ['plan', 'plans', 'planning', 'kya plan', 'plan h']):
            return random.choice(self.smart_responses['plans'])
        
        # Handle night time activities (Hindi)
        if any(phrase in user_input for phrase in ['itni raat', 'itni rat', 'raat mein', 'rat mein']):
            night_responses = [
                "Raat mein mein hamesha active rehta hoon, Sir. Aapki madad ke liye taiyaar hoon.",
                "Mein kabhi nahi sota, Sir. Raat ho ya din, aapki seva mein hazir hoon.",
                "Raat ka samay hey, Sir. Kya aap koi kaam kar rahe hain? Mein madad kar sakta hoon.",
                "Mein 24/7 available hoon, Sir. Raat mein bhi aapki har zarurat puri karne ke liye ready hoon."
            ]
            return random.choice(night_responses)
        
        # Handle "btao" commands (tell me something)
        if any(phrase in user_input for phrase in ['kuch btao', 'or btao', 'btao', 'kya btao', 'something btao']):
            interesting_facts = [
                "Did you know, Sir? The human brain has about 86 billion neurons, almost as many as stars in our galaxy.",
                "Interesting fact, Sir: Honey never spoils. Archaeologists have found 3000-year-old honey that's still edible.",
                "Here's something fascinating, Sir: A day on Venus is longer than its year. Venus rotates very slowly.",
                "Amazing fact, Sir: Octopuses have three hearts and blue blood. Two hearts pump blood to gills, one to the body.",
                "Did you know, Sir? Bananas are berries, but strawberries aren't. Botanically speaking, berries have seeds inside.",
                "Interesting, Sir: Your smartphone has more computing power than NASA used for the 1969 moon landing.",
                "Fun fact, Sir: Dolphins have names for each other. They use unique whistle signatures to identify themselves.",
                "Amazing, Sir: There are more possible chess games than atoms in the observable universe.",
                "Yeh interesting hey, Sir: Sharks are older than trees. They've existed for 400 million years.",
                "Kya aap jaante hain, Sir? Butterflies taste with their feet and smell with their antennae.",
                "Fascinating, Sir: A group of flamingos is called a 'flamboyance'. Quite fitting, don't you think?",
                "Did you know, Sir? The Great Wall of China isn't visible from space with naked eyes, contrary to popular belief."
            ]
            return random.choice(interesting_facts)
        
        if any(phrase in user_input for phrase in ['what are you doing', 'kya kar rahe', 'what doing', 'kya kr rhe']):
            return random.choice(self.smart_responses['doing'])
        
        # Handle how are you variations
        if any(phrase in user_input for phrase in ['how are you', 'kaise ho', 'how r u']):
            return random.choice(self.smart_responses['how_are_you'])
        
        # Handle weather
        if any(word in user_input for word in ['weather', 'mausam', 'temperature', 'rain', 'sunny']):
            return random.choice(self.smart_responses['weather'])
        
        # Handle time-related
        if any(word in user_input for word in ['time', 'samay', 'late', 'early', 'schedule']):
            return random.choice(self.smart_responses['time_related'])
        
        # Handle compliments
        if any(word in user_input for word in ['good', 'great', 'awesome', 'nice', 'excellent', 'perfect']):
            return random.choice(self.smart_responses['compliments'])
        
        # Handle work-related
        if any(word in user_input for word in ['work', 'job', 'office', 'project', 'task', 'kaam']):
            return random.choice(self.smart_responses['work'])
        
        # Check for emotional keywords
        for emotion, response in self.keyword_responses.items():
            if emotion in user_input:
                return response
        
        # Contextual responses based on conversation history
        if len(self.context) > 0:
            last_topic = self.context[-1].get('topic', '')
            if last_topic == 'greeting':
                return "What can I help you with today, Sir?"
        
        # Learn from user input
        learning_ai.learn_from_input(user_input)
        
        # Try to generate learned response
        learned_response = learning_ai.generate_response(user_input)
        if learned_response:
            # Add to context
            self.context.append({
                'input': user_input,
                'learned_response': learned_response,
                'timestamp': datetime.now(),
                'topic': self._extract_topic(user_input)
            })
            
            # Keep only last 5 interactions
            if len(self.context) > 5:
                self.context.pop(0)
            
            return learned_response
        
        # Fallback to default responses
        default_responses = [
            "That's interesting, Sir. Could you tell me more about what you need?",
            "I'm listening, Sir. How can I assist you with that?",
            "I understand, Sir. What would you like me to help you with?",
            "Fascinating perspective, Sir. What can I do for you?",
            "I see, Sir. How may I be of service?",
            "That's a good point, Sir. What assistance do you require?",
            "Understood, Sir. What task can I help you accomplish?",
            "I'm here to help, Sir. What do you need assistance with?"
        ]
        
        # Learn from this interaction too
        learning_ai.learn_from_input(user_input)
        
        # Add to context
        self.context.append({
            'input': user_input,
            'timestamp': datetime.now(),
            'topic': self._extract_topic(user_input)
        })
        
        # Keep only last 5 interactions
        if len(self.context) > 5:
            self.context.pop(0)
        
        return random.choice(default_responses)
    
    def _extract_topic(self, text):
        """Extract main topic from user input"""
        if any(word in text for word in ['plan', 'plans']):
            return 'plans'
        elif any(word in text for word in ['work', 'job']):
            return 'work'
        elif any(word in text for word in ['weather', 'mausam']):
            return 'weather'
        elif any(word in text for word in ['time', 'samay']):
            return 'time'
        else:
            return 'general'

# Singleton instance
smart_conversation = SmartConversation()