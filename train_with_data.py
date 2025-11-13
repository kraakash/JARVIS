"""
Main Training Script for JARVIS
Train JARVIS with books, real-time data, and web content
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ai.data_trainer import data_trainer
from modules.ai.book_processor import book_processor
import json
from datetime import datetime

def train_with_books(books_folder="d:/Code/Books"):
    """Train JARVIS with books from folder"""
    print("🔥 Starting Book Training...")
    
    if not os.path.exists(books_folder):
        print(f"Books folder not found: {books_folder}")
        print("Please create folder and add PDF/TXT/EPUB/DOCX files")
        return
    
    # Process all books
    processed_count = book_processor.process_book_folder(books_folder)
    print(f"📚 Processed {processed_count} books")
    
    # Save processed books
    book_processor.save_processed_books()
    
    # Convert to training data
    training_count = 0
    for book in book_processor.processed_books:
        for chapter in book["chapters"]:
            if len(chapter["content"]) > 100:
                data_trainer.training_data["books"].append({
                    "text": chapter["content"],
                    "source": f"{book['title']} - {chapter['title']}",
                    "timestamp": datetime.now().isoformat(),
                    "type": "book_content",
                    "book_title": book["title"],
                    "chapter_title": chapter["title"]
                })
                training_count += 1
    
    data_trainer.save_training_data()
    print(f"📖 Added {training_count} training samples from books")

def train_with_real_time_data():
    """Train with real-time news and Wikipedia"""
    print("🌐 Starting Real-time Data Training...")
    
    # Fetch latest news
    news_count = data_trainer.fetch_real_time_news()
    print(f"📰 Fetched {news_count} news articles")
    
    # Fetch Wikipedia data for common topics
    topics = [
        "Artificial Intelligence", "Machine Learning", "Python Programming",
        "Technology", "Science", "History", "Geography", "Mathematics",
        "Physics", "Chemistry", "Biology", "Computer Science",
        "India", "World News", "Space", "Environment"
    ]
    
    wiki_count = data_trainer.fetch_wikipedia_data(topics)
    print(f"📖 Fetched {wiki_count} Wikipedia articles")

def build_knowledge_system():
    """Build comprehensive knowledge system"""
    print("🧠 Building Knowledge System...")
    
    # Build knowledge graph
    data_trainer.build_knowledge_graph()
    
    # Get training stats
    stats = data_trainer.get_training_stats()
    
    print("📊 Training Statistics:")
    print(f"   Books: {stats['total_books']}")
    print(f"   News: {stats['total_news']}")
    print(f"   Wikipedia: {stats['total_wikipedia']}")
    print(f"   Conversations: {stats['total_conversations']}")
    print(f"   Knowledge Entities: {stats['total_entities']}")
    print(f"   Last Updated: {stats['last_updated']}")

def start_continuous_learning():
    """Start continuous learning system"""
    print("🚀 Starting Continuous Learning...")
    
    # Start real-time training
    data_trainer.start_real_time_training()
    
    print("✅ Continuous learning started!")
    print("JARVIS will now automatically:")
    print("   - Fetch latest news every 30 minutes")
    print("   - Update knowledge graph every hour")
    print("   - Learn from every conversation")

def test_trained_knowledge():
    """Test the trained knowledge"""
    print("🧪 Testing Trained Knowledge...")
    
    test_queries = [
        "What is artificial intelligence?",
        "Tell me about Python programming",
        "Latest news about technology",
        "What is machine learning?",
        "Tell me about India"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = data_trainer.get_smart_response(query)
        if response:
            print(f"Response: {response}")
        else:
            print("No specific knowledge found")

def main():
    """Main training function"""
    print("🤖 JARVIS Advanced Training System")
    print("=" * 50)
    
    while True:
        print("\nTraining Options:")
        print("1. Train with Books (PDF/TXT/EPUB/DOCX)")
        print("2. Train with Real-time Data (News + Wikipedia)")
        print("3. Build Knowledge System")
        print("4. Start Continuous Learning")
        print("5. Test Trained Knowledge")
        print("6. View Training Statistics")
        print("7. Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == "1":
            books_folder = input("Enter books folder path (default: d:/Code/Books): ").strip()
            if not books_folder:
                books_folder = "d:/Code/Books"
            train_with_books(books_folder)
            
        elif choice == "2":
            train_with_real_time_data()
            
        elif choice == "3":
            build_knowledge_system()
            
        elif choice == "4":
            start_continuous_learning()
            
        elif choice == "5":
            test_trained_knowledge()
            
        elif choice == "6":
            stats = data_trainer.get_training_stats()
            print("\n📊 Current Training Statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
                
        elif choice == "7":
            print("Training completed! 🎉")
            break
            
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()