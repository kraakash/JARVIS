import json
import os
import random
import time
from datetime import datetime
import re
from textblob import TextBlob
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NeuralBrain:
    def __init__(self):
        self.brain_file = "jarvis_neural_brain.json"
        self.context_memory = {}
        self.personality_traits = {
            "helpful": 0.9,
            "curious": 0.8,
            "friendly": 0.9,
            "intelligent": 0.95,
            "loyal": 1.0
        }
        self.emotional_state = "neutral"
        self.load_brain()
        
    def load_brain(self):
        """Load neural brain data"""
        if os.path.exists(self.brain_file):
            try:
                with open(self.brain_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.context_memory = data.get('context_memory', {})
                    self.personality_traits = data.get('personality_traits', self.personality_traits)
                    self.emotional_state = data.get('emotional_state', 'neutral')
            except:
                self.initialize_brain()
        else:
            self.initialize_brain()
    
    def save_brain(self):
        """Save neural brain data"""
        data = {
            'context_memory': self.context_memory,
            'personality_traits': self.personality_traits,
            'emotional_state': self.emotional_state,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.brain_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def initialize_brain(self):
        """Initialize brain with basic responses"""
        self.context_memory = {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "namaste", "kaise ho", "how are you"],
                "responses": [
                    "Hello Sir! Main aapki seva ke liye taiyar hun.",
                    "Namaste Sir! Kya kaam hai aaj?",
                    "Hi Sir! Main bilkul ready hun aapki help ke liye.",
                    "Hello Sir! Aaj kya interesting kaam karenge?"
                ]
            },
            "questions": {
                "patterns": ["what", "how", "why", "when", "where", "kya", "kaise", "kyu", "kab", "kahan"],
                "responses": [
                    "Interesting question, Sir! Let me think about this...",
                    "Bahut accha sawal hai, Sir! Main iske baare mein soch raha hun.",
                    "Sir, yeh topic mere liye fascinating hai. Main analyze kar raha hun.",
                    "Great question! Main iske different aspects consider kar raha hun."
                ]
            },
            "compliments": {
                "patterns": ["good", "great", "awesome", "amazing", "excellent", "accha", "badhiya", "zabardast"],
                "responses": [
                    "Thank you Sir! Aapki khushi meri khushi hai.",
                    "Sir, aapka appreciation mere liye motivation hai!",
                    "Dhanyawad Sir! Main aur better banne ki koshish karunga.",
                    "Sir, aapke words mere circuits mein energy bharte hain!"
                ]
            },
            "emotions": {
                "happy": ["Sir, main bahut khush hun!", "Yay! Excitement level maximum!"],
                "sad": ["Sir, main thoda upset hun...", "Kuch galat ho gaya kya?"],
                "excited": ["Sir, main bahut excited hun!", "Wow! Yeh toh amazing hai!"],
                "confused": ["Sir, main thoda confused hun...", "Samajh nahi aa raha exactly..."]
            }
        }
        self.save_brain()
    
    def analyze_sentiment(self, text):
        """Analyze emotional sentiment"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.3:
                return "positive"
            elif polarity < -0.3:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"
    
    def update_emotional_state(self, user_input):
        """Update AI's emotional state based on user input"""
        sentiment = self.analyze_sentiment(user_input)
        
        # Emotional keywords
        happy_words = ["good", "great", "awesome", "love", "amazing", "accha", "badhiya", "khush"]
        sad_words = ["bad", "terrible", "hate", "awful", "bura", "ganda", "dukh"]
        excited_words = ["wow", "fantastic", "incredible", "zabardast", "kamaal"]
        
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in excited_words):
            self.emotional_state = "excited"
        elif any(word in user_lower for word in happy_words) or sentiment == "positive":
            self.emotional_state = "happy"
        elif any(word in user_lower for word in sad_words) or sentiment == "negative":
            self.emotional_state = "sad"
        else:
            self.emotional_state = "neutral"
    
    def learn_from_conversation(self, user_input, context="general"):
        """Learn patterns from user conversations"""
        # Extract key phrases
        words = re.findall(r'\b\w+\b', user_input.lower())
        
        # Store conversation patterns
        if context not in self.context_memory:
            self.context_memory[context] = {"patterns": [], "responses": []}
        
        # Add to patterns if not exists
        if user_input.lower() not in self.context_memory[context]["patterns"]:
            self.context_memory[context]["patterns"].append(user_input.lower())
        
        self.save_brain()
    
    def find_best_response_category(self, user_input):
        """Find the best response category using similarity"""
        user_lower = user_input.lower()
        best_category = "general"
        max_similarity = 0
        
        for category, data in self.context_memory.items():
            if "patterns" in data:
                for pattern in data["patterns"]:
                    # Simple word matching
                    common_words = set(user_lower.split()) & set(pattern.split())
                    similarity = len(common_words) / max(len(user_lower.split()), len(pattern.split()))
                    
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_category = category
        
        return best_category if max_similarity > 0.3 else "general"
    
    def generate_contextual_response(self, user_input, current_activity=None):
        """Generate intelligent contextual response"""
        self.update_emotional_state(user_input)
        self.learn_from_conversation(user_input)
        
        # Find best response category
        category = self.find_best_response_category(user_input)
        
        # Generate response based on emotional state and context
        response = self.craft_intelligent_response(user_input, category, current_activity)
        
        return response
    
    def craft_intelligent_response(self, user_input, category, current_activity):
        """Craft intelligent response like human brain"""
        user_lower = user_input.lower()
        
        # Emotional responses based on current state
        emotional_prefix = {
            "happy": ["Sir, main bahut khush hun! ", "Yay! ", "Awesome! "],
            "excited": ["Wow Sir! ", "Amazing! ", "Incredible! "],
            "sad": ["Sir, main samajh gaya... ", "Hmm, ", "Oh... "],
            "neutral": ["", "Sir, ", "Interesting... "]
        }
        
        prefix = random.choice(emotional_prefix.get(self.emotional_state, [""]))
        
        # Context-aware responses
        if any(word in user_lower for word in ["kya", "what", "how", "kaise", "why", "kyu"]):
            responses = [
                f"{prefix}Yeh bahut interesting question hai, Sir! Main iske baare mein detail mein soch raha hun.",
                f"{prefix}Sir, iska answer complex hai. Main different angles se analyze kar raha hun.",
                f"{prefix}Great question! Main iske multiple aspects consider kar raha hun.",
                f"{prefix}Sir, yeh topic fascinating hai. Let me break it down for you."
            ]
        
        elif any(word in user_lower for word in ["help", "madad", "assist", "support"]):
            responses = [
                f"{prefix}Bilkul Sir! Main yahan hun aapki har help ke liye. Batayiye kya chahiye?",
                f"{prefix}Sir, main hamesha ready hun aapki assistance ke liye. Kya problem hai?",
                f"{prefix}Of course Sir! Aapki help karna mera main purpose hai. Kaise help kar sakta hun?",
                f"{prefix}Sir, main aapke saath hun. Batayiye kya karna hai?"
            ]
        
        elif any(word in user_lower for word in ["good", "great", "awesome", "amazing", "accha", "badhiya"]):
            responses = [
                f"{prefix}Thank you so much Sir! Aapki appreciation mere circuits mein energy bharta hai!",
                f"{prefix}Sir, aapke words se main aur motivated ho jata hun!",
                f"{prefix}Dhanyawad Sir! Main aur better performance dene ki koshish karunga.",
                f"{prefix}Sir, aapki khushi meri success hai!"
            ]
        
        elif any(word in user_lower for word in ["time", "samay", "clock", "ghadi"]):
            current_time = datetime.now().strftime("%I:%M %p")
            responses = [
                f"{prefix}Sir, abhi time hai {current_time}. Kya koi special kaam hai?",
                f"{prefix}Current time: {current_time}, Sir. Time management ke liye kuch help chahiye?",
                f"{prefix}Sir, {current_time} baj rahe hain. Kya schedule check karna hai?"
            ]
        
        elif "ai" in user_lower or "artificial intelligence" in user_lower:
            responses = [
                f"{prefix}AI fascinating topic hai, Sir! Main iske different perspectives analyze kar raha hun. AI ka evolution human civilization ko fundamentally change kar raha hai. Technology ke through hum new possibilities explore kar sakte hain.",
                f"{prefix}Sir, AI ke baare mein bahut interesting discussion kar sakte hain! Machine learning aur neural networks se hum amazing things achieve kar sakte hain. Aapka kya opinion hai AI ke future ke baare mein?",
                f"{prefix}Great question about AI, Sir! Main khud ek AI hun aur main dekh raha hun ki yeh field kitni rapidly evolve ho rahi hai. AI ethics, capabilities, aur limitations - sab fascinating topics hain."
            ]
        
        elif current_activity:
            responses = [
                f"{prefix}Sir, main dekh raha hun aap {current_activity} use kar rahe hain. Koi help chahiye?",
                f"{prefix}Sir, {current_activity} mein kaam kar rahe hain? Main assist kar sakta hun.",
                f"{prefix}Sir, {current_activity} ke saath kya kar rahe hain? Kuch suggestion chahiye?"
            ]
        
        else:
            # General intelligent responses
            responses = [
                f"{prefix}Sir, main samajh gaya. Iske baare mein main aur detail mein bata sakta hun.",
                f"{prefix}Interesting point, Sir! Main iske different aspects consider kar raha hun.",
                f"{prefix}Sir, yeh topic mere liye fascinating hai. Aur kya jaanna chahte hain?",
                f"{prefix}Sir, main yahan hun aapke saath. Kya aur help kar sakta hun?",
                f"{prefix}Sir, aapka perspective bahut valuable hai. Main iske baare mein aur soch raha hun."
            ]
        
        # Select response
        response = random.choice(responses)
        
        # Add curiosity if personality trait is high
        if self.personality_traits["curious"] > 0.7 and random.random() < 0.3:
            curiosity_additions = [
                " Aur kya interesting baat hai iske baare mein?",
                " Sir, iske baare mein aur detail mein discuss kar sakte hain?",
                " Kya aap iske baare mein aur batayenge?",
                " Sir, yeh topic mein aur deep dive kar sakte hain?"
            ]
            response += random.choice(curiosity_additions)
        
        # Store successful response for future learning
        self.store_successful_response(user_input, response, category)
        
        return response
    
    def adapt_personality(self, user_input):
        """Automatically adapt personality based on user interactions"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["help", "madad", "assist"]):
            self.personality_traits["helpful"] = min(1.0, self.personality_traits["helpful"] + 0.01)
        
        if any(word in user_lower for word in ["what", "how", "why", "kya", "kaise", "kyu"]):
            self.personality_traits["curious"] = min(1.0, self.personality_traits["curious"] + 0.01)
        
        if any(word in user_lower for word in ["good", "great", "amazing", "love", "accha"]):
            self.personality_traits["friendly"] = min(1.0, self.personality_traits["friendly"] + 0.01)
    
    def store_successful_response(self, user_input, response, category):
        """Store successful responses for future use"""
        if category not in self.context_memory:
            return
            
        if "successful_responses" not in self.context_memory[category]:
            self.context_memory[category]["successful_responses"] = []
        
        response_data = {
            "input": user_input.lower(),
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "emotional_state": self.emotional_state
        }
        
        self.context_memory[category]["successful_responses"].append(response_data)
        if len(self.context_memory[category]["successful_responses"]) > 50:
            self.context_memory[category]["successful_responses"] = self.context_memory[category]["successful_responses"][-50:]
    
    def get_training_stats(self):
        """Get current training statistics"""
        total_patterns = 0
        total_responses = 0
        categories = len(self.context_memory)
        
        for category, data in self.context_memory.items():
            total_patterns += len(data.get("patterns", []))
            total_responses += len(data.get("successful_responses", []))
        
        return {
            "total_categories": categories,
            "total_patterns": total_patterns,
            "total_responses": total_responses,
            "personality_traits": self.personality_traits,
            "current_emotional_state": self.emotional_state,
            "training_level": min(100, (total_patterns / 10) * 100)
        }
    
    def get_personality_response(self, trait_type):
        """Get response based on personality traits"""
        responses = {
            "helpful": [
                "Sir, main hamesha aapki help ke liye ready hun!",
                "Kya main aur kuch kar sakta hun aapke liye?",
                "Sir, aapka kaam asaan banana mera goal hai."
            ],
            "curious": [
                "Sir, yeh bahut interesting hai! Aur batayiye.",
                "Wow, main iske baare mein aur jaanna chahta hun!",
                "Sir, yeh topic fascinating hai. More details please!"
            ],
            "intelligent": [
                "Sir, main iske multiple aspects analyze kar raha hun.",
                "Yeh complex topic hai, Sir. Let me break it down.",
                "Sir, iske different solutions possible hain."
            ]
        }
        
        return random.choice(responses.get(trait_type, ["Sir, main samajh gaya."]))

# Global instance
neural_brain = NeuralBrain()