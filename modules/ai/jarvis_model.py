"""
JARVIS Personal AI Model - Train from Groq responses
Custom transformer model that learns JARVIS conversation style
"""

import json
import os
import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import Trainer, TrainingArguments
from torch.utils.data import Dataset
import numpy as np
from datetime import datetime

class JarvisDataset(Dataset):
    def __init__(self, conversations, tokenizer, max_length=512):
        self.conversations = conversations
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.conversations)
    
    def __getitem__(self, idx):
        conv = self.conversations[idx]
        
        # Format: "User: {question} JARVIS: {response}"
        text = f"User: {conv['question']} JARVIS: {conv['response']}"
        
        # Tokenize
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': encoding['input_ids'].flatten()
        }

class JarvisModel:
    def __init__(self):
        self.model_path = "jarvis_model"
        self.data_file = "jarvis_training_data.json"
        self.tokenizer = None
        self.model = None
        self.training_data = []
        
        # Load training data first
        self.load_training_data()
        # Then setup model based on available data
        self.setup_model()
    
    def setup_model(self):
        """Initialize or load model"""
        # Check if model directory exists and has required files
        model_exists = (os.path.exists(self.model_path) and 
                       os.path.exists(os.path.join(self.model_path, 'config.json')))
        
        if model_exists:
            try:
                # Try to load existing model
                self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
                self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
                print("[JARVIS] Loaded existing model")
                return
            except Exception as e:
                print(f"[JARVIS] Failed to load existing model: {e}")
        
        # Only create new model if we have training data
        if len(self.training_data) < 5:
            print("[JARVIS] Skipping model creation - insufficient training data")
            self.model = None
            self.tokenizer = None
            return
        
        try:
            # Create new model only when needed
            print("[JARVIS] Creating new model...")
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            config = GPT2Config(
                vocab_size=self.tokenizer.vocab_size,
                n_positions=512,
                n_ctx=512,
                n_embd=768,
                n_layer=12,
                n_head=12
            )
            
            self.model = GPT2LMHeadModel(config)
            
            # Save immediately to prevent recreation
            os.makedirs(self.model_path, exist_ok=True)
            self.model.save_pretrained(self.model_path)
            self.tokenizer.save_pretrained(self.model_path)
            
            print("[JARVIS] Created and saved new model successfully")
        except Exception as setup_error:
            print(f"[JARVIS] Model setup failed: {setup_error}")
            self.model = None
            self.tokenizer = None
    
    def load_training_data(self):
        """Load existing training data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.training_data = json.load(f)
                print(f"[JARVIS] Loaded {len(self.training_data)} training samples")
            else:
                self.training_data = []
            
            # Load pre-trained personal conversation data
            pretrained_file = "personal_conversation_training.json"
            if os.path.exists(pretrained_file):
                with open(pretrained_file, 'r', encoding='utf-8') as f:
                    pretrained_data = json.load(f)
                
                # Add pretrained data if not already present
                for item in pretrained_data:
                    exists = any(existing['question'].lower() == item['question'].lower() 
                               for existing in self.training_data)
                    if not exists:
                        self.training_data.append(item)
                
                print(f"[JARVIS] Added {len(pretrained_data)} pre-trained personal conversations")
                self.save_training_data()
                
        except Exception as e:
            print(f"[JARVIS] Error loading data: {e}")
            self.training_data = []
    
    def is_personal_conversation(self, question, response):
        """Check if this is a personal/emotional conversation worth training on"""
        personal_keywords = [
            'kaise ho', 'how are you', 'mood', 'feel', 'emotion', 'love', 'pyaar',
            'dost', 'friend', 'achha', 'bura', 'khush', 'sad', 'happy', 'angry',
            'flirt', 'cute', 'beautiful', 'handsome', 'sweet', 'romantic',
            'thank you', 'dhanyawad', 'sorry', 'maaf', 'compliment', 'tareef',
            'joke', 'mazak', 'funny', 'hasna', 'smile', 'muskurana',
            'miss', 'yaad', 'care', 'fikar', 'worry', 'tension'
        ]
        
        # Skip technical/news/app control conversations
        skip_keywords = [
            'open', 'close', 'search', 'youtube', 'chrome', 'calculator',
            'election', 'news', 'result', 'algorithm', 'code', 'programming',
            'sort', 'merge', 'selection', 'binary', 'function', 'variable'
        ]
        
        question_lower = question.lower()
        response_lower = response.lower()
        
        # Skip if contains technical keywords
        if any(keyword in question_lower for keyword in skip_keywords):
            return False
        
        # Include if contains personal keywords
        if any(keyword in question_lower or keyword in response_lower for keyword in personal_keywords):
            return True
        
        # Include short conversational exchanges
        if len(question.split()) <= 5 and len(response.split()) <= 20:
            return True
        
        return False
    
    def detect_emotion(self, question, response):
        """Detect emotion in conversation"""
        positive_words = ['happy', 'khush', 'achha', 'good', 'great', 'awesome', 'love', 'pyaar']
        negative_words = ['sad', 'bura', 'bad', 'angry', 'gussa', 'upset', 'tension']
        flirty_words = ['cute', 'beautiful', 'handsome', 'sweet', 'romantic', 'miss', 'yaad']
        
        text = (question + ' ' + response).lower()
        
        if any(word in text for word in flirty_words):
            return 'flirty'
        elif any(word in text for word in positive_words):
            return 'positive'
        elif any(word in text for word in negative_words):
            return 'negative'
        else:
            return 'neutral'
    
    def add_conversation(self, question, response):
        """Add new conversation to training data (only personal conversations)"""
        # Only train on personal/emotional conversations
        if not self.is_personal_conversation(question, response):
            return
        
        conversation = {
            'question': question.strip(),
            'response': response.strip(),
            'timestamp': datetime.now().isoformat(),
            'source': 'personal',
            'emotion': self.detect_emotion(question, response)
        }
        
        # Store multiple responses for same question
        existing_found = False
        for existing in self.training_data:
            if existing['question'].lower() == question.lower():
                # Create variants list if not exists
                if 'variants' not in existing:
                    existing['variants'] = [existing['response']]
                
                # Add new response as variant if different
                if response not in existing['variants']:
                    existing['variants'].append(response)
                    existing['timestamp'] = conversation['timestamp']
                    print(f"[JARVIS] Added response variant: {question[:30]}...")
                existing_found = True
                break
        
        if not existing_found:
            self.training_data.append(conversation)
            print(f"[JARVIS] Added personal conversation: {question[:30]}...")
        
        self.save_training_data()
        
        # Auto-train if we have enough personal data
        if len(self.training_data) % 5 == 0:
            self.train_model()
    
    def save_training_data(self):
        """Save training data to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.training_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[JARVIS] Error saving data: {e}")
    
    def train_model(self):
        """Train the model with current data"""
        if len(self.training_data) < 5:
            print("[JARVIS] Not enough data to train")
            return
        
        try:
            print(f"[JARVIS] Training model with {len(self.training_data)} samples...")
            
            # Create dataset
            dataset = JarvisDataset(self.training_data, self.tokenizer)
            
            # Training arguments
            training_args = TrainingArguments(
                output_dir='./jarvis_training',
                overwrite_output_dir=True,
                num_train_epochs=3,
                per_device_train_batch_size=2,
                save_steps=50,
                save_total_limit=2,
                logging_steps=10,
                learning_rate=5e-5,
                warmup_steps=10,
                logging_dir='./logs',
                no_cuda=True  # Use CPU only
            )
            
            # Create trainer
            trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=dataset,
                tokenizer=self.tokenizer
            )
            
            # Train
            trainer.train()
            
            # Save model
            self.model.save_pretrained(self.model_path)
            self.tokenizer.save_pretrained(self.model_path)
            
            print("[JARVIS] Model training completed!")
            
        except Exception as e:
            print(f"[JARVIS] Training error: {e}")
    
    def generate_response(self, question):
        """Generate response using trained model"""
        try:
            if not self.model:
                return None
            
            # Format input
            input_text = f"User: {question} JARVIS:"
            
            # Tokenize
            inputs = self.tokenizer.encode(input_text, return_tensors='pt')
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.8,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract JARVIS response
            if "JARVIS:" in response:
                jarvis_response = response.split("JARVIS:")[-1].strip()
                if jarvis_response and len(jarvis_response) > 10:
                    return jarvis_response
            
        except Exception as e:
            print(f"[JARVIS] Generation error: {e}")
        
        return None
    
    def is_available(self):
        """Check if model is available"""
        return self.model is not None and self.tokenizer is not None
    
    def get_model_stats(self):
        """Get model statistics"""
        last_training = "Never"
        if self.training_data:
            # Find the most recent entry with timestamp
            for conv in reversed(self.training_data):
                if 'timestamp' in conv:
                    last_training = conv['timestamp']
                    break
        
        return {
            'total_conversations': len(self.training_data),
            'model_size': f"{sum(p.numel() for p in self.model.parameters()) / 1e6:.1f}M parameters" if self.model else "Not loaded",
            'last_training': last_training,
            'data_sources': list(set([conv.get('source', 'unknown') for conv in self.training_data]))
        }

# Global instance
try:
    jarvis_model = JarvisModel()
    print("[JARVIS] Model initialized successfully")
except Exception as e:
    print(f"[JARVIS] Model initialization failed: {e}")
    jarvis_model = None