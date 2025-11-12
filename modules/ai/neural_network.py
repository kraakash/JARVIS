"""
JARVIS Neural Network - Simple ML Model for Future Expansion
"""

import numpy as np
import json
import os
from datetime import datetime

class SimpleNeuralNetwork:
    def __init__(self, input_size=100, hidden_size=50, output_size=20):
        # Initialize weights randomly
        self.W1 = np.random.randn(input_size, hidden_size) * 0.1
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.1
        self.b2 = np.zeros((1, output_size))
        
        # Vocabulary for text processing
        self.vocab = {}
        self.response_classes = {}
        self.training_data = []
        
        # Load existing model if available
        self.load_model()
    
    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def softmax(self, x):
        """Softmax activation for output layer"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
    
    def text_to_vector(self, text):
        """Convert text to numerical vector"""
        words = text.lower().split()
        vector = np.zeros(len(self.W1))
        
        for word in words:
            if word not in self.vocab:
                self.vocab[word] = len(self.vocab)
            
            if self.vocab[word] < len(vector):
                vector[self.vocab[word]] = 1
        
        return vector.reshape(1, -1)
    
    def forward(self, X):
        """Forward pass through network"""
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)
        return self.a2
    
    def predict_response_type(self, text):
        """Predict response type for given text"""
        if len(self.vocab) == 0:
            return "general"
        
        X = self.text_to_vector(text)
        output = self.forward(X)
        
        # Get predicted class
        predicted_class = np.argmax(output)
        
        # Map back to response type
        for response_type, class_id in self.response_classes.items():
            if class_id == predicted_class:
                return response_type
        
        return "general"
    
    def add_training_data(self, text, response_type):
        """Add training data for future learning"""
        self.training_data.append({
            'text': text,
            'response_type': response_type,
            'timestamp': datetime.now().isoformat()
        })
        
        # Add response type to classes if new
        if response_type not in self.response_classes:
            self.response_classes[response_type] = len(self.response_classes)
        
        # Keep only recent 1000 training examples
        if len(self.training_data) > 1000:
            self.training_data = self.training_data[-1000:]
    
    def simple_train(self):
        """Simple training method (placeholder for future ML training)"""
        if len(self.training_data) < 10:
            return False
        
        # For now, just update vocabulary and response classes
        for data in self.training_data[-50:]:  # Use recent 50 examples
            self.text_to_vector(data['text'])  # Updates vocab
        
        return True
    
    def save_model(self):
        """Save model weights and vocabulary"""
        try:
            model_data = {
                'vocab': self.vocab,
                'response_classes': self.response_classes,
                'training_data': self.training_data[-100:],  # Save recent 100
                'model_info': {
                    'input_size': self.W1.shape[0],
                    'hidden_size': self.W1.shape[1],
                    'output_size': self.W2.shape[1],
                    'last_updated': datetime.now().isoformat()
                }
            }
            
            with open('jarvis_neural_model.json', 'w') as f:
                json.dump(model_data, f, indent=2)
            
            # Save weights separately (numpy arrays)
            np.savez('jarvis_weights.npz', 
                    W1=self.W1, b1=self.b1, 
                    W2=self.W2, b2=self.b2)
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not save model: {e}")
            return False
    
    def load_model(self):
        """Load existing model"""
        try:
            if os.path.exists('jarvis_neural_model.json'):
                with open('jarvis_neural_model.json', 'r') as f:
                    model_data = json.load(f)
                
                self.vocab = model_data.get('vocab', {})
                self.response_classes = model_data.get('response_classes', {})
                self.training_data = model_data.get('training_data', [])
                
                print(f"[OK] Loaded neural model with {len(self.vocab)} vocabulary")
            
            if os.path.exists('jarvis_weights.npz'):
                weights = np.load('jarvis_weights.npz')
                self.W1 = weights['W1']
                self.b1 = weights['b1']
                self.W2 = weights['W2']
                self.b2 = weights['b2']
                
                print(f"[OK] Loaded neural network weights")
                
        except Exception as e:
            print(f"[ERROR] Could not load model: {e}")
    
    def get_model_stats(self):
        """Get model statistics"""
        return {
            'vocabulary_size': len(self.vocab),
            'response_classes': len(self.response_classes),
            'training_examples': len(self.training_data),
            'network_shape': f"{self.W1.shape[0]}-{self.W1.shape[1]}-{self.W2.shape[1]}"
        }

# Future ML Integration Plan:
"""
FUTURE UPGRADES:
1. Replace with TensorFlow/PyTorch for real deep learning
2. Add LSTM/Transformer for better text understanding  
3. Implement proper backpropagation training
4. Add word embeddings (Word2Vec/GloVe)
5. Use pre-trained models (BERT/GPT for conversation)
6. Add reinforcement learning for user feedback
7. Implement attention mechanisms
8. Add multi-modal learning (text + voice patterns)

CURRENT: Simple feedforward network with basic text vectorization
FUTURE: Advanced transformer-based conversational AI
"""

# Singleton instance
neural_network = SimpleNeuralNetwork()