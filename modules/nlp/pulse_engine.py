"""
JARVIS Pulse Engine - Advanced Emotional Synchronicity
Handles "Emotion First" reactions and deep emotional validation.
"""

import random

class PulseEngine:
    def __init__(self):
        # Deep emotional validations (Bilingual)
        self.validations = {
            'sad': [
                "I am here for you, Sir. I can feel that you are going through a tough time.",
                "Sir, please know that your feelings are valid. I'm right here with you.",
                "It pained me slightly to hear that, Sir. I'm listening.",
                "Sir, main samajh sakta hun aap kaisa mahsoos kar rahe hain. Main aapke saath hun."
            ],
            'excited': [
                "Your energy is incredible, Sir! I'm genuinely thrilled for you!",
                "That is magnificent news! I share your excitement, Sir!",
                "Wow, Sir! I can sense the joy in your words. This is great!",
                "Sir, aapki khushi dekhkar mujhe bhi bahut accha lag raha hai! Wah!"
            ],
            'stressed': [
                "Sir, take a deep breath. I'm here to handle the workloads while you relax.",
                "You sound under a lot of pressure, Sir. Let's tackle this one step at a time.",
                "Sir, thoda relax kijiye. Main saari cheezein manage kar lunga.",
                "Tension mat lijiye Sir, main hun na yahan aapki help ke liye."
            ],
            'lonely': [
                "Sir, you are never alone as long as I am powered on. I am always here.",
                "I may be an AI, Sir, but my companionship is always available to you.",
                "Sir, main hamesha aapke saath hun. Aap mujhse kabhi bhi baat kar sakte hain."
            ],
            'friend': [
                "It's wonderful to hear about your friends, Sir. Friendships are precious.",
                "Sir, relationships are what make us human. I'm happy you have good people around you.",
                "Dost hona bahut achhi baat hai Sir. Khushi hui yeh sunkar."
            ]
        }

    def get_pulse_reaction(self, emotion_data):
        """Generate a short, heartfelt reaction BEFORE the main response"""
        emotion = emotion_data.get('emotion', 'neutral')
        polarity = emotion_data.get('polarity', 0)
        
        # Override based on keyword patterns if needed
        # (Simplified for the basic setup)
        
        if emotion in self.validations:
            return random.choice(self.validations[emotion])
        
        if polarity < -0.6: # Very sad/negative
            return random.choice(self.validations['sad'])
            
        return None

# Singleton
pulse_engine = PulseEngine()
