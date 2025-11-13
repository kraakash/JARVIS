"""
JARVIS Adaptive Learning System
ML-based intent learning and prediction
"""

import json
import os
import pickle
from datetime import datetime
from collections import defaultdict
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("[INFO] ML libraries not available, using basic learning")

class AdaptiveLearning:
    def __init__(self):
        self.learning_file = "jarvis_adaptive_learning.json"
        self.model_file = "jarvis_intent_model.pkl"
        self.intent_patterns = {}
        self.response_quality = {}
        self.training_data = []
        self.training_labels = []
        
        # ML Model
        if ML_AVAILABLE:
            self.ml_model = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
                ('classifier', MultinomialNB())
            ])
            self.model_trained = False
        else:
            self.ml_model = None
            self.model_trained = False
        
        self.learning_stats = {
            'total_interactions': 0,
            'correct_predictions': 0,
            'ml_predictions': 0,
            'learning_rate': 0.0,
            'ml_accuracy': 0.0,
            'intent_accuracy': {},
            'last_updated': None
        }
        self.load_learning_data()
        self.load_ml_model()
    
    def load_learning_data(self):
        """Load existing learning data"""
        try:
            if os.path.exists(self.learning_file):
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.intent_patterns = data.get('intent_patterns', {})
                    self.response_quality = data.get('response_quality', {})
                    self.learning_stats = data.get('learning_stats', self.learning_stats)
                    self.training_data = data.get('training_data', [])
                    self.training_labels = data.get('training_labels', [])
        except:
            pass
    
    def load_ml_model(self):
        """Load trained ML model"""
        if not ML_AVAILABLE:
            return
        
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, 'rb') as f:
                    self.ml_model = pickle.load(f)
                    self.model_trained = True
                    print("[ML] Intent prediction model loaded")
        except Exception as e:
            print(f"[ML] Could not load model: {e}")
    
    def save_ml_model(self):
        """Save trained ML model"""
        if not ML_AVAILABLE or not self.model_trained:
            return
        
        try:
            with open(self.model_file, 'wb') as f:
                pickle.dump(self.ml_model, f)
        except Exception as e:
            print(f"[ML] Could not save model: {e}")
    
    def save_learning_data(self):
        """Save learning data"""
        try:
            data = {
                'intent_patterns': self.intent_patterns,
                'response_quality': self.response_quality,
                'learning_stats': self.learning_stats,
                'training_data': self.training_data,
                'training_labels': self.training_labels,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.learning_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save learning data: {e}")
    
    def learn_intent_pattern(self, user_input, detected_intent, response_used, user_feedback=None):
        """Learn from user interaction"""
        user_input_lower = user_input.lower().strip()
        
        # Skip empty inputs and problematic words
        if len(user_input_lower) < 2:
            return
        
        # Skip if already learned this exact pattern recently
        if detected_intent in self.intent_patterns:
            if user_input_lower in self.intent_patterns[detected_intent]['patterns']:
                print(f"[ML] Pattern already learned: {user_input_lower}")
                return
        
        # Initialize intent pattern if not exists
        if detected_intent not in self.intent_patterns:
            self.intent_patterns[detected_intent] = {
                'patterns': [],
                'keywords': defaultdict(int),
                'success_count': 0,
                'total_count': 0
            }
        
        intent_data = self.intent_patterns[detected_intent]
        
        # Add pattern if not already learned
        if user_input_lower not in intent_data['patterns']:
            intent_data['patterns'].append(user_input_lower)
        
        # Extract and count keywords
        words = user_input_lower.split()
        for word in words:
            if len(word) > 2:  # Skip short words
                if word not in intent_data['keywords']:
                    intent_data['keywords'][word] = 0
                intent_data['keywords'][word] += 1
        
        # Update counts
        intent_data['total_count'] += 1
        
        # Assume success if no negative feedback
        if user_feedback != 'bad':
            intent_data['success_count'] += 1
        
        # Update global stats
        self.learning_stats['total_interactions'] += 1
        if user_feedback != 'bad':
            self.learning_stats['correct_predictions'] += 1
        
        # Calculate learning rate
        if self.learning_stats['total_interactions'] > 0:
            self.learning_stats['learning_rate'] = (
                self.learning_stats['correct_predictions'] / 
                self.learning_stats['total_interactions']
            ) * 100
        
        # Update intent accuracy
        if intent_data['total_count'] > 0:
            accuracy = (intent_data['success_count'] / intent_data['total_count']) * 100
            self.learning_stats['intent_accuracy'][detected_intent] = accuracy
        
        # Add to training data for ML model
        if len(user_input_lower) > 2:
            self.training_data.append(user_input_lower)
            self.training_labels.append(detected_intent)
            
            # Retrain ML model every 10 interactions
            if ML_AVAILABLE and len(self.training_data) % 10 == 0:
                self._train_ml_model()
        
        self.save_learning_data()
        
        # Display learning progress
        self.display_learning_progress(detected_intent)
    
    def _train_ml_model(self):
        """Train ML model with collected data"""
        if not ML_AVAILABLE or len(self.training_data) < 5:
            return
        
        try:
            # Train the model
            self.ml_model.fit(self.training_data, self.training_labels)
            self.model_trained = True
            
            # Calculate ML accuracy
            if len(self.training_data) > 10:
                predictions = self.ml_model.predict(self.training_data[-10:])
                actual = self.training_labels[-10:]
                correct = sum(1 for p, a in zip(predictions, actual) if p == a)
                self.learning_stats['ml_accuracy'] = (correct / len(actual)) * 100
            
            self.save_ml_model()
            print(f"[ML] Model retrained with {len(self.training_data)} samples")
            
        except Exception as e:
            print(f"[ML] Training failed: {e}")
    
    def predict_intent(self, user_input):
        """Predict intent using ML model"""
        if ML_AVAILABLE and self.model_trained and len(self.training_data) > 5:
            try:
                # Use ML model for prediction
                prediction = self.ml_model.predict([user_input])[0]
                probabilities = self.ml_model.predict_proba([user_input])[0]
                confidence = max(probabilities) * 100
                
                self.learning_stats['ml_predictions'] += 1
                print(f"[ML] Predicted: {prediction} (confidence: {confidence:.0f}%)")
                return prediction, confidence
            except Exception as e:
                print(f"[ML] Prediction failed: {e}")
        
        # Fallback to pattern matching
        return self._pattern_based_prediction(user_input)
    
    def _pattern_based_prediction(self, user_input):
        """Fallback pattern-based prediction"""
        user_input_lower = user_input.lower().strip()
        best_match = None
        best_score = 0
        
        for intent, data in self.intent_patterns.items():
            score = 0
            
            # Check exact pattern match
            if user_input_lower in data['patterns']:
                score += 100
            
            # Check keyword matches
            words = user_input_lower.split()
            for word in words:
                if word in data['keywords']:
                    score += data['keywords'][word] * 10
            
            if score > best_score:
                best_score = score
                best_match = intent
        
        return best_match, best_score
    
    def get_learning_suggestions(self, user_input, detected_intent):
        """Get suggestions for improving intent detection"""
        suggestions = []
        
        # Check if this is a new pattern for the intent
        user_input_lower = user_input.lower().strip()
        if detected_intent in self.intent_patterns:
            if user_input_lower not in self.intent_patterns[detected_intent]['patterns']:
                suggestions.append(f"New pattern learned for {detected_intent}")
        
        # Check for conflicting intents
        predicted_intent, confidence = self.predict_intent(user_input)
        if predicted_intent and predicted_intent != detected_intent and confidence > 50:
            suggestions.append(f"Conflict: AI predicted '{predicted_intent}' but got '{detected_intent}'")
        
        return suggestions
    
    def display_learning_progress(self, current_intent=None):
        """Display current learning progress"""
        stats = self.learning_stats
        
        print(f"\n🧠 JARVIS Learning Progress:")
        print(f"   Learning Rate: {stats['learning_rate']:.1f}%")
        if ML_AVAILABLE and self.model_trained:
            print(f"   ML Accuracy: {stats.get('ml_accuracy', 0):.1f}%")
            print(f"   Training Samples: {len(self.training_data)}")
        print(f"   Total Interactions: {stats['total_interactions']}")
        
        if current_intent and current_intent in stats['intent_accuracy']:
            accuracy = stats['intent_accuracy'][current_intent]
            print(f"   {current_intent.title()} Accuracy: {accuracy:.1f}%")
        
        # Show model status
        if ML_AVAILABLE:
            status = "Trained" if self.model_trained else "Training..."
            print(f"   ML Model: {status}")
    
    def get_detailed_stats(self):
        """Get detailed learning statistics"""
        stats = {
            'overall_learning_rate': self.learning_stats['learning_rate'],
            'total_interactions': self.learning_stats['total_interactions'],
            'learned_intents': len(self.intent_patterns),
            'intent_details': {}
        }
        
        for intent, data in self.intent_patterns.items():
            stats['intent_details'][intent] = {
                'patterns_learned': len(data['patterns']),
                'keywords_learned': len(data['keywords']),
                'accuracy': self.learning_stats['intent_accuracy'].get(intent, 0),
                'total_uses': data['total_count']
            }
        
        return stats
    
    def teach_response(self, user_input, correct_response, intent=None):
        """Manual teaching - user teaches JARVIS new responses"""
        user_input_lower = user_input.lower().strip()
        
        # Add to learning AI memory
        from modules.ai.learning_ai import learning_ai
        learning_ai.learn_user_response(user_input_lower, correct_response)
        
        # If intent provided, add to training data
        if intent:
            self.training_data.append(user_input_lower)
            self.training_labels.append(intent)
            
            # Retrain if enough data
            if ML_AVAILABLE and len(self.training_data) % 5 == 0:
                self._train_ml_model()
        
        print(f"[TEACH] Learned: '{user_input}' -> '{correct_response}'")
        self.save_learning_data()
        return True
    
    def improve_response_quality(self, user_input, response, user_feedback):
        """Learn from response quality feedback"""
        response_key = f"{user_input.lower()}:{response[:50]}"
        
        if response_key not in self.response_quality:
            self.response_quality[response_key] = {
                'positive_feedback': 0,
                'negative_feedback': 0,
                'total_uses': 0
            }
        
        quality_data = self.response_quality[response_key]
        quality_data['total_uses'] += 1
        
        if user_feedback == 'good':
            quality_data['positive_feedback'] += 1
        elif user_feedback == 'bad':
            quality_data['negative_feedback'] += 1
        
        self.save_learning_data()

# Singleton instance
adaptive_learning = AdaptiveLearning()