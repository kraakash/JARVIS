"""
Clean Algorithm Responses for JARVIS
"""

def get_algorithm_response(question):
    """Get clean algorithm responses"""
    # Skip auto-generated for now, use manual responses
    # try:
    #     from modules.ai.book_response_generator import book_response_generator
    #     auto_response = book_response_generator.get_clean_response(question)
    #     if auto_response:
    #         return auto_response
    # except Exception as e:
    #     print(f"[DEBUG] Auto-response error: {e}")
    
    # Fallback to manual responses
    question_lower = question.lower()
    
    if "binary search" in question_lower:
        return "Sir, binary search is an efficient algorithm that finds items in sorted arrays by repeatedly dividing the search space in half. It has O(log n) time complexity, making it much faster than linear search for large datasets."
    
    elif ("algorithm" in question_lower and ("what" in question_lower or "kya" in question_lower)) or ("algorithm kya hai" in question_lower):
        return "Sir, an algorithm is a step-by-step procedure for solving a problem. Algorithms have different time complexities measured in Big O notation, like O(1), O(log n), O(n), etc."
    
    elif "sorting" in question_lower or "sort" in question_lower:
        return "Sir, sorting algorithms arrange data in order. Common ones include quick sort O(n log n), merge sort O(n log n), and selection sort O(n²). Each has different performance characteristics."
    
    elif "big o" in question_lower or "bigo" in question_lower:
        return "Sir, Big O notation describes algorithm efficiency. It shows how runtime grows with input size. O(1) is constant, O(log n) is logarithmic, O(n) is linear, and O(n²) is quadratic."
    
    elif "recursion" in question_lower or "recursive" in question_lower:
        return "Sir, recursion is when a function calls itself to solve smaller versions of the same problem. It needs a base case to stop and makes problems easier to understand."
    
    elif "data structure" in question_lower or "datastructure" in question_lower:
        return "Sir, data structures organize and store data efficiently. Examples include arrays, linked lists, stacks, queues, trees, and graphs. Each has specific use cases and performance characteristics."
    
    elif "graph" in question_lower:
        return "Sir, graphs are data structures with nodes connected by edges. They're used for networks, social connections, and pathfinding algorithms like breadth-first search and Dijkstra's algorithm."
    
    elif "array" in question_lower:
        return "Sir, arrays store elements in contiguous memory locations with O(1) access time. They're simple but have fixed size in most languages."
    
    elif "complexity" in question_lower:
        return "Sir, algorithm complexity measures efficiency in time and space. Time complexity shows how runtime grows, space complexity shows memory usage as input increases."
    
    # Add more programming concepts
    elif "loop" in question_lower or "iteration" in question_lower:
        return "Sir, loops allow repeated execution of code blocks. Common types include for loops, while loops, and do-while loops. They're essential for processing collections and repetitive tasks."
    
    elif "variable" in question_lower:
        return "Sir, variables store data values in memory. They have names, types, and scopes. Variables can hold numbers, text, objects, or other data types depending on the programming language."
    
    elif "function" in question_lower:
        return "Sir, functions are reusable blocks of code that perform specific tasks. They can take parameters, process data, and return results. Functions help organize code and avoid repetition."
    
    elif "class" in question_lower and "object" in question_lower:
        return "Sir, classes are blueprints for creating objects in object-oriented programming. Objects are instances of classes that contain data (attributes) and behavior (methods)."
    
    return None