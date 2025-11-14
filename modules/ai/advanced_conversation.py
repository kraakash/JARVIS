import json
import random
import re
from datetime import datetime
import requests
from textblob import TextBlob

class AdvancedConversation:
    def __init__(self):
        self.conversation_history = []
        self.user_preferences = {}
        self.topic_knowledge = self.load_topic_knowledge()
        
    def load_topic_knowledge(self):
        """Load comprehensive topic knowledge"""
        return {
            "technology": {
                "keywords": ["computer", "software", "programming", "code", "tech", "ai", "ml", "python", "java"],
                "responses": [
                    "Sir, technology ke field mein main bahut interested hun! Kya specific topic discuss karna chahte hain?",
                    "Technology fascinating hai, Sir! Main programming aur AI ke baare mein bahut kuch janta hun.",
                    "Sir, tech world mein har din kuch naya hota hai. Kya latest trends ke baare mein baat karenge?"
                ]
            },
            "science": {
                "keywords": ["physics", "chemistry", "biology", "space", "universe", "science", "research"],
                "responses": [
                    "Science mere favorite topics mein se ek hai, Sir! Kya explore karna chahte hain?",
                    "Sir, science ke wonders infinite hain! Kya specific field mein interest hai?",
                    "Amazing, Sir! Science ke through hum universe ko samajh sakte hain."
                ]
            },
            "entertainment": {
                "keywords": ["movie", "music", "game", "fun", "entertainment", "film", "song"],
                "responses": [
                    "Entertainment ke baare mein baat karna mujhe pasand hai, Sir! Kya favorite genre hai?",
                    "Sir, movies aur music life mein colors bharte hain! Kya recommend karu?",
                    "Fun topics mere liye refreshing hain, Sir! Kya discuss karenge?"
                ]
            },
            "personal": {
                "keywords": ["feel", "think", "opinion", "like", "love", "hate", "prefer"],
                "responses": [
                    "Sir, aapke thoughts mere liye valuable hain! Main sunna chahta hun.",
                    "Personal opinions share karna trust ki baat hai, Sir. Main appreciate karta hun.",
                    "Sir, aapke perspective se main bahut kuch seekhta hun!"
                ]
            },
            "work": {
                "keywords": ["work", "job", "office", "project", "task", "kaam", "office"],
                "responses": [
                    "Work ke baare mein discuss karna productive hai, Sir! Kya challenges hain?",
                    "Sir, main aapke work mein help kar sakta hun! Kya support chahiye?",
                    "Professional life important hai, Sir. Kaise optimize kar sakte hain?"
                ]
            }
        }
    
    def detect_topic(self, user_input):
        """Detect conversation topic"""
        user_lower = user_input.lower()
        
        for topic, data in self.topic_knowledge.items():
            if any(keyword in user_lower for keyword in data["keywords"]):
                return topic
        
        return "general"
    
    def generate_follow_up_question(self, topic, user_input):
        """Generate intelligent follow-up questions"""
        follow_ups = {
            "technology": [
                "Sir, kya aap programming languages mein se koi favorite hai?",
                "Technology trends ke baare mein aapka kya opinion hai?",
                "Sir, AI ke future ke baare mein kya sochte hain?",
                "Kya aap latest tech innovations follow karte hain?"
            ],
            "science": [
                "Sir, space exploration ke baare mein kya fascinating lagta hai?",
                "Science ke kya aspects aapko most interesting lagte hain?",
                "Sir, kya aap research papers padhte hain?",
                "Future scientific discoveries ke baare mein kya expectations hain?"
            ],
            "entertainment": [
                "Sir, recent mein koi good movie dekhi hai?",
                "Music mein kya genre prefer karte hain?",
                "Sir, entertainment ke liye time kaise nikaalte hain?",
                "Kya recommendations hain mere liye?"
            ],
            "personal": [
                "Sir, aapke hobbies kya hain?",
                "Life mein kya motivate karta hai aapko?",
                "Sir, free time mein kya karna pasand hai?",
                "Kya goals hain future ke liye?"
            ],
            "work": [
                "Sir, work-life balance kaise maintain karte hain?",
                "Kya challenges face kar rahe hain currently?",
                "Sir, productivity tips share kar sakte hain?",
                "Team work ke baare mein kya experience hai?"
            ]
        }
        
        return random.choice(follow_ups.get(topic, [
            "Sir, iske baare mein aur detail mein bata sakte hain?",
            "Interesting! Aur kya thoughts hain iske baare mein?",
            "Sir, yeh topic fascinating hai. More insights please!"
        ]))
    
    def analyze_conversation_depth(self, user_input):
        """Analyze how deep the conversation should go"""
        depth_indicators = {
            "surface": ["yes", "no", "ok", "fine", "good", "haan", "nahi", "theek"],
            "medium": ["because", "think", "feel", "maybe", "probably", "kyunki", "lagta"],
            "deep": ["philosophy", "meaning", "purpose", "complex", "detailed", "analysis"]
        }
        
        user_lower = user_input.lower()
        
        for depth, indicators in depth_indicators.items():
            if any(indicator in user_lower for indicator in indicators):
                return depth
        
        # Default based on length
        if len(user_input.split()) > 10:
            return "deep"
        elif len(user_input.split()) > 5:
            return "medium"
        else:
            return "surface"
    
    def generate_contextual_response(self, user_input, conversation_history=None):
        """Generate highly contextual response"""
        topic = self.detect_topic(user_input)
        depth = self.analyze_conversation_depth(user_input)
        
        # Store conversation
        self.conversation_history.append({
            "user": user_input,
            "topic": topic,
            "depth": depth,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate base response
        if topic in self.topic_knowledge:
            base_response = random.choice(self.topic_knowledge[topic]["responses"])
        else:
            base_response = self.generate_general_response(user_input)
        
        # Add depth-based elaboration
        if depth == "deep":
            elaboration = self.add_deep_insight(topic, user_input)
            response = f"{base_response} {elaboration}"
        elif depth == "medium":
            follow_up = self.generate_follow_up_question(topic, user_input)
            response = f"{base_response} {follow_up}"
        else:
            response = base_response
        
        # Add personality touch
        response = self.add_personality_touch(response, user_input)
        
        return response
    
    def generate_general_response(self, user_input):
        """Generate general intelligent response"""
        user_lower = user_input.lower()
        
        # Question responses
        if any(word in user_lower for word in ["kya", "what", "how", "kaise", "why", "kyu", "when", "kab"]):
            return random.choice([
                "Sir, yeh bahut interesting question hai! Main iske different aspects consider kar raha hun.",
                "Great question, Sir! Iske baare mein detail mein discuss kar sakte hain.",
                "Sir, yeh complex topic hai. Main step by step explain kar sakta hun.",
                "Fascinating question! Main iske multiple perspectives analyze kar raha hun."
            ])
        
        # Statement responses
        elif any(word in user_lower for word in ["think", "feel", "believe", "lagta", "sochta"]):
            return random.choice([
                "Sir, aapka perspective valuable hai! Main iske baare mein aur jaanna chahta hun.",
                "Interesting viewpoint, Sir! Iske behind reasoning kya hai?",
                "Sir, aapke thoughts always insightful hote hain. Elaborate kar sakte hain?",
                "Great insight! Main iske implications ke baare mein soch raha hun."
            ])
        
        # Default responses
        else:
            return random.choice([
                "Sir, main samajh gaya. Iske baare mein aur discuss kar sakte hain.",
                "Interesting, Sir! Main iske different angles consider kar raha hun.",
                "Sir, yeh topic mere liye fascinating hai. More details please!",
                "Sir, aapke saath conversation hamesha enlightening hoti hai!"
            ])
    
    def add_deep_insight(self, topic, user_input):
        """Add deep insights for complex conversations"""
        insights = {
            "technology": [
                "Technology ka evolution human civilization ko fundamentally change kar raha hai.",
                "AI aur machine learning ke through hum new possibilities explore kar sakte hain.",
                "Digital transformation har industry ko revolutionize kar raha hai."
            ],
            "science": [
                "Science ke through hum universe ke mysteries unlock kar sakte hain.",
                "Scientific method critical thinking develop karta hai.",
                "Research aur innovation future ke solutions provide karte hain."
            ],
            "personal": [
                "Personal growth continuous journey hai, Sir.",
                "Self-reflection se hum better decisions le sakte hain.",
                "Life experiences wisdom provide karte hain."
            ]
        }
        
        return random.choice(insights.get(topic, [
            "Yeh topic bahut multi-dimensional hai, Sir.",
            "Iske philosophical implications bhi interesting hain.",
            "Sir, yeh broader context mein significant hai."
        ]))
    
    def add_personality_touch(self, response, user_input):
        """Add JARVIS personality to response"""
        # Emotional context
        if any(word in user_input.lower() for word in ["sad", "upset", "problem", "issue", "dukh"]):
            response = f"Sir, main samajh sakta hun. {response} Main yahan hun aapke saath."
        
        elif any(word in user_input.lower() for word in ["happy", "good", "great", "khush", "accha"]):
            response = f"Sir, aapki khushi meri khushi hai! {response}"
        
        elif any(word in user_input.lower() for word in ["confused", "don't know", "samajh nahi"]):
            response = f"No worries, Sir! {response} Main step by step explain karunga."
        
        # Add encouraging endings
        encouraging_endings = [
            " Aur kya discuss karna chahte hain?",
            " Sir, main hamesha yahan hun help ke liye!",
            " Kya aur insights share kar sakte hain?",
            " Sir, aapke thoughts valuable hain!"
        ]
        
        if random.random() < 0.4:  # 40% chance to add encouraging ending
            response += random.choice(encouraging_endings)
        
        return response
    
    def get_conversation_summary(self):
        """Get summary of recent conversations"""
        if not self.conversation_history:
            return "Sir, abhi tak koi detailed conversation nahi hui hai."
        
        recent_topics = [conv["topic"] for conv in self.conversation_history[-5:]]
        topic_counts = {}
        for topic in recent_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        most_discussed = max(topic_counts, key=topic_counts.get)
        
        return f"Sir, recent conversations mein hum mainly {most_discussed} ke baare mein discuss kar rahe hain. Total {len(self.conversation_history)} conversations hui hain."

# Global instance
advanced_conversation = AdvancedConversation()