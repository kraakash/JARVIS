"""
Simple AI Fallback - No External Dependencies
"""

import random

class SimpleAI:
    def __init__(self):
        self.responses = {
            "question": [
                "Kya code mein koi problem aa rahi hai?",
                "Kya research mein help chahiye?",
                "Main kya madad kar sakta hun?",
                "Koi specific help chahiye?"
            ],
            "help": [
                "Haan Sir, main help kar sakta hun.",
                "Batayiye kya chahiye?",
                "Kya problem hai, Sir?",
                "Main taiyar hun help karne ke liye."
            ],
            "error": [
                "Koi baat nahi, Sir. Main samjh gaya.",
                "Local system se kaam chal jayega.",
                "API problem hai, lekin main hun na.",
                "Tension mat lo, Sir. Main handle kar lunga."
            ]
        }
    
    def get_response(self, user_input: str, context: str = "") -> str:
        """Get simple response"""
        user_lower = user_input.lower()
        
        if "question" in user_lower or "pucho" in user_lower:
            return random.choice(self.responses["question"])
        elif "help" in user_lower or "madad" in user_lower:
            return random.choice(self.responses["help"])
        elif "error" in user_lower or "problem" in user_lower:
            return random.choice(self.responses["error"])
        else:
            return "Samjha nahi, Sir. Phir se boliye."
    
    def handle_api_error(self, error_msg: str) -> str:
        """Handle API errors"""
        return random.choice(self.responses["error"])

# Global instance
simple_ai = SimpleAI()
