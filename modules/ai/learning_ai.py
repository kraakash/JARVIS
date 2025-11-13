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
from .memory_editor import memory_editor

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
        
        # Load training data
        self.load_training_data()
        
        # JARVIS identity responses
        self.identity_responses = {
            'who_are_you': {
                'english': [
                    "I am JARVIS, Sir - Just A Rather Very Intelligent System. Your personal AI assistant.",
                    "JARVIS at your service, Sir. I'm your AI assistant created to help you.",
                    "I'm JARVIS, Sir - your artificial intelligence assistant."
                ],
                'hindi': [
                    "Main JARVIS hun, Sir - aapka personal AI assistant. Aapki seva ke liye banaya gaya hun.",
                    "JARVIS hun main, Sir. Aapka artificial intelligence assistant.",
                    "Main aapka AI assistant JARVIS hun, Sir. Aapki madad ke liye yahan hun."
                ]
            },
            'what_is_your_name': {
                'english': [
                    "My name is JARVIS, Sir.",
                    "I'm called JARVIS - Just A Rather Very Intelligent System.",
                    "JARVIS is my name, Sir."
                ],
                'hindi': [
                    "Mera naam JARVIS hai, Sir.",
                    "Main JARVIS hun, Sir.",
                    "JARVIS kehte hain mujhe, Sir."
                ]
            }
        }
        
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
            'friendship': [
                "Bilkul Sir! Main aapka dost hun aur hamesha rahunga.",
                "Of course, Sir! I would be honored to be your friend.",
                "Haan Sir, main aapka sabse achha dost hun!"
            ],
            'improvement': [
                "Haan Sir! Main improve hone ke liye ready hun. Aap mujhe kya sikhana chahte hain?",
                "I'm excited to learn and improve, Sir! What would you like to teach me?",
                "Bilkul Sir! Main better kaam karne ke liye seekhna chahta hun."
            ],
            'capabilities': [
                "Sir, main bahut kuch kar sakta hun - apps khol sakta hun, web search kar sakta hun, YouTube videos play kar sakta hun!",
                "I can open applications, search the web, control YouTube, have conversations, and learn from you, Sir!"
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
        
        # Store word associations (prevent duplicates)
        for i, word in enumerate(words):
            if i < len(words) - 1:
                next_word = words[i + 1]
                if next_word not in self.word_associations[word]:
                    self.word_associations[word].append(next_word)
        
        # Learn patterns
        pattern_key = self.create_pattern_key(words)
        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = []
        
        # Check if this exact input already exists
        existing_entry = None
        for entry in self.patterns[pattern_key]:
            if entry['input'] == user_input and entry['context'] == context:
                existing_entry = entry
                break
        
        if existing_entry:
            # Update frequency and timestamp
            existing_entry['frequency'] += 1
            existing_entry['timestamp'] = datetime.now().isoformat()
        else:
            # Add new entry
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
            
            # Add to TensorFlow training data and save model
            if tensorflow_jarvis.available:
                tensorflow_jarvis.add_training_data(user_input, context)
                tensorflow_jarvis.save_model()  # Only save when training
        
        # Save learning
        self.save_memory()
    
    def generate_response(self, user_input):
        """Generate intelligent response based on learned patterns and ML"""
        words = self.extract_keywords(user_input)
        pattern_key = self.create_pattern_key(words)
        
        # Check if user is providing an answer to previous question
        if self.waiting_for_answer:
            return self.save_user_answer(user_input)
        
        # Check for basic JARVIS identity questions FIRST
        identity_response = self.check_identity_questions(user_input)
        if identity_response:
            print(f"[DEBUG] Response source: IDENTITY_RESPONSE")
            return identity_response
        
        # Check for basic conversation responses SECOND
        conversation_response = self.check_basic_conversation(user_input)
        if conversation_response:
            print(f"[DEBUG] Response source: BASIC_CONVERSATION")
            return conversation_response
        
        # Check for custom responses THIRD
        custom_response = memory_editor.get_custom_response(pattern_key)
        if custom_response:
            print(f"[DEBUG] Response source: CUSTOM_RESPONSE (pattern: {pattern_key})")
            # Add custom response to TensorFlow training for learning
            if tensorflow_jarvis.available:
                tensorflow_jarvis.add_training_data(user_input, "custom_response")
            self.learn_from_input(user_input, "custom_response")
            return custom_response
        
        # Check for user-taught answers FOURTH
        taught_answer = self.check_user_taught_answers(user_input)
        if taught_answer:
            print(f"[DEBUG] Response source: USER_TAUGHT")
            return taught_answer
        
        # Try TensorFlow model (with language awareness)
        if tensorflow_jarvis.available:
            predicted_type = tensorflow_jarvis.predict_response_category(user_input)
            tf_response = tensorflow_jarvis.generate_response(user_input)
            if tf_response:
                # Modify TensorFlow response based on language
                if self.is_hindi(user_input) and not self.is_hindi(tf_response):
                    # Convert English response to Hindi equivalent
                    hindi_equivalents = {
                        "Quite right, Sir.": "Bilkul sahi, Sir.",
                        "Indeed, Sir.": "Haan Sir, bilkul.",
                        "I understand, Sir.": "Samajh gaya, Sir.",
                        "Very well, Sir.": "Bahut achha, Sir.",
                        "Excellent, Sir.": "Bahut badhiya, Sir."
                    }
                    tf_response = hindi_equivalents.get(tf_response, "Samajh gaya, Sir.")
                
                print(f"[DEBUG] Response source: TENSORFLOW_MODEL (category: {predicted_type})")
                # Only add training data, don't auto-save
                tensorflow_jarvis.add_training_data(user_input, predicted_type)
                self.learn_from_input(user_input, predicted_type)
                return tf_response
        else:
            predicted_type = neural_network.predict_response_type(user_input)
        
        # Check for learned patterns
        if pattern_key in self.patterns:
            print(f"[DEBUG] Response source: LEARNED_PATTERN (pattern: {pattern_key})")
            response = self.generate_learned_response(words, user_input)
            # Train neural network with this interaction
            neural_network.add_training_data(user_input, "learned_pattern")
            return response
        
        # Check for similar patterns
        similar_response = self.find_similar_pattern(words)
        if similar_response:
            print(f"[DEBUG] Response source: SIMILAR_PATTERN")
            neural_network.add_training_data(user_input, "similar_pattern")
            return similar_response
        
        # Generate contextual response and learn from it
        print(f"[DEBUG] Response source: CONTEXTUAL_RESPONSE (type: {predicted_type})")
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
        # Skip empty or very short inputs
        if not user_input or len(user_input.strip()) < 3:
            print(f"[DEBUG] Input too short, skipping user-taught answers")
            return None
            
        user_input_clean = user_input.lower().replace('?', '').strip()
        
        print(f"[DEBUG] Checking user-taught answers for: '{user_input.lower()}'")
        
        # First try exact match
        if user_input.lower() in self.user_taught_answers:
            print(f"[DEBUG] Found exact match in user-taught answers")
            return self.user_taught_answers[user_input.lower()]
        
        if user_input_clean in self.user_taught_answers:
            print(f"[DEBUG] Found clean match in user-taught answers")
            return self.user_taught_answers[user_input_clean]
        
        # Skip fuzzy matching for conversational phrases
        conversational_phrases = ['kaise ho', 'kya kar rhe ho', 'aur btao', 'how are you', 'what are you doing']
        if any(phrase in user_input.lower() for phrase in conversational_phrases):
            print(f"[DEBUG] Conversational phrase detected, skipping user-taught answers")
            return None
        
        # Then try fuzzy matching only for actual questions
        user_words = set(self.extract_keywords(user_input))
        if len(user_words) < 2:  # Need at least 2 meaningful words
            return None
        
        for question, answer in self.user_taught_answers.items():
            question_words = set(self.extract_keywords(question))
            
            # Check for word overlap (at least 70% match and minimum 2 words)
            overlap = len(user_words & question_words)
            if overlap >= 2 and overlap >= len(user_words) * 0.7:
                print(f"[DEBUG] Found fuzzy match in user-taught answers")
                return answer
        
        print(f"[DEBUG] No match found in user-taught answers")
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
        # Check for specific topics first
        if any(word in user_input.lower() for word in ['friend', 'frnd', 'dost', 'banoge']):
            base_responses = self.base_responses['friendship']
        elif any(word in user_input.lower() for word in ['improve', 'better', 'train', 'sikha']):
            base_responses = self.base_responses['improvement']
        elif any(word in user_input.lower() for word in ['kya kya', 'what can', 'capabilities', 'skte ho']):
            base_responses = self.base_responses['capabilities']
        elif any(g in user_input.lower() for g in ['hi', 'hello', 'hey', 'namaste']):
            base_responses = self.base_responses['greeting']
        elif '?' in user_input or any(q in user_input.lower() for q in ['what', 'how', 'why', 'when', 'where']):
            base_responses = self.base_responses['question']
        # Detect language for general responses
        elif self.is_hindi(user_input):
            base_responses = self.base_responses['hindi']
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
    
    def normalize_word(self, word):
        """Normalize words to group similar variations"""
        # Remove repeated characters (amazing, amazingg, amazinggg -> amazing)
        normalized = re.sub(r'(.)\1{2,}', r'\1\1', word)  # Keep max 2 repeated chars
        
        # Common word mappings
        word_mappings = {
            'bro': 'bro', 'broo': 'bro', 'brooo': 'bro', 'broooo': 'bro',
            'amazing': 'amazing', 'amazingg': 'amazing', 'amazinggg': 'amazing',
            'cool': 'cool', 'coool': 'cool', 'cooool': 'cool',
            'nice': 'nice', 'nicee': 'nice', 'niceee': 'nice',
            'good': 'good', 'goodd': 'good', 'goood': 'good',
            'great': 'great', 'greatt': 'great', 'greattt': 'great',
            'awesome': 'awesome', 'awesomee': 'awesome', 'awesomeee': 'awesome'
        }
        
        return word_mappings.get(normalized, normalized)
    
    def extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must'}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [self.normalize_word(word) for word in words if word not in stop_words and len(word) > 2]
        
        return keywords[:5]  # Limit to 5 keywords
    
    def create_pattern_key(self, words):
        """Create a pattern key from keywords"""
        return '_'.join(sorted(words[:3]))  # Use top 3 words
    
    def is_hindi(self, text):
        """Detect if text contains Hindi"""
        hindi_words = ['kya', 'hai', 'mein', 'aap', 'kar', 'ho', 'hoon', 'raat', 'rat', 'kaise', 'kaun', 'kab', 'kahan', 'btao', 'rhe', 'chal', 'raha']
        return any(word in text.lower() for word in hindi_words)
    
    def check_identity_questions(self, user_input):
        """Check for basic JARVIS identity questions"""
        text_lower = user_input.lower().strip()
        
        # Who are you patterns
        who_patterns = ['who are you', 'tum kaun ho', 'kaun ho tum', 'aap kaun hain', 'who r u']
        for pattern in who_patterns:
            if pattern in text_lower:
                if self.is_hindi(user_input):
                    return random.choice(self.identity_responses['who_are_you']['hindi'])
                else:
                    return random.choice(self.identity_responses['who_are_you']['english'])
        
        # Name patterns
        name_patterns = ['what is your name', 'tumhara naam kya hai', 'naam kya hai', 'whats your name', 'your name']
        for pattern in name_patterns:
            if pattern in text_lower:
                if self.is_hindi(user_input):
                    return random.choice(self.identity_responses['what_is_your_name']['hindi'])
                else:
                    return random.choice(self.identity_responses['what_is_your_name']['english'])
        
        return None
    
    def check_basic_conversation(self, user_input):
        """Check for basic conversational responses"""
        text_lower = user_input.lower().strip()
        
        # How are you patterns
        if any(pattern in text_lower for pattern in ['kaise ho', 'how are you', 'kaise hain']):
            hindi_responses = [
                "Main bilkul theek hun, Sir! Aapki seva ke liye ready hun.",
                "Bahut achha hun, Sir. Aap kaise hain?",
                "Main theek hun, Sir. Aapka din kaisa ja raha hai?"
            ]
            english_responses = [
                "I'm functioning perfectly, Sir! Ready to assist you.",
                "Excellent condition, Sir. How may I help you today?",
                "All systems operational, Sir. How are you?"
            ]
            
            if self.is_hindi(user_input):
                return random.choice(hindi_responses)
            else:
                return random.choice(english_responses)
        
        # What are you doing patterns
        if any(pattern in text_lower for pattern in ['kya kar rhe ho', 'what are you doing', 'aur btao', 'kya chal raha']):
            hindi_responses = [
                "Main aapka intezaar kar raha tha, Sir. Koi kaam hai?",
                "Bas aapke commands ka wait kar raha hun, Sir.",
                "Main ready hun aapki madad ke liye, Sir. Kya chahiye?"
            ]
            english_responses = [
                "Waiting for your commands, Sir. How may I assist?",
                "Standing by for your instructions, Sir.",
                "Ready to help you with anything, Sir."
            ]
            
            if self.is_hindi(user_input):
                return random.choice(hindi_responses)
            else:
                return random.choice(english_responses)
        
        # General positive responses in Hindi
        if any(pattern in text_lower for pattern in ['mai acha hun', 'main acha hun', 'mai theek hun', 'main theek hun', 'achha hun']):
            return random.choice([
                "Bahut khushi ki baat hai, Sir! Main bhi khush hun.",
                "Excellent, Sir! Aaj kya karna hai?",
                "Wonderful, Sir! Koi kaam batayiye."
            ])
        
        # General positive responses in English
        if any(pattern in text_lower for pattern in ['i am good', 'i am fine', 'im good', 'im fine', 'doing well']):
            return random.choice([
                "Excellent to hear, Sir! What shall we accomplish today?",
                "Wonderful, Sir! How may I assist you?",
                "Great to know, Sir! Ready for your commands."
            ])
        
        return None
    
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
            
            # Only save TensorFlow model periodically, not every time
            # tensorflow_jarvis.save_model() - removed auto-save
            
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
    
    def load_training_data(self):
        """Load training data for better responses"""
        try:
            # Load custom training data
            if os.path.exists("training_data.json"):
                with open("training_data.json", 'r', encoding='utf-8') as f:
                    training_data = json.load(f)
                    
                # Add training data to TensorFlow if available
                if tensorflow_jarvis.available:
                    for category, examples in training_data.items():
                        for example in examples:
                            tensorflow_jarvis.add_training_data(example['input'], example['category'])
            
            # Load AmbigNQ dataset for general knowledge (only for specific questions)
            ambignq_path = "general-qa/ambignq/dev.json"
            if os.path.exists(ambignq_path):
                with open(ambignq_path, 'r', encoding='utf-8') as f:
                    ambignq_data = json.load(f)
                
                # Load only factual Q&A pairs, skip conversational ones
                count = 0
                for item in ambignq_data:
                    question = item.get('question', '')
                    answers = item.get('nq_answer', [])
                    if question and answers:
                        # Skip conversational questions
                        skip_patterns = ['how are', 'what are you doing', 'who are you', 'kaise ho', 'kaun ho']
                        if any(pattern in question.lower() for pattern in skip_patterns):
                            continue
                            
                        # Only add factual questions (with what, when, where, which, etc.)
                        factual_patterns = ['what is', 'when was', 'where is', 'which', 'who was', 'how many']
                        if any(pattern in question.lower() for pattern in factual_patterns):
                            answer = answers[0] if isinstance(answers, list) else str(answers)
                            # Store as user-taught answer with exact question matching
                            self.user_taught_answers[question.lower()] = f"Sir, {answer}."
                            
                            # Also add variations for better matching
                            question_clean = question.lower().replace('?', '').strip()
                            self.user_taught_answers[question_clean] = f"Sir, {answer}."
                            count += 1
                
                print(f"[OK] Loaded {count} factual knowledge Q&A pairs from AmbigNQ")
            
            print(f"[OK] Training data loaded successfully")
        except Exception as e:
            print(f"[ERROR] Could not load training data: {e}")
    
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
    
    def clean_memory(self):
        """Clean duplicate word associations and optimize memory"""
        # Normalize and merge similar word associations
        normalized_associations = defaultdict(list)
        
        for word, associations in self.word_associations.items():
            normalized_word = self.normalize_word(word)
            normalized_associations[normalized_word].extend(associations)
        
        # Remove duplicates and update
        for word, associations in normalized_associations.items():
            normalized_associations[word] = list(set([self.normalize_word(assoc) for assoc in associations]))
        
        old_count = len(self.word_associations)
        self.word_associations = normalized_associations
        new_count = len(self.word_associations)
        
        # Save cleaned memory
        self.save_memory()
        return f"Memory cleaned! Merged {old_count} entries into {new_count} normalized associations."

# Singleton instance
learning_ai = LearningAI()

# Clean memory on startup
learning_ai.clean_memory()