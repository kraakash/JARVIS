"""
JARVIS Learning AI - Simple Neural Network for Conversation Learning
"""

import json
import os
import random
import re
from datetime import datetime
from collections import defaultdict
from .neural_network import neural_network
from .tensorflow_model import tensorflow_jarvis

class LearningAI:
    def __init__(self):
        self.data_file = "jarvis_memory.json"
        self.patterns = {}
        self.responses = {}
        self.word_associations = defaultdict(list)
        self.conversation_history = []
        self.user_taught_answers = {}  # Store user-taught Q&A pairs
        self.waiting_for_answer = None  # Track if waiting for user to teach
        
        # Load existing knowledge
        self.load_memory()
        
        # Base JARVIS responses
        self.base_responses = {
            'greeting': [
                "Good to see you, Sir!",
                "At your service, Sir.",
                "How may I assist you today, Sir?",
                "Ready for your commands, Sir."
            ],
            'question': [
                "That's an interesting question, Sir. Let me think about that.",
                "I'm processing that information, Sir.",
                "Based on what I know, Sir, I believe...",
                "Let me analyze that for you, Sir."
            ],
            'unknown': [
                "Sir, yeh mujhe nahi aata. Kya aap bata sakte hain?",
                "Maaf kijiye Sir, iske baare mein mujhe knowledge nahi hey. Aap explain kar sakte hain?",
                "Sir, main iske baare mein nahi jaanta. Aap mujhe sikha sakte hain?",
                "I don't know about this, Sir. Could you tell me more so I can learn?",
                "Yeh topic mujhe naya hey, Sir. Kya aap detail mein bata sakte hain?"
            ],
            'hindi': [
                "Sir, yeh mujhe samajh nahi aaya. Kya aap explain kar sakte hain?",
                "Maaf kijiye Sir, yeh mujhe nahi pata. Aap bata sakte hain?",
                "Sir, iske baare mein mujhe knowledge nahi hey. Sikha dijiye?",
                "Yeh naya hey mere liye, Sir. Aap detail mein batayiye."
            ]
        }
    
    def learn_from_input(self, user_input, context="general"):
        """Learn patterns from user input"""
        words = self.extract_keywords(user_input)
        
        # Store word associations
        for i, word in enumerate(words):
            if i < len(words) - 1:
                self.word_associations[word].append(words[i + 1])
        
        # Learn patterns
        pattern_key = self.create_pattern_key(words)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = []
        
        self.patterns[pattern_key].append({
            'input': user_input,
            'words': words,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'frequency': 1
        })
        
        # Train models periodically
        if len(self.patterns) % 10 == 0:  # Every 10 new patterns
            neural_network.simple_train()
            
            # Add to TensorFlow training data
            if tensorflow_jarvis.available:
                tensorflow_jarvis.add_training_data(user_input, context)
        
        # Save learning
        self.save_memory()
    
    def generate_response(self, user_input):
        """Generate intelligent response based on learned patterns and ML"""
        words = self.extract_keywords(user_input)
        pattern_key = self.create_pattern_key(words)
        
        # Check if user is providing an answer to previous question
        if self.waiting_for_answer:
            return self.save_user_answer(user_input)
        
        # Check for user-taught answers first
        taught_answer = self.check_user_taught_answers(user_input)
        if taught_answer:
            return taught_answer
        
        # Try TensorFlow model first (Phase 2), fallback to simple neural network
        if tensorflow_jarvis.available:
            predicted_type = tensorflow_jarvis.predict_response_category(user_input)
            tf_response = tensorflow_jarvis.generate_response(user_input)
            if tf_response:
                # Automatically learn from this interaction
                tensorflow_jarvis.add_training_data(user_input, predicted_type)
                self.learn_from_input(user_input, predicted_type)
                return tf_response
        else:
            predicted_type = neural_network.predict_response_type(user_input)
        
        # Check for learned patterns
        if pattern_key in self.patterns:
            response = self.generate_learned_response(words, user_input)
            # Train neural network with this interaction
            neural_network.add_training_data(user_input, "learned_pattern")
            return response
        
        # Check for similar patterns
        similar_response = self.find_similar_pattern(words)
        if similar_response:
            neural_network.add_training_data(user_input, "similar_pattern")
            return similar_response
        
        # Generate contextual response and learn from it
        response = self.generate_contextual_response(user_input, words)
        neural_network.add_training_data(user_input, predicted_type)
        
        # Add learning request for unknown topics and set waiting flag
        if 'unknown' in predicted_type or 'question' in predicted_type:
            self.waiting_for_answer = user_input  # Remember what user asked
            if self.is_hindi(user_input):
                response += " Agar aap mujhe bata denge to main yaad rakh lunga, Sir."
            else:
                response += " If you teach me, I'll remember it for next time, Sir."
        
        return response
    
    def check_user_taught_answers(self, user_input):
        """Check if user previously taught an answer for this question"""
        user_words = set(self.extract_keywords(user_input))
        
        for question, answer in self.user_taught_answers.items():
            question_words = set(self.extract_keywords(question))
            
            # Check for word overlap (at least 60% match)
            if len(user_words & question_words) >= len(user_words) * 0.6:
                return f"Main yaad hey, Sir! {answer}"
        
        return None
    
    def save_user_answer(self, user_input):
        """Save user's answer to previously asked question"""
        if self.waiting_for_answer:
            question = self.waiting_for_answer
            answer = user_input
            
            # Save the Q&A pair
            self.user_taught_answers[question] = answer
            
            # Also learn the pattern
            self.learn_from_input(f"{question} {answer}", "user_taught")
            
            # Clear waiting flag
            self.waiting_for_answer = None
            
            # Save to memory
            self.save_memory()
            
            if self.is_hindi(user_input):
                return f"Dhanyawad Sir! Main '{question}' ka jawab yaad rakh liya: '{answer}'. Agli baar main yeh answer dunga."
            else:
                return f"Thank you, Sir! I've learned that '{question}' means '{answer}'. I'll remember this for next time."
        
        return "I wasn't expecting an answer, Sir."
    
    def generate_learned_response(self, words, user_input):
        """Generate response from learned patterns"""
        responses = [
            f"I remember you asking about {' '.join(words[:2])}, Sir.",
            f"Based on our previous conversations about {words[0] if words else 'this'}, Sir...",
            f"I've learned that when you mention {words[0] if words else 'this'}, you usually want...",
            f"From what I've observed, Sir, this relates to {' '.join(words[:2])}."
        ]
        
        # Add Hindi responses if Hindi detected
        if self.is_hindi(user_input):
            responses.extend([
                f"Mein yaad hey, Sir, aap {words[0] if words else 'yeh'} ke baare mein puch rahe the.",
                f"Pehle bhi aap {words[0] if words else 'iske'} baare mein baat kar rahe the, Sir.",
                f"Meine seekha hey ki jab aap {words[0] if words else 'yeh'} kehte hain..."
            ])
        
        return random.choice(responses)
    
    def find_similar_pattern(self, words):
        """Find similar learned patterns"""
        for pattern_key, patterns in self.patterns.items():
            pattern_words = pattern_key.split('_')
            
            # Check for word overlap
            overlap = set(words) & set(pattern_words)
            if len(overlap) >= 2:  # At least 2 words match
                recent_pattern = patterns[-1]  # Get most recent
                return f"This reminds me of when you asked about {recent_pattern['input'][:30]}..., Sir."
        
        return None
    
    def generate_contextual_response(self, user_input, words):
        """Generate contextual response based on input analysis"""
        # Detect language
        if self.is_hindi(user_input):
            base_responses = self.base_responses['hindi']
        elif '?' in user_input or any(q in user_input.lower() for q in ['what', 'how', 'why', 'when', 'where']):
            base_responses = self.base_responses['question']
        elif any(g in user_input.lower() for g in ['hi', 'hello', 'hey', 'namaste']):
            base_responses = self.base_responses['greeting']
        else:
            base_responses = self.base_responses['unknown']
        
        response = random.choice(base_responses)
        
        # Add learned context if available
        if words and len(self.word_associations) > 0:
            key_word = words[0]
            if key_word in self.word_associations:
                associated = random.choice(self.word_associations[key_word])
                response += f" I notice you often mention {associated} with {key_word}."
        
        # Add learning confirmation for new inputs
        if len(self.patterns) > 0 and words:
            response += f" Main '{' '.join(words[:2])}' ke baare mein seekh raha hun."
        
        return response
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Limit to 5 keywords
    
    def create_pattern_key(self, words):
        """Create a pattern key from keywords"""
        return '_'.join(sorted(words[:3]))  # Use top 3 words
    
    def is_hindi(self, text):
        """Detect if text contains Hindi"""
        hindi_words = ['kya', 'hai', 'mein', 'aap', 'kar', 'ho', 'hoon', 'raat', 'rat', 'kaise', 'kaun', 'kab', 'kahan']
        return any(word in text.lower() for word in hindi_words)
    
    def save_memory(self):
        """Save learned patterns and neural network"""
        try:
            memory_data = {
                'patterns': self.patterns,
                'word_associations': dict(self.word_associations),
                'user_taught_answers': self.user_taught_answers,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            
            # Save neural network model
            neural_network.save_model()
            
            # Save TensorFlow model
            if tensorflow_jarvis.available:
                tensorflow_jarvis.save_model()
            
        except Exception as e:
            print(f"[ERROR] Could not save memory: {e}")
    
    def load_memory(self):
        """Load learned patterns from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                
                self.patterns = memory_data.get('patterns', {})
                self.word_associations = defaultdict(list, memory_data.get('word_associations', {}))
                self.user_taught_answers = memory_data.get('user_taught_answers', {})
                
                print(f"[OK] Loaded {len(self.patterns)} learned patterns and {len(self.user_taught_answers)} user-taught answers")
        except Exception as e:
            print(f"[ERROR] Could not load memory: {e}")
    
    def get_learning_stats(self):
        """Get statistics about learned knowledge"""
        ml_stats = neural_network.get_model_stats()
        tf_stats = tensorflow_jarvis.get_model_info()
        return {
            'total_patterns': len(self.patterns),
            'word_associations': len(self.word_associations),
            'memory_file_exists': os.path.exists(self.data_file),
            'simple_ml_model': ml_stats,
            'tensorflow_model': tf_stats
        }

# Singleton instance
learning_ai = LearningAI()