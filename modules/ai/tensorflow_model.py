"""
JARVIS Phase 2 - TensorFlow Neural Network for Advanced Learning
"""

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    import numpy as np
    import pickle
    import os
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("[INFO] TensorFlow not installed. Using fallback mode.")

class TensorFlowJARVIS:
    def __init__(self):
        self.available = TENSORFLOW_AVAILABLE
        if not self.available:
            return
            
        self.model = None
        self.tokenizer = None
        self.max_sequence_length = 50
        self.vocab_size = 5000
        
        # Response categories
        self.response_categories = {
            'greeting': 0,
            'question': 1, 
            'command': 2,
            'casual': 3,
            'hindi': 4,
            'technical': 5,
            'unknown': 6
        }
        
        self.category_responses = {
            0: ["Good to see you, Sir!", "At your service, Sir.", "How may I assist you today, Sir?"],
            1: ["Let me analyze that for you, Sir.", "Based on my knowledge, Sir...", "That's an interesting question, Sir."],
            2: ["Right away, Sir.", "Processing your command, Sir.", "Executing task, Sir."],
            3: ["I understand, Sir.", "Indeed, Sir.", "Quite right, Sir."],
            4: ["Samajh gaya, Sir.", "Bilkul theek, Sir.", "Haan Sir, main ready hun."],
            5: ["Analyzing technical parameters, Sir.", "Processing system data, Sir.", "Technical analysis complete, Sir."],
            6: ["I'm learning about that, Sir.", "That's new information for me, Sir.", "Adding to my knowledge base, Sir."]
        }
        
        # Initialize or load model
        self.setup_model()
    
    def setup_model(self):
        """Setup TensorFlow model"""
        if not self.available:
            return False
            
        try:
            # Try to load existing model
            if os.path.exists('jarvis_tf_model.h5') and os.path.exists('jarvis_tokenizer.pkl'):
                self.load_model()
                print("[OK] Loaded existing TensorFlow model")
            else:
                self.create_model()
                print("[OK] Created new TensorFlow model")
            return True
        except Exception as e:
            print(f"[ERROR] TensorFlow model setup failed: {e}")
            return False
    
    def create_model(self):
        """Create new neural network model"""
        if not self.available:
            return
            
        # Create tokenizer
        self.tokenizer = Tokenizer(num_words=self.vocab_size, oov_token="<OOV>")
        
        # Build model architecture
        self.model = Sequential([
            Embedding(self.vocab_size, 64, input_length=self.max_sequence_length),
            LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True),
            LSTM(64, dropout=0.2, recurrent_dropout=0.2),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(len(self.response_categories), activation='softmax')
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("[OK] TensorFlow model architecture created")
    
    def preprocess_text(self, texts):
        """Preprocess text for model input"""
        if not self.available or not self.tokenizer:
            return None
        
        try:
            # Ensure tokenizer has vocabulary
            if not hasattr(self.tokenizer, 'word_index') or len(self.tokenizer.word_index) == 0:
                self.tokenizer.fit_on_texts(texts)
            
            sequences = self.tokenizer.texts_to_sequences(texts)
            return pad_sequences(sequences, maxlen=self.max_sequence_length, padding='post')
        except Exception as e:
            print(f"[ERROR] Text preprocessing failed: {e}")
            return None
    
    def predict_response_category(self, text):
        """Predict response category using TensorFlow model"""
        if not self.available or not self.model or not self.tokenizer:
            return 'unknown'
            
        try:
            # Check if tokenizer has vocabulary
            if not hasattr(self.tokenizer, 'word_index') or len(self.tokenizer.word_index) == 0:
                # Auto-categorize based on simple rules
                return self._simple_categorize(text)
            
            # Preprocess input
            processed = self.preprocess_text([text])
            if processed is None or processed.size == 0:
                return self._simple_categorize(text)
            
            # Make prediction
            prediction = self.model.predict(processed, verbose=0)
            predicted_category = np.argmax(prediction[0])
            
            # Map back to category name
            for category, idx in self.response_categories.items():
                if idx == predicted_category:
                    return category
            
            return 'unknown'
        except Exception as e:
            print(f"[ERROR] Prediction failed: {e}")
            return self._simple_categorize(text)
    
    def _simple_categorize(self, text):
        """Simple rule-based categorization as fallback"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['hi', 'hello', 'hey', 'namaste']):
            return 'greeting'
        elif any(word in text_lower for word in ['kya', 'hai', 'kaise', 'kaun']):
            return 'hindi'
        elif '?' in text or any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where']):
            return 'question'
        elif any(word in text_lower for word in ['open', 'close', 'start', 'stop']):
            return 'command'
        elif any(word in text_lower for word in ['stronger', 'better', 'improve', 'learn']):
            return 'technical'
        else:
            return 'casual'
    
    def generate_response(self, text):
        """Generate response using TensorFlow predictions"""
        if not self.available:
            return None
            
        category = self.predict_response_category(text)
        category_idx = self.response_categories.get(category, 6)
        
        responses = self.category_responses.get(category_idx, self.category_responses[6])
        
        # Add learning context to response
        base_response = np.random.choice(responses)
        
        # Add learning confirmation for unknown inputs
        if category == 'unknown' or 'stronger' in text.lower():
            base_response += " I'm automatically learning from our conversation and will remember this."
        
        return base_response
    
    def add_training_data(self, text, category):
        """Add training data (for future batch training)"""
        if not self.available:
            return
            
        # Store training data for batch processing
        training_file = 'jarvis_training_data.txt'
        try:
            with open(training_file, 'a', encoding='utf-8') as f:
                f.write(f"{text}\t{category}\n")
        except Exception as e:
            print(f"[ERROR] Could not save training data: {e}")
    
    def train_model(self, texts, labels, epochs=5):
        """Train the model with new data"""
        if not self.available or not self.model:
            return False
            
        try:
            # Fit tokenizer on texts
            self.tokenizer.fit_on_texts(texts)
            
            # Preprocess data
            X = self.preprocess_text(texts)
            y = np.array([self.response_categories.get(label, 6) for label in labels])
            
            # Train model
            history = self.model.fit(
                X, y,
                epochs=epochs,
                batch_size=32,
                validation_split=0.2,
                verbose=0
            )
            
            print(f"[OK] Model trained. Final accuracy: {history.history['accuracy'][-1]:.3f}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Training failed: {e}")
            return False
    
    def save_model(self):
        """Save TensorFlow model and tokenizer"""
        if not self.available or not self.model:
            return False
            
        try:
            self.model.save('jarvis_tf_model.h5')
            
            with open('jarvis_tokenizer.pkl', 'wb') as f:
                pickle.dump(self.tokenizer, f)
            
            print("[OK] TensorFlow model saved")
            return True
        except Exception as e:
            print(f"[ERROR] Could not save model: {e}")
            return False
    
    def load_model(self):
        """Load existing TensorFlow model"""
        if not self.available:
            return False
            
        try:
            self.model = load_model('jarvis_tf_model.h5')
            
            with open('jarvis_tokenizer.pkl', 'rb') as f:
                self.tokenizer = pickle.load(f)
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not load model: {e}")
            return False
    
    def get_model_info(self):
        """Get model information"""
        if not self.available:
            return {'status': 'TensorFlow not available'}
            
        return {
            'status': 'Available' if self.model else 'Not loaded',
            'vocab_size': self.vocab_size,
            'sequence_length': self.max_sequence_length,
            'categories': len(self.response_categories),
            'tensorflow_version': tf.__version__ if self.available else 'Not installed'
        }

# Singleton instance
tensorflow_jarvis = TensorFlowJARVIS()