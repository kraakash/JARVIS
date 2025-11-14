"""
Real Tutor System for JARVIS - Live Examples & Step-by-Step Teaching
"""

class TutorSystem:
    def __init__(self):
        self.tutor_responses = {
            "binary_search": {
                "explanation": "Sir, binary search ek smart searching technique hai. Main aapko step-by-step sikhata hun:",
                "example": "Imagine aapke paas sorted array hai [1, 3, 5, 7, 9, 11, 13]. Aapko 7 dhundna hai.",
                "steps": [
                    "Step 1: Middle element dekho - index 3 pe 7 hai",
                    "Step 2: Target 7 == middle 7? Haan! Found!",
                    "Agar target chota hota, left half mein dhundte",
                    "Agar target bada hota, right half mein dhundte"
                ],
                "code_example": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid  # Found!
        elif arr[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half
    
    return -1  # Not found
                """,
                "real_world": "Real life mein: Dictionary mein word dhundna, phone book mein number dhundna - sab binary search use karte hain!"
            },
            
            "algorithm": {
                "explanation": "Sir, algorithm ek recipe ki tarah hai - step-by-step instructions jo problem solve karte hain.",
                "example": "Chai banane ka algorithm: 1) Paani garam karo, 2) Chai patti dalo, 3) Sugar add karo, 4) Boil karo, 5) Serve karo",
                "steps": [
                    "Input: Problem ya data",
                    "Process: Step-by-step solution",
                    "Output: Final result",
                    "Efficiency: Kitna time/memory lagta hai"
                ],
                "code_example": """
# Simple algorithm: Find maximum number
def find_max(numbers):
    max_num = numbers[0]  # Start with first number
    
    for num in numbers:   # Check each number
        if num > max_num:
            max_num = num # Update if bigger
    
    return max_num       # Return result
                """,
                "real_world": "GPS navigation, Google search, Netflix recommendations - sab algorithms use karte hain!"
            },
            
            "sorting": {
                "explanation": "Sir, sorting matlab data ko order mein arrange karna - ascending ya descending.",
                "example": "Aapke paas numbers hain [64, 34, 25, 12]. Sorted: [12, 25, 34, 64]",
                "steps": [
                    "Bubble Sort: Adjacent elements compare karo, swap karo",
                    "Selection Sort: Minimum find karo, beginning mein rakh do",
                    "Quick Sort: Pivot choose karo, partition karo",
                    "Merge Sort: Divide karo, sort karo, merge karo"
                ],
                "code_example": """
# Bubble Sort - Simple but slow
def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap
    
    return arr
                """,
                "real_world": "Excel mein data sort karna, leaderboard banana, file names arrange karna!"
            }
        }
    
    def get_tutor_response(self, topic):
        """Get comprehensive tutor-style response"""
        topic_key = topic.lower().replace(" ", "_")
        
        if topic_key in self.tutor_responses:
            data = self.tutor_responses[topic_key]
            
            response = f"{data['explanation']}\n\n"
            response += f"📚 Example: {data['example']}\n\n"
            response += "🔢 Steps:\n"
            
            for i, step in enumerate(data['steps'], 1):
                response += f"   {i}. {step}\n"
            
            response += f"\n💻 Code Example:\n{data['code_example']}\n"
            response += f"🌍 Real World: {data['real_world']}"
            
            return response
        
        return None

# Global instance
tutor_system = TutorSystem()