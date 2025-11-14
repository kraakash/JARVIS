"""
Generate Clean Responses from All Books
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.data_trainer import data_trainer
from modules.ai.book_response_generator import book_response_generator

def generate_all_clean_responses():
    """Generate clean responses from all trained books"""
    
    print("🧠 Generating Clean Responses from Books...")
    
    # Load training data
    training_data = data_trainer.training_data
    
    if not training_data.get("books"):
        print("❌ No book training data found!")
        print("First run: python train_single_book.py")
        return
    
    print(f"📚 Found {len(training_data['books'])} book entries")
    
    # Generate clean responses
    generated_count = book_response_generator.generate_responses_from_book(training_data)
    
    print(f"✅ Generated {generated_count} clean responses")
    
    # Show statistics
    stats = book_response_generator.get_stats()
    print(f"\n📊 Response Statistics:")
    print(f"   Total Responses: {stats['total_responses']}")
    print(f"   Unique Keywords: {stats['unique_keywords']}")
    print(f"   Books Processed: {len(stats['sources'])}")
    
    # Test some responses
    print(f"\n🧪 Testing Generated Responses:")
    test_questions = [
        "what is algorithm",
        "binary search kya hai", 
        "tell me about sorting",
        "recursion samjhao"
    ]
    
    for question in test_questions:
        response = book_response_generator.get_clean_response(question)
        if response:
            print(f"✅ {question}: {response[:60]}...")
        else:
            print(f"❌ {question}: No response found")
    
    print(f"\n🎉 Clean responses generated! JARVIS will now give structured answers.")

if __name__ == "__main__":
    generate_all_clean_responses()