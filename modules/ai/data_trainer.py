"""
Advanced Data Training System for JARVIS
Trains JARVIS with books, real-time data, and web content like ChatGPT
"""

import json
import requests
import feedparser
import wikipedia
import os
from datetime import datetime
import threading
import time
from textblob import TextBlob
import re

class DataTrainer:
    def __init__(self):
        self.training_data_file = "d:/Code/Jarvis/training_data.json"
        self.knowledge_base_file = "d:/Code/Jarvis/knowledge_base.json"
        self.real_time_sources = [
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://rss.cnn.com/rss/edition.rss",
            "https://feeds.reuters.com/reuters/topNews"
        ]
        self.training_data = self.load_training_data()
        self.knowledge_base = self.load_knowledge_base()
        
    def load_training_data(self):
        """Load existing training data"""
        try:
            with open(self.training_data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure all required keys exist
                required_keys = ["conversations", "facts", "books", "news", "wikipedia"]
                for key in required_keys:
                    if key not in data:
                        data[key] = []
                return data
        except:
            return {
                "conversations": [],
                "facts": [],
                "books": [],
                "news": [],
                "wikipedia": [],
                "last_updated": datetime.now().isoformat()
            }
    
    def load_knowledge_base(self):
        """Load knowledge base"""
        try:
            with open(self.knowledge_base_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure all required keys exist
                required_keys = ["topics", "entities", "relationships", "confidence_scores"]
                for key in required_keys:
                    if key not in data:
                        data[key] = {}
                return data
        except:
            return {
                "topics": {},
                "entities": {},
                "relationships": {},
                "confidence_scores": {}
            }
    
    def save_training_data(self):
        """Save training data to file"""
        self.training_data["last_updated"] = datetime.now().isoformat()
        with open(self.training_data_file, 'w', encoding='utf-8') as f:
            json.dump(self.training_data, f, indent=2, ensure_ascii=False)
    
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        with open(self.knowledge_base_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)
    
    def train_from_text_file(self, file_path):
        """Train from text files (books, documents)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process content into training data
            sentences = self.extract_sentences(content)
            
            for sentence in sentences:
                if len(sentence.strip()) > 20:  # Only meaningful sentences
                    self.training_data["books"].append({
                        "text": sentence.strip(),
                        "source": os.path.basename(file_path),
                        "timestamp": datetime.now().isoformat(),
                        "type": "book_content"
                    })
            
            self.save_training_data()
            return len(sentences)
            
        except Exception as e:
            print(f"Error training from file: {e}")
            return 0
    
    def extract_sentences(self, text):
        """Extract meaningful sentences from text"""
        # Clean text
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Filter meaningful sentences
        meaningful_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (len(sentence) > 20 and 
                len(sentence) < 500 and 
                ' ' in sentence and
                not sentence.isupper()):
                meaningful_sentences.append(sentence)
        
        return meaningful_sentences
    
    def fetch_real_time_news(self):
        """Fetch real-time news data"""
        news_count = 0
        
        for source_url in self.real_time_sources:
            try:
                feed = feedparser.parse(source_url)
                
                for entry in feed.entries[:10]:  # Latest 10 articles
                    news_data = {
                        "title": entry.title,
                        "summary": entry.get('summary', ''),
                        "link": entry.link,
                        "published": entry.get('published', ''),
                        "source": source_url,
                        "timestamp": datetime.now().isoformat(),
                        "type": "real_time_news"
                    }
                    
                    self.training_data["news"].append(news_data)
                    news_count += 1
                    
            except Exception as e:
                print(f"Error fetching from {source_url}: {e}")
        
        # Ensure news key exists and keep only latest 1000 news items
        if "news" not in self.training_data:
            self.training_data["news"] = []
        if len(self.training_data["news"]) > 1000:
            self.training_data["news"] = self.training_data["news"][-1000:]
        
        self.save_training_data()
        return news_count
    
    def fetch_wikipedia_data(self, topics):
        """Fetch Wikipedia data for specific topics"""
        wiki_count = 0
        
        for topic in topics:
            try:
                # Search for the topic
                search_results = wikipedia.search(topic, results=3)
                
                for result in search_results:
                    try:
                        page = wikipedia.page(result)
                        
                        wiki_data = {
                            "title": page.title,
                            "summary": page.summary[:1000],  # First 1000 chars
                            "content": page.content[:5000],   # First 5000 chars
                            "url": page.url,
                            "topic": topic,
                            "timestamp": datetime.now().isoformat(),
                            "type": "wikipedia_content"
                        }
                        
                        self.training_data["wikipedia"].append(wiki_data)
                        wiki_count += 1
                        
                    except wikipedia.exceptions.DisambiguationError as e:
                        # Take first option from disambiguation
                        try:
                            page = wikipedia.page(e.options[0])
                            wiki_data = {
                                "title": page.title,
                                "summary": page.summary[:1000],
                                "content": page.content[:5000],
                                "url": page.url,
                                "topic": topic,
                                "timestamp": datetime.now().isoformat(),
                                "type": "wikipedia_content"
                            }
                            self.training_data["wikipedia"].append(wiki_data)
                            wiki_count += 1
                        except:
                            continue
                    except:
                        continue
                        
            except Exception as e:
                print(f"Error fetching Wikipedia data for {topic}: {e}")
        
        self.save_training_data()
        return wiki_count
    
    def process_conversation_for_training(self, user_input, jarvis_response):
        """Process user conversations for training"""
        try:
            sentiment = str(TextBlob(user_input).sentiment)
        except:
            sentiment = "neutral"
        
        conversation_data = {
            "user_input": user_input,
            "jarvis_response": jarvis_response,
            "timestamp": datetime.now().isoformat(),
            "sentiment": sentiment,
            "type": "conversation"
        }
        
        self.training_data["conversations"].append(conversation_data)
        
        # Ensure conversations key exists and keep only latest 5000 conversations
        if "conversations" not in self.training_data:
            self.training_data["conversations"] = []
        if len(self.training_data["conversations"]) > 5000:
            self.training_data["conversations"] = self.training_data["conversations"][-5000:]
        
        self.save_training_data()
    
    def extract_knowledge_entities(self, text):
        """Extract knowledge entities from text"""
        try:
            blob = TextBlob(text)
            
            # Extract noun phrases as potential entities
            entities = []
            for phrase in blob.noun_phrases:
                if len(phrase) > 3 and len(phrase) < 50:
                    entities.append(phrase.lower())
            
            return entities
        except Exception as e:
            print(f"TextBlob error: {e}")
            # Fallback: simple word extraction
            import re
            words = re.findall(r'\b[A-Za-z]{4,}\b', text)
            return [word.lower() for word in words[:10]]  # Return first 10 words
    
    def build_knowledge_graph(self):
        """Build knowledge graph from training data"""
        print("Building knowledge graph...")
        
        # Process all training data
        all_texts = []
        
        # Add book content
        for book in self.training_data.get("books", []):
            all_texts.append(book["text"])
        
        # Add news content
        for news in self.training_data.get("news", []):
            all_texts.append(news["title"] + " " + news.get("summary", ""))
        
        # Add Wikipedia content
        for wiki in self.training_data.get("wikipedia", []):
            all_texts.append(wiki["summary"])
        
        # Extract entities and build relationships
        for text in all_texts:
            entities = self.extract_knowledge_entities(text)
            
            for entity in entities:
                if entity not in self.knowledge_base["entities"]:
                    self.knowledge_base["entities"][entity] = {
                        "frequency": 0,
                        "contexts": [],
                        "related_entities": []
                    }
                
                self.knowledge_base["entities"][entity]["frequency"] += 1
                
                # Add context
                if len(self.knowledge_base["entities"][entity]["contexts"]) < 10:
                    self.knowledge_base["entities"][entity]["contexts"].append(text[:200])
        
        self.save_knowledge_base()
        print(f"Knowledge graph built with {len(self.knowledge_base['entities'])} entities")
    
    def get_smart_response(self, user_input):
        """Get smart response based on training data"""
        user_lower = user_input.lower()
        
        # Search in book training data first
        if "books" in self.training_data:
            for book_entry in self.training_data["books"]:
                book_text = book_entry.get("text", "").lower()
                
                # Check for algorithm-related keywords
                algorithm_keywords = ["algorithm", "binary search", "sorting", "big o", "recursion", "data structure"]
                
                for keyword in algorithm_keywords:
                    if keyword in user_lower and keyword in book_text:
                        # Extract relevant portion
                        start_idx = book_text.find(keyword)
                        if start_idx != -1:
                            # Get context around the keyword
                            context_start = max(0, start_idx - 100)
                            context_end = min(len(book_text), start_idx + 300)
                            context = book_entry["text"][context_start:context_end]
                            
                            return f"Sir, from {book_entry.get('source', 'book')}: {context.strip()}..."
        
        # Search in knowledge base entities
        if "entities" in self.knowledge_base:
            relevant_entities = []
            for entity, data in self.knowledge_base["entities"].items():
                if entity in user_lower:
                    relevant_entities.append((entity, data))
            
            if relevant_entities:
                # Sort by frequency
                relevant_entities.sort(key=lambda x: x[1]["frequency"], reverse=True)
                top_entity = relevant_entities[0]
                
                contexts = top_entity[1].get("contexts", [])
                if contexts:
                    return f"Sir, {top_entity[0]} ke baare mein: {contexts[0][:150]}..."
        
        # Search in recent news
        for news in self.training_data.get("news", [])[-50:]:  # Latest 50 news
            if any(word in news["title"].lower() for word in user_lower.split()):
                return f"Sir, latest news: {news['title']} - {news.get('summary', '')[:100]}..."
        
        return None
    
    def start_real_time_training(self):
        """Start continuous real-time training"""
        def training_loop():
            while True:
                try:
                    # Fetch news every 30 minutes
                    news_count = self.fetch_real_time_news()
                    print(f"Fetched {news_count} news articles")
                    
                    # Build knowledge graph every hour
                    self.build_knowledge_graph()
                    
                    # Wait 30 minutes
                    time.sleep(1800)
                    
                except Exception as e:
                    print(f"Error in training loop: {e}")
                    time.sleep(300)  # Wait 5 minutes on error
        
        # Start training in background
        training_thread = threading.Thread(target=training_loop, daemon=True)
        training_thread.start()
        print("Real-time training started!")
    
    def get_training_stats(self):
        """Get training statistics"""
        return {
            "total_books": len(self.training_data.get("books", [])),
            "total_news": len(self.training_data.get("news", [])),
            "total_wikipedia": len(self.training_data.get("wikipedia", [])),
            "total_conversations": len(self.training_data.get("conversations", [])),
            "total_entities": len(self.knowledge_base.get("entities", {})),
            "last_updated": self.training_data.get("last_updated", "Never")
        }

# Global instance
data_trainer = DataTrainer()