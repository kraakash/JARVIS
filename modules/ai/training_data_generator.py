"""
JARVIS Training Data Generator - Create Human-like Conversation Datasets
"""

import json
import random
from datetime import datetime

class TrainingDataGenerator:
    def __init__(self):
        self.conversation_patterns = {
            'contextual_responses': [
                {
                    'context': 'user_says_day_bad',
                    'user_inputs': ['aacha nhi ja rha hai', 'bad day', 'kharab din hai', 'not good'],
                    'responses': [
                        'Oh, kya hua Sir? Koi problem hai?',
                        'Sorry to hear that, Sir. What\'s troubling you?',
                        'Main kuch help kar sakta hun, Sir?'
                    ]
                },
                {
                    'context': 'user_explains_problem',
                    'user_inputs': ['work stress hai', 'boss problem', 'project difficult', 'kaam mushkil'],
                    'responses': [
                        'Work stress common hai, Sir. Break lena chahiye.',
                        'Sir, priorities set karne se help milegi.',
                        'One step at a time approach try kariye, Sir.'
                    ]
                },
                {
                    'context': 'user_shares_interest',
                    'user_inputs': ['i like music', 'mujhe cricket pasand', 'love reading', 'movies dekhta hun'],
                    'responses': [
                        'That\'s interesting, Sir! Tell me more about it.',
                        'Bahut achha, Sir! Kya favorite hai aapka?',
                        'I\'d love to learn more about your interests, Sir.'
                    ]
                }
            ],
            
            'follow_up_training': [
                {
                    'sequence': [
                        {'user': 'kaise ho', 'jarvis': 'Main theek hun, Sir. Aap kaise hain?'},
                        {'user': 'thoda tired hun', 'jarvis': 'Kya hua Sir? Kaam zyada hai?'},
                        {'user': 'haan project deadline hai', 'jarvis': 'Sir, break lena important hai. Kya main kuch suggest kar sakta hun?'}
                    ]
                },
                {
                    'sequence': [
                        {'user': 'what can you do', 'jarvis': 'I can help with many things, Sir. What do you need?'},
                        {'user': 'help with work', 'jarvis': 'What kind of work assistance do you need, Sir?'},
                        {'user': 'time management', 'jarvis': 'Great choice, Sir! Let\'s create a schedule together.'}
                    ]
                }
            ],
            
            'intelligent_responses': [
                {
                    'category': 'problem_solving',
                    'triggers': ['problem', 'issue', 'mushkil', 'difficulty'],
                    'responses': [
                        'Let\'s break this down step by step, Sir.',
                        'Sir, pehle main cause identify karte hain.',
                        'What\'s the root cause here, Sir?'
                    ]
                },
                {
                    'category': 'decision_making',
                    'triggers': ['decide', 'choose', 'faisla', 'select'],
                    'responses': [
                        'Sir, pros and cons list banate hain.',
                        'What factors are most important to you, Sir?',
                        'Let\'s analyze the options systematically, Sir.'
                    ]
                }
            ]
        }
    
    def generate_contextual_training_data(self):
        """Generate training data for contextual responses"""
        training_data = []
        
        for pattern in self.conversation_patterns['contextual_responses']:
            context = pattern['context']
            
            for user_input in pattern['user_inputs']:
                for response in pattern['responses']:
                    training_data.append({
                        'input': user_input,
                        'output': response,
                        'context': context,
                        'category': 'contextual_response'
                    })
        
        return training_data
    
    def generate_follow_up_training_data(self):
        """Generate training data for follow-up conversations"""
        training_data = []
        
        for sequence in self.conversation_patterns['follow_up_training']:
            for i, exchange in enumerate(sequence['sequence']):
                if i > 0:  # Skip first exchange, use previous as context
                    previous_context = sequence['sequence'][:i]
                    training_data.append({
                        'input': exchange['user'],
                        'output': exchange['jarvis'],
                        'context': previous_context,
                        'category': 'follow_up_response'
                    })
        
        return training_data
    
    def generate_intelligent_training_data(self):
        """Generate training data for intelligent responses"""
        training_data = []
        
        for pattern in self.conversation_patterns['intelligent_responses']:
            category = pattern['category']
            
            for trigger in pattern['triggers']:
                for response in pattern['responses']:
                    # Create variations with the trigger word
                    variations = [
                        f"I have a {trigger}",
                        f"There's a {trigger}",
                        f"Mujhe {trigger} hai",
                        f"Yeh {trigger} hai"
                    ]
                    
                    for variation in variations:
                        training_data.append({
                            'input': variation,
                            'output': response,
                            'category': category,
                            'trigger': trigger
                        })
        
        return training_data
    
    def create_conversation_dataset(self):
        """Create comprehensive conversation dataset"""
        print("🏗️  Building conversation dataset...")
        
        contextual = self.generate_contextual_training_data()
        followup = self.generate_follow_up_training_data()
        intelligent = self.generate_intelligent_training_data()
        
        dataset = {
            'contextual_responses': contextual,
            'follow_up_responses': followup,
            'intelligent_responses': intelligent,
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_samples': len(contextual) + len(followup) + len(intelligent)
            }
        }
        
        print(f"   ✅ Dataset created with {dataset['metadata']['total_samples']} samples")
        return dataset
    
    def save_training_dataset(self, filename='jarvis_conversation_training.json'):
        """Save training dataset to file with progress tracking"""
        print("\n🔄 Building JARVIS Conversation Model...")
        print("━" * 50)
        
        print("📊 Step 1: Generating contextual responses...")
        contextual_data = self.generate_contextual_training_data()
        print(f"   ✅ Generated {len(contextual_data)} contextual response patterns")
        
        print("🔗 Step 2: Creating follow-up conversation chains...")
        followup_data = self.generate_follow_up_training_data()
        print(f"   ✅ Generated {len(followup_data)} follow-up conversation sequences")
        
        print("🧠 Step 3: Building intelligent response patterns...")
        intelligent_data = self.generate_intelligent_training_data()
        print(f"   ✅ Generated {len(intelligent_data)} intelligent response variations")
        
        dataset = {
            'contextual_responses': contextual_data,
            'follow_up_responses': followup_data,
            'intelligent_responses': intelligent_data,
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_samples': len(contextual_data) + len(followup_data) + len(intelligent_data)
            }
        }
        
        try:
            print("💾 Step 4: Saving training dataset...")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            
            print(f"   ✅ Training dataset saved successfully!")
            print(f"\n📈 Model Statistics:")
            print(f"   • Total Training Samples: {dataset['metadata']['total_samples']}")
            print(f"   • Contextual Patterns: {len(contextual_data)}")
            print(f"   • Follow-up Chains: {len(followup_data)}")
            print(f"   • Intelligent Responses: {len(intelligent_data)}")
            print(f"   • Dataset File: {filename}")
            
            return dataset
        except Exception as e:
            print(f"   ❌ ERROR: Could not save training dataset: {e}")
            return None
    
    def add_user_conversation(self, user_input, jarvis_response, context=None):
        """Add real user conversation to training data with progress tracking"""
        training_file = 'user_conversations.json'
        
        conversation_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'jarvis_response': jarvis_response,
            'context': context
        }
        
        try:
            # Load existing conversations
            conversations = []
            try:
                with open(training_file, 'r', encoding='utf-8') as f:
                    conversations = json.load(f)
            except FileNotFoundError:
                pass
            
            # Add new conversation
            conversations.append(conversation_entry)
            conversation_count = len(conversations)
            
            # Save updated conversations
            with open(training_file, 'w', encoding='utf-8') as f:
                json.dump(conversations, f, indent=2, ensure_ascii=False)
            
            # Print learning progress
            if conversation_count % 5 == 0:  # Every 5 conversations
                print(f"\n🎯 Learning Progress: {conversation_count} conversations learned!")
                print(f"   📝 Latest: '{user_input[:30]}...' → '{jarvis_response[:30]}...'")
            
            return True
        except Exception as e:
            print(f"❌ ERROR: Could not save user conversation: {e}")
            return False
    
    def train_tensorflow_model(self, dataset):
        """Train TensorFlow model with conversation data"""
        print("\n🤖 Step 5: Training TensorFlow Neural Network...")
        
        try:
            from .tensorflow_model import tensorflow_jarvis
            
            if not tensorflow_jarvis.available:
                print("   ⚠️  TensorFlow not available, skipping neural network training")
                return False
            
            # Prepare training data
            training_inputs = []
            training_labels = []
            
            for category in ['contextual_responses', 'follow_up_responses', 'intelligent_responses']:
                for item in dataset[category]:
                    training_inputs.append(item['input'])
                    training_labels.append(item['category'])
            
            print(f"   📚 Preparing {len(training_inputs)} training samples...")
            
            # Train the model
            success = tensorflow_jarvis.train_model(training_inputs, training_labels, epochs=10)
            
            if success:
                print("   ✅ Neural network training completed!")
                tensorflow_jarvis.save_model()
                print("   💾 Model saved successfully!")
                return True
            else:
                print("   ❌ Neural network training failed")
                return False
                
        except Exception as e:
            print(f"   ❌ ERROR during neural network training: {e}")
            return False

    def get_model_stats(self):
        """Get comprehensive model statistics"""
        stats = {
            'training_dataset': 'Not found',
            'user_conversations': 0,
            'tensorflow_model': 'Not available',
            'conversation_context': 'Not loaded'
        }
        
        # Check training dataset
        try:
            with open('jarvis_conversation_training.json', 'r') as f:
                dataset = json.load(f)
                stats['training_dataset'] = f"{dataset['metadata']['total_samples']} samples"
        except:
            pass
        
        # Check user conversations
        try:
            with open('user_conversations.json', 'r') as f:
                conversations = json.load(f)
                stats['user_conversations'] = len(conversations)
        except:
            pass
        
        # Check TensorFlow model
        try:
            from .tensorflow_model import tensorflow_jarvis
            if tensorflow_jarvis.available:
                stats['tensorflow_model'] = 'Available and trained'
        except:
            pass
        
        # Check conversation context
        try:
            from .conversation_context import conversation_context
            if len(conversation_context.conversation_history) > 0:
                stats['conversation_context'] = f"{len(conversation_context.conversation_history)} exchanges"
        except:
            pass
        
        return stats

# Singleton instance
training_generator = TrainingDataGenerator()