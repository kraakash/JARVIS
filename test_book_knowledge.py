"""
Test JARVIS Book Knowledge
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.data_trainer import data_trainer
from modules.ai.book_processor import book_processor

def test_jarvis_knowledge():
    """Test what JARVIS learned from books"""
    print("🧠 Testing JARVIS Book Knowledge...")
    
    # Algorithm book related questions
    test_questions = [
        "What is an algorithm?",
        "Tell me about binary search",
        "What is Big O notation?", 
        "Explain sorting algorithms",
        "What is recursion?",
        "Tell me about data structures",
        "What is a graph?",
        "Explain breadth first search",
        "What is dynamic programming?",
        "Tell me about arrays"
    ]
    
    print("\n📚 Book Knowledge Test Results:")
    print("=" * 50)
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        
        # Get response from trained data
        response = data_trainer.get_smart_response(question)
        
        if response:
            print(f"🤖 JARVIS: {response}")
        else:
            print("🤖 JARVIS: Sir, I don't have specific knowledge about this topic yet.")
        
        print("-" * 30)
    
    # Show training stats
    stats = data_trainer.get_training_stats()
    print(f"\n📊 Training Statistics:")
    print(f"Books Processed: {stats['total_books']}")
    print(f"Knowledge Entities: {stats['total_entities']}")
    print(f"Total Conversations: {stats['total_conversations']}")

if __name__ == "__main__":
    test_jarvis_knowledge()