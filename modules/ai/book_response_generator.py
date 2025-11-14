"""
Automatic Clean Response Generator from Books
"""

import json
import re
from datetime import datetime

class BookResponseGenerator:
    def __init__(self):
        self.clean_responses = {}
        self.load_clean_responses()
    
    def load_clean_responses(self):
        """Load existing clean responses"""
        try:
            with open("d:/Code/Jarvis/clean_book_responses.json", 'r', encoding='utf-8') as f:
                self.clean_responses = json.load(f)
        except:
            self.clean_responses = {}
    
    def save_clean_responses(self):
        """Save clean responses to file"""
        with open("d:/Code/Jarvis/clean_book_responses.json", 'w', encoding='utf-8') as f:
            json.dump(self.clean_responses, f, indent=2, ensure_ascii=False)
    
    def extract_clean_definition(self, text, keyword):
        """Extract clean definition from book text"""
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # Find keyword position
        keyword_pos = text_lower.find(keyword_lower)
        if keyword_pos == -1:
            return None
        
        # Get sentences around keyword
        sentences = re.split(r'[.!?]+', text)
        
        for i, sentence in enumerate(sentences):
            if keyword_lower in sentence.lower():
                # Get current and next 1-2 sentences
                definition_parts = []
                for j in range(i, min(i + 3, len(sentences))):
                    clean_sentence = sentences[j].strip()
                    if len(clean_sentence) > 10:
                        definition_parts.append(clean_sentence)
                
                if definition_parts:
                    definition = '. '.join(definition_parts)
                    # Clean up the definition
                    definition = self.clean_definition_text(definition)
                    return definition
        
        return None
    
    def clean_definition_text(self, text):
        """Clean and format definition text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and references
        text = re.sub(r'\b\d+\b', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()-]', '', text)
        
        # Capitalize first letter
        text = text.strip()
        if text:
            text = text[0].upper() + text[1:]
        
        # Ensure it ends with period
        if text and not text.endswith('.'):
            text += '.'
        
        return text
    
    def generate_responses_from_book(self, training_data):
        """Generate clean responses from book training data"""
        
        # Common programming/algorithm keywords to extract
        keywords = [
            "algorithm", "binary search", "linear search", "sorting", "bubble sort",
            "quick sort", "merge sort", "selection sort", "big o notation", 
            "time complexity", "space complexity", "recursion", "iteration",
            "data structure", "array", "linked list", "stack", "queue",
            "tree", "binary tree", "graph", "hash table", "dictionary",
            "breadth first search", "depth first search", "dynamic programming",
            "greedy algorithm", "divide and conquer", "backtracking",
            "variable", "function", "loop", "condition", "class", "object"
        ]
        
        generated_count = 0
        
        if "books" in training_data:
            for book_entry in training_data["books"]:
                book_text = book_entry.get("text", "")
                book_source = book_entry.get("source", "Unknown Book")
                
                for keyword in keywords:
                    if keyword.lower() in book_text.lower():
                        # Generate clean response
                        clean_def = self.extract_clean_definition(book_text, keyword)
                        
                        if clean_def and len(clean_def) > 50:
                            # Store multiple question variations
                            question_variations = [
                                f"what is {keyword}",
                                f"{keyword} kya hai",
                                f"tell me about {keyword}",
                                f"{keyword} ke baare mein batao",
                                f"explain {keyword}",
                                f"{keyword} samjhao"
                            ]
                            
                            for question in question_variations:
                                self.clean_responses[question] = {
                                    "response": f"Sir, {clean_def}",
                                    "source": book_source,
                                    "keyword": keyword,
                                    "generated_date": datetime.now().isoformat()
                                }
                            
                            generated_count += 1
        
        self.save_clean_responses()
        return generated_count
    
    def get_clean_response(self, question):
        """Get clean response for a question"""
        question_lower = question.lower().strip()
        
        # Direct match
        if question_lower in self.clean_responses:
            return self.clean_responses[question_lower]["response"]
        
        # Fuzzy match
        for stored_question, data in self.clean_responses.items():
            # Check if key words match
            question_words = set(question_lower.split())
            stored_words = set(stored_question.split())
            
            # If 70% words match
            common_words = question_words.intersection(stored_words)
            if len(common_words) >= len(question_words) * 0.7:
                return data["response"]
        
        return None
    
    def get_stats(self):
        """Get generation statistics"""
        return {
            "total_responses": len(self.clean_responses),
            "unique_keywords": len(set(data["keyword"] for data in self.clean_responses.values())),
            "sources": list(set(data["source"] for data in self.clean_responses.values()))
        }

# Global instance
book_response_generator = BookResponseGenerator()