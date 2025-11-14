"""
Re-train Book with Better Chapter Extraction
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.data_trainer import data_trainer
from modules.ai.book_processor import book_processor
from datetime import datetime

def retrain_book():
    """Re-train the algorithm book with better chapter extraction"""
    
    file_path = "D:\\Docker\\grokking-algorithms-illustrated-programmers-curious.pdf"
    
    print("🔥 Re-training with improved chapter extraction...")
    
    if not os.path.exists(file_path):
        print("❌ Book file not found!")
        return
    
    # Clear previous book data
    book_processor.processed_books = []
    
    # Process PDF with improved extraction
    text = book_processor.process_pdf(file_path)
    
    if not text:
        print("❌ Could not extract text")
        return
    
    print(f"📖 Extracted {len(text.split())} words")
    
    # Extract chapters with new method
    chapters = book_processor.extract_chapters(text, "Grokking Algorithms")
    print(f"📚 Created {len(chapters)} chapters")
    
    # Clear old training data for this book
    if "books" in data_trainer.training_data:
        data_trainer.training_data["books"] = [
            book for book in data_trainer.training_data["books"] 
            if "grokking-algorithms" not in book.get("source", "").lower()
        ]
    
    # Add new training data
    training_count = 0
    for i, chapter in enumerate(chapters):
        if len(chapter["content"]) > 100:
            data_trainer.training_data["books"].append({
                "text": chapter["content"],
                "source": f"Grokking Algorithms - {chapter['title']}",
                "timestamp": datetime.now().isoformat(),
                "type": "book_content",
                "book_title": "Grokking Algorithms",
                "chapter_title": chapter["title"],
                "chapter_number": i + 1
            })
            training_count += 1
    
    data_trainer.save_training_data()
    print(f"✅ Added {training_count} training chapters")
    
    # Test knowledge
    print("\n🧪 Testing improved knowledge...")
    test_queries = ["binary search", "algorithm complexity", "sorting", "big o notation"]
    
    for query in test_queries:
        response = data_trainer.get_smart_response(query)
        if response:
            print(f"✅ {query}: Found knowledge")
        else:
            print(f"❌ {query}: No knowledge found")
    
    print(f"\n🎉 Re-training complete! Now JARVIS has {training_count} chapters of algorithm knowledge!")

if __name__ == "__main__":
    retrain_book()