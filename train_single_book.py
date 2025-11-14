"""
Train JARVIS with Single Book
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.data_trainer import data_trainer
from modules.ai.book_processor import book_processor
from datetime import datetime

def train_single_book(file_path):
    """Train with a single book file"""
    print(f"🔥 Training with: {os.path.basename(file_path)}")
    
    if not os.path.exists(file_path):
        print("❌ File not found!")
        return
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    # Process based on file type
    if file_ext == '.pdf':
        text = book_processor.process_pdf(file_path)
    elif file_ext == '.txt':
        text = book_processor.process_txt(file_path)
    elif file_ext == '.epub':
        text = book_processor.process_epub(file_path)
    elif file_ext == '.docx':
        text = book_processor.process_docx(file_path)
    else:
        print(f"❌ Unsupported format: {file_ext}")
        return
    
    if not text:
        print("❌ Could not extract text from file")
        return
    
    print(f"📖 Extracted {len(text.split())} words")
    
    # Extract chapters
    chapters = book_processor.extract_chapters(text, os.path.basename(file_path))
    print(f"📚 Found {len(chapters)} chapters")
    
    # Add to training data
    training_count = 0
    for chapter in chapters:
        if len(chapter["content"]) > 100:
            data_trainer.training_data["books"].append({
                "text": chapter["content"],
                "source": f"{os.path.basename(file_path)} - {chapter['title']}",
                "timestamp": datetime.now().isoformat(),
                "type": "book_content",
                "book_title": os.path.basename(file_path),
                "chapter_title": chapter["title"]
            })
            training_count += 1
    
    data_trainer.save_training_data()
    print(f"✅ Added {training_count} training samples")
    
    # Test knowledge
    print("\n🧪 Testing book knowledge...")
    test_queries = ["algorithm", "programming", "data structure"]
    
    for query in test_queries:
        response = data_trainer.get_smart_response(query)
        if response:
            print(f"Query '{query}': {response[:100]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter book file path: ").strip().strip('"')
    
    train_single_book(file_path)