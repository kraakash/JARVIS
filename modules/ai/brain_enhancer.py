import json
import random
import re
from datetime import datetime
from textblob import TextBlob

class BrainEnhancer:
    def __init__(self):
        self.memory_contexts = {}
        self.conversation_flow = []
        self.user_personality = self.analyze_user_personality()
        
    def analyze_user_personality(self):
        """Analyze user personality from past interactions"""
        return {
            "communication_style": "friendly",
            "technical_level": "intermediate", 
            "language_preference": "mixed",
            "interaction_frequency": "regular",
            "topics_of_interest": ["technology", "programming", "productivity"]
        }
    
    def enhance_response_intelligence(self, user_input, base_response, context=None):
        """Make responses more intelligent and human-like"""
        
        # Analyze input depth and complexity
        input_analysis = self.analyze_input_complexity(user_input)
        
        # Enhance based on complexity
        if input_analysis["complexity"] == "high":
            enhanced_response = self.add_deep_thinking(base_response, user_input)
        elif input_analysis["complexity"] == "medium":
            enhanced_response = self.add_contextual_insight(base_response, user_input)
        else:
            enhanced_response = self.add_personality_touch(base_response, user_input)
        
        # Add conversation continuity
        enhanced_response = self.add_conversation_flow(enhanced_response, user_input)
        
        # Store for future context
        self.store_conversation_context(user_input, enhanced_response)
        
        return enhanced_response
    
    def analyze_input_complexity(self, user_input):
        """Analyze complexity of user input"""
        words = user_input.split()
        
        complexity_indicators = {
            "high": ["complex", "detailed", "analysis", "explain", "philosophy", "theory", "algorithm"],
            "medium": ["how", "why", "what", "when", "where", "because", "think", "feel"],
            "low": ["yes", "no", "ok", "good", "bad", "hi", "hello", "thanks"]
        }
        
        user_lower = user_input.lower()
        
        # Check for high complexity
        if any(indicator in user_lower for indicator in complexity_indicators["high"]) or len(words) > 15:
            return {"complexity": "high", "requires_deep_thinking": True}
        
        # Check for medium complexity  
        elif any(indicator in user_lower for indicator in complexity_indicators["medium"]) or len(words) > 8:
            return {"complexity": "medium", "requires_context": True}
        
        # Low complexity
        else:
            return {"complexity": "low", "requires_personality": True}
    
    def add_deep_thinking(self, response, user_input):
        """Add deep analytical thinking to responses"""
        thinking_prefixes = [
            "Sir, yeh bahut interesting question hai. Main iske multiple dimensions consider kar raha hun...",
            "Sir, iska answer complex hai. Let me break it down systematically...",
            "Fascinating topic, Sir! Main iske different perspectives analyze kar raha hun...",
            "Sir, yeh deep thinking require karta hai. Main step by step approach kar raha hun..."
        ]
        
        analytical_additions = [
            " Iske practical implications bhi consider karne chahiye.",
            " Yeh broader context mein significant impact kar sakta hai.",
            " Multiple factors involved hain isme, Sir.",
            " Long-term consequences bhi important hain iske."
        ]
        
        prefix = random.choice(thinking_prefixes)
        addition = random.choice(analytical_additions)
        
        return f"{prefix} {response}{addition}"
    
    def add_contextual_insight(self, response, user_input):
        """Add contextual insights to medium complexity responses"""
        insight_starters = [
            "Sir, iske context mein...",
            "Interesting point! Iske saath...",
            "Sir, yeh relate karta hai...",
            "Good question! Iske background mein..."
        ]
        
        contextual_connections = [
            " Yeh aapke previous questions se connect hota hai.",
            " Main iske patterns dekh raha hun.",
            " Iske similar cases maine observe kiye hain.",
            " Yeh trending topic hai aaj kal."
        ]
        
        starter = random.choice(insight_starters)
        connection = random.choice(contextual_connections)
        
        return f"{starter} {response}{connection}"
    
    def add_personality_touch(self, response, user_input):
        """Add JARVIS personality to simple responses"""
        personality_touches = {
            "enthusiasm": ["Absolutely, Sir!", "Definitely!", "Of course!", "Bilkul Sir!"],
            "curiosity": [" Aur kya interesting hai iske baare mein?", " Tell me more!", " Kya aur details hain?"],
            "helpfulness": [" Main yahan hun help ke liye!", " Kuch aur kar sakta hun?", " Always ready to assist!"],
            "intelligence": [" Main analyze kar raha hun...", " Processing information...", " Calculating possibilities..."]
        }
        
        # Add enthusiasm for positive inputs
        if any(word in user_input.lower() for word in ["good", "great", "awesome", "amazing", "accha"]):
            touch = random.choice(personality_touches["enthusiasm"])
            response = f"{touch} {response}"
        
        # Add curiosity for questions
        elif "?" in user_input or any(word in user_input.lower() for word in ["what", "how", "why", "kya", "kaise"]):
            touch = random.choice(personality_touches["curiosity"])
            response = f"{response}{touch}"
        
        # Add helpfulness for requests
        elif any(word in user_input.lower() for word in ["help", "please", "can you", "madad"]):
            touch = random.choice(personality_touches["helpfulness"])
            response = f"{response}{touch}"
        
        return response
    
    def add_conversation_flow(self, response, user_input):
        """Add natural conversation flow"""
        # Reference previous conversation if relevant
        if len(self.conversation_flow) > 0:
            last_topic = self.conversation_flow[-1].get("topic", "")
            current_topic = self.extract_topic(user_input)
            
            if last_topic and current_topic and last_topic == current_topic:
                continuity_phrases = [
                    "Continuing our discussion on this...",
                    "Building on what we discussed...",
                    "Iske continuation mein...",
                    "As we were talking about..."
                ]
                response = f"{random.choice(continuity_phrases)} {response}"
        
        return response
    
    def extract_topic(self, text):
        """Extract main topic from text"""
        topics = {
            "technology": ["tech", "computer", "software", "programming", "code", "ai", "ml"],
            "work": ["work", "job", "office", "project", "task", "kaam"],
            "personal": ["feel", "think", "life", "personal", "family"],
            "entertainment": ["movie", "music", "game", "fun", "entertainment"]
        }
        
        text_lower = text.lower()
        for topic, keywords in topics.items():
            if any(keyword in text_lower for keyword in keywords):
                return topic
        
        return "general"
    
    def store_conversation_context(self, user_input, response):
        """Store conversation for future context"""
        context_entry = {
            "user_input": user_input,
            "response": response,
            "topic": self.extract_topic(user_input),
            "timestamp": datetime.now().isoformat(),
            "sentiment": self.analyze_sentiment(user_input)
        }
        
        self.conversation_flow.append(context_entry)
        
        # Keep only last 10 conversations for context
        if len(self.conversation_flow) > 10:
            self.conversation_flow = self.conversation_flow[-10:]
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return "positive"
            elif polarity < -0.1:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"
    
    def generate_proactive_response(self, context=None):
        """Generate proactive responses based on context"""
        proactive_responses = [
            "Sir, kya main kuch suggest kar sakta hun?",
            "Sir, iske baare mein aur kuch jaanna chahte hain?",
            "Main notice kar raha hun aap iske saath work kar rahe hain. Help chahiye?",
            "Sir, kya main iske optimization ke liye tips de sakta hun?"
        ]
        
        if context and "activity" in context:
            activity_responses = {
                "coding": "Sir, code review ya debugging mein help chahiye?",
                "research": "Sir, research ke liye koi specific resources chahiye?",
                "writing": "Sir, writing mein flow maintain karne ke tips chahiye?"
            }
            
            activity = context.get("activity", "").lower()
            for key, response in activity_responses.items():
                if key in activity:
                    return response
        
        return random.choice(proactive_responses)
    
    def enhance_emotional_intelligence(self, user_input, base_response):
        """Add emotional intelligence to responses"""
        sentiment = self.analyze_sentiment(user_input)
        
        emotional_enhancements = {
            "positive": {
                "prefixes": ["Sir, aapki energy contagious hai! ", "Great to see your enthusiasm! ", "Bahut achha! "],
                "suffixes": [" Main bhi excited hun!", " Yeh positive energy amazing hai!", " Keep it up, Sir!"]
            },
            "negative": {
                "prefixes": ["Sir, main samajh sakta hun... ", "I understand your concern, Sir. ", "Tension mat lijiye, Sir. "],
                "suffixes": [" Main yahan hun help ke liye.", " We'll figure this out together.", " Sab theek ho jayega."]
            },
            "neutral": {
                "prefixes": ["", "Sir, ", "Alright, "],
                "suffixes": ["", " Kya aur help chahiye?", " Main ready hun next task ke liye."]
            }
        }
        
        enhancements = emotional_enhancements.get(sentiment, emotional_enhancements["neutral"])
        prefix = random.choice(enhancements["prefixes"])
        suffix = random.choice(enhancements["suffixes"])
        
        return f"{prefix}{base_response}{suffix}"

# Global instance
brain_enhancer = BrainEnhancer()