"""
Book Processing System for JARVIS Training
Processes PDF, TXT, EPUB books for training data
"""

import os
import json
from datetime import datetime
import PyPDF2
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import docx
import re

class BookProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt', '.epub', '.docx']
        self.processed_books = []
        
    def process_pdf(self, file_path):
        """Process PDF files"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return self.clean_text(text)
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return ""
    
    def process_txt(self, file_path):
        """Process TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                return self.clean_text(text)
        except Exception as e:
            print(f"Error processing TXT {file_path}: {e}")
            return ""
    
    def process_epub(self, file_path):
        """Process EPUB files"""
        try:
            book = epub.read_epub(file_path)
            text = ""
            
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += soup.get_text() + "\n"
            
            return self.clean_text(text)
        except Exception as e:
            print(f"Error processing EPUB {file_path}: {e}")
            return ""
    
    def process_docx(self, file_path):
        """Process DOCX files"""
        try:
            doc = docx.Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self.clean_text(text)
        except Exception as e:
            print(f"Error processing DOCX {file_path}: {e}")
            return ""
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'"()-]', '', text)
        
        # Remove very short lines
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 10]
        
        return '\n'.join(cleaned_lines)
    
    def extract_chapters(self, text, book_title):
        """Extract chapters from book text"""
        # Split text into chunks for better processing
        words = text.split()
        chunk_size = 2000  # Words per chunk
        
        chapters = []
        
        # If text is small, treat as single chapter
        if len(words) < chunk_size:
            chapters.append({
                "title": "Complete Content",
                "content": text
            })
            return chapters
        
        # Split into multiple chapters based on content
        for i in range(0, len(words), chunk_size):
            chunk_words = words[i:i + chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            # Try to find a good chapter title from first few words
            first_line = ' '.join(chunk_words[:10])
            
            # Look for chapter indicators
            chapter_indicators = ['chapter', 'introduction', 'algorithm', 'search', 'sort', 'graph', 'tree', 'array']
            chapter_title = f"Chapter {len(chapters) + 1}"
            
            for indicator in chapter_indicators:
                if indicator.lower() in first_line.lower():
                    chapter_title = f"Chapter {len(chapters) + 1}: {indicator.title()}"
                    break
            
            chapters.append({
                "title": chapter_title,
                "content": chunk_text
            })
        
        return chapters
    
    def process_book_folder(self, folder_path):
        """Process all books in a folder"""
        processed_count = 0
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in self.supported_formats:
                    print(f"Processing: {file}")
                    
                    # Process based on file type
                    if file_ext == '.pdf':
                        text = self.process_pdf(file_path)
                    elif file_ext == '.txt':
                        text = self.process_txt(file_path)
                    elif file_ext == '.epub':
                        text = self.process_epub(file_path)
                    elif file_ext == '.docx':
                        text = self.process_docx(file_path)
                    else:
                        continue
                    
                    if text:
                        # Extract chapters
                        chapters = self.extract_chapters(text, file)
                        
                        book_data = {
                            "title": os.path.splitext(file)[0],
                            "file_path": file_path,
                            "chapters": chapters,
                            "total_words": len(text.split()),
                            "processed_date": datetime.now().isoformat(),
                            "file_type": file_ext
                        }
                        
                        self.processed_books.append(book_data)
                        processed_count += 1
        
        return processed_count
    
    def save_processed_books(self, output_file="d:/Code/Jarvis/processed_books.json"):
        """Save processed books to JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.processed_books, f, indent=2, ensure_ascii=False)
    
    def get_book_knowledge(self, query):
        """Get knowledge from processed books"""
        query_lower = query.lower()
        relevant_content = []
        
        for book in self.processed_books:
            for chapter in book["chapters"]:
                if any(word in chapter["content"].lower() for word in query_lower.split()):
                    relevant_content.append({
                        "book": book["title"],
                        "chapter": chapter["title"],
                        "content": chapter["content"][:500] + "...",
                        "relevance_score": self.calculate_relevance(query_lower, chapter["content"].lower())
                    })
        
        # Sort by relevance
        relevant_content.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return relevant_content[:5]  # Top 5 results
    
    def calculate_relevance(self, query, content):
        """Calculate relevance score"""
        query_words = query.split()
        content_words = content.split()
        
        matches = 0
        for word in query_words:
            if word in content_words:
                matches += content_words.count(word)
        
        return matches / len(query_words) if query_words else 0

# Global instance
book_processor = BookProcessor()