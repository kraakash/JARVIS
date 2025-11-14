"""
Ollama-based Real Tutor System for JARVIS
"""

import requests
import json
import time

class OllamaTutor:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "codellama:7b-instruct"
        self.available = self.check_availability()
    
    def check_availability(self):
        """Check if Ollama is running"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def get_tutor_explanation(self, topic, question=""):
        """Get comprehensive tutor-style explanation"""
        
        if not self.available:
            return self.get_fallback_response(topic)
        
        # Create tutor-style prompt
        prompt = f"""You are JARVIS, a friendly programming tutor. Explain {topic} in this exact format:

Sir, {topic} samjhiye step-by-step!

🎯 Simple Definition:
[Give 1-2 line simple explanation in Hindi-English mix]

📚 Real-World Analogy:
[Compare with everyday example like games, cooking, etc.]

🔢 Live Example:
[Show actual numbers/data step-by-step]

💻 Working Code:
```python
[Provide clean, commented code]
```

🌍 Real Applications:
[Where is this used in real world]

❓ Quick Question:
[Ask a simple practice question]

Keep it conversational, use "Sir" and Hindi-English mix. Make it feel like a real tutor teaching.

User asked: {question}"""

        try:
            response = requests.post(
                self.base_url,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['response'].strip()
            else:
                return self.get_fallback_response(topic)
                
        except Exception as e:
            print(f"[TUTOR] Ollama error: {e}")
            return self.get_fallback_response(topic)
    
    def get_fallback_response(self, topic):
        """Fallback responses when Ollama is not available"""
        
        fallback_responses = {
            "binary search": """Sir, binary search samjhiye step-by-step!

🎯 Simple Definition:
Binary search ek smart technique hai jo sorted array mein element dhundti hai by dividing search space in half.

📚 Real-World Analogy:
Dictionary mein word dhundna - aap middle page khol ke dekh te hain, phir decide karte hain left ya right jaana hai!

🔢 Live Example:
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Middle = 7 (index 3) → Found it! ✅
Agar 5 dhundte: Middle = 7 → "Too high" → Left half mein dhundo

💻 Working Code:
```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # Mil gaya!
        elif arr[mid] < target:
            left = mid + 1  # Right side dhundo
        else:
            right = mid - 1  # Left side dhundo
    
    return -1  # Nahi mila
```

🌍 Real Applications:
Google search, phone contacts, library systems, database queries!

❓ Quick Question:
Agar 1000 elements hain, maximum kitne comparisons lagenge? (Hint: log₂(1000) ≈ 10)""",

            "algorithm": """Sir, algorithm samjhiye step-by-step!

🎯 Simple Definition:
Algorithm ek step-by-step recipe hai jo koi problem solve karta hai - like cooking recipe!

📚 Real-World Analogy:
Chai banane ka process: 1) Paani boil karo, 2) Chai patti dalo, 3) Sugar add karo, 4) Serve karo

🔢 Live Example:
Problem: Find maximum number in [64, 34, 25, 12, 22, 11, 90]

Step 1: Start with first number (64)
Step 2: Compare with next (34) → 64 is bigger
Step 3: Compare with next (25) → 64 is bigger
...continue...
Step 7: Compare with (90) → 90 is bigger! New max = 90

💻 Working Code:
```python
def find_max(numbers):
    max_num = numbers[0]  # Start with first
    
    for num in numbers:
        if num > max_num:
            max_num = num  # Update if bigger
    
    return max_num
```

🌍 Real Applications:
GPS navigation, Google search ranking, Netflix recommendations, game AI!

❓ Quick Question:
Agar 100 numbers hain, kitne comparisons lagenge maximum find karne ke liye?""",

            "sorting": """Sir, sorting samjhiye step-by-step!

🎯 Simple Definition:
Sorting matlab data ko order mein arrange karna - ascending (chota se bada) ya descending (bada se chota).

📚 Real-World Analogy:
Playing cards ko arrange karna by number, ya students ko height ke hisaab se line mein khada karna!

🔢 Live Example:
Unsorted: [64, 34, 25, 12]
Bubble Sort process:
Pass 1: [34, 25, 12, 64] (64 bubble up)
Pass 2: [25, 12, 34, 64] (34 bubble up)  
Pass 3: [12, 25, 34, 64] (25 bubble up)
Sorted! ✅

💻 Working Code:
```python
def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
    
    return arr
```

🌍 Real Applications:
Excel data sorting, leaderboards, file organization, search results ranking!

❓ Quick Question:
Agar 5 numbers hain, bubble sort mein maximum kitne swaps ho sakte hain?"""
        }
        
        topic_lower = topic.lower()
        for key, response in fallback_responses.items():
            if key in topic_lower:
                return response
        
        return f"Sir, {topic} ke baare mein detailed explanation chahiye. Ollama service start kariye for advanced tutoring!"
    
    def get_interactive_response(self, user_input):
        """Get interactive tutor response"""
        
        # Detect what user is asking about
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ["binary search", "binary"]):
            return self.get_tutor_explanation("binary search", user_input)
        elif any(word in user_lower for word in ["algorithm", "algo"]):
            return self.get_tutor_explanation("algorithm", user_input)
        elif any(word in user_lower for word in ["sorting", "sort"]):
            return self.get_tutor_explanation("sorting", user_input)
        elif any(word in user_lower for word in ["recursion", "recursive"]):
            return self.get_tutor_explanation("recursion", user_input)
        elif any(word in user_lower for word in ["big o", "complexity"]):
            return self.get_tutor_explanation("big o notation", user_input)
        else:
            return self.get_tutor_explanation("programming concept", user_input)

# Global instance
ollama_tutor = OllamaTutor()