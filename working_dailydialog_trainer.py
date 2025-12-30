#!/usr/bin/env python3
"""
Working DailyDialog Trainer - Fixed API approach
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

try:
    from modules.ai.jarvis_model import jarvis_model
    JARVIS_AVAILABLE = True
except ImportError as e:
    print(f"[ERROR] JARVIS model not available: {e}")
    JARVIS_AVAILABLE = False

def fetch_with_retry(offset=0, length=50):
    """Fetch data with proper error handling and retry"""
    url = f"https://datasets-server.huggingface.co/rows?dataset=roskoN%2Fdailydialog&config=full&split=train&offset={offset}&length={length}"
    
    for attempt in range(3):
        try:
            print(f"[FETCH] Attempt {attempt+1}: offset {offset}, length {length}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rows = data.get('rows', [])
                print(f"[SUCCESS] Got {len(rows)} rows")
                return rows
            elif response.status_code == 429:
                print(f"[RATE_LIMIT] Waiting 5 seconds...")
                time.sleep(5)
            else:
                print(f"[ERROR] Status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    
    return []

def extract_conversations(rows):
    """Extract conversations from API response"""
    conversations = []
    
    for row in rows:
        try:
            # Debug: Print row structure
            print(f"[DEBUG] Row keys: {list(row.keys())}")
            
            if 'row' in row:
                row_data = row['row']
                print(f"[DEBUG] Row data keys: {list(row_data.keys())}")
                
                if 'utterances' in row_data:
                    utterances = row_data['utterances']
                    print(f"[DEBUG] Utterances length: {len(utterances)}")
                    
                    # Extract Q&A pairs
                    for i in range(0, len(utterances)-1, 2):
                        if i+1 < len(utterances):
                            q = utterances[i].strip()
                            a = utterances[i+1].strip()
                            
                            if len(q) > 3 and len(a) > 3 and len(q) < 80 and len(a) < 120:
                                conversations.append({
                                    'question': q,
                                    'response': a,
                                    'source': 'dailydialog_api'
                                })
                                print(f"[CONV] Q: {q[:30]}... A: {a[:30]}...")
            
        except Exception as e:
            print(f"[WARN] Row processing error: {e}")
    
    return conversations

def train_from_api():
    """Train JARVIS from DailyDialog API"""
    if not JARVIS_AVAILABLE:
        print("[ERROR] JARVIS not available")
        return False
    
    print("Starting API training...")
    
    total_trained = 0
    
    # Try different offsets
    for offset in [0, 50, 100, 200, 500]:
        print(f"\n--- Trying offset {offset} ---")
        
        rows = fetch_with_retry(offset, 20)  # Smaller batches
        
        if not rows:
            print(f"No data at offset {offset}")
            continue
        
        conversations = extract_conversations(rows)
        
        if conversations:
            print(f"[TRAIN] Training {len(conversations)} conversations...")
            
            for conv in conversations:
                try:
                    jarvis_model.add_conversation(conv['question'], conv['response'])
                    total_trained += 1
                    
                    if total_trained % 5 == 0:
                        print(f"[PROGRESS] Trained {total_trained} conversations")
                
                except Exception as e:
                    print(f"[WARN] Training error: {e}")
        
        # Don't overwhelm the API
        time.sleep(3)
        
        if total_trained >= 20:  # Stop after 20 successful trainings
            break
    
    print(f"\n[FINAL] Total trained: {total_trained}")
    return total_trained > 0

if __name__ == "__main__":
    print("Working DailyDialog Trainer")
    print("=" * 40)
    
    success = train_from_api()
    
    if success:
        print("\n[SUCCESS] API training completed!")
        
        # Show updated stats
        try:
            stats = jarvis_model.get_model_stats()
            print(f"Total conversations now: {stats['total_conversations']}")
        except:
            pass
    else:
        print("\n[FAILED] API training failed")