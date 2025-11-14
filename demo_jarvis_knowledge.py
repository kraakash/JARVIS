"""
Demo: JARVIS Answering from Book Knowledge
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_jarvis_answers():
    """Demo what JARVIS will answer after training"""
    
    print("🤖 JARVIS Knowledge Demo")
    print("=" * 40)
    print("After training with 'Grokking Algorithms' book:")
    print()
    
    # Simulate JARVIS responses
    examples = [
        {
            "user": "Jarvis, what is binary search?",
            "jarvis": "Sir, binary search is an efficient algorithm for finding items in sorted arrays. It works by repeatedly dividing the search interval in half, comparing the target with the middle element. Time complexity is O(log n), making it much faster than linear search for large datasets."
        },
        {
            "user": "Tell me about Big O notation",
            "jarvis": "Sir, Big O notation describes algorithm efficiency and performance. It tells you how runtime grows as input size increases. For example: O(1) is constant time, O(log n) is logarithmic, O(n) is linear, and O(n²) is quadratic. It helps compare algorithm efficiency."
        },
        {
            "user": "What are sorting algorithms?",
            "jarvis": "Sir, sorting algorithms arrange data in order. Common ones include: Quick sort (O(n log n) average), Merge sort (O(n log n) guaranteed), Selection sort (O(n²)). Each has different trade-offs between speed, memory usage, and stability."
        },
        {
            "user": "Explain recursion",
            "jarvis": "Sir, recursion is when a function calls itself to solve smaller versions of the same problem. It needs a base case to stop and a recursive case that moves toward the base. Examples include calculating factorials, tree traversals, and divide-and-conquer algorithms."
        },
        {
            "user": "What is dynamic programming?",
            "jarvis": "Sir, dynamic programming solves complex problems by breaking them into simpler subproblems and storing results to avoid redundant calculations. It's useful for optimization problems like finding shortest paths, knapsack problems, and sequence alignment."
        }
    ]
    
    for example in examples:
        print(f"👤 You: \"{example['user']}\"")
        print(f"🤖 JARVIS: \"{example['jarvis']}\"")
        print()
    
    print("🎯 How to Enable This:")
    print("1. Run: python train_single_book.py \"path/to/book.pdf\"")
    print("2. Start JARVIS: python main.py")
    print("3. Ask algorithm questions!")
    print()
    print("📚 JARVIS will now answer from trained book knowledge!")

if __name__ == "__main__":
    demo_jarvis_answers()