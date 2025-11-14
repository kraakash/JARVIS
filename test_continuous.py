"""
Test Continuous Voice Conversation
"""

from core.brain import JarvisBrain

def test_continuous():
    brain = JarvisBrain()
    
    print("Testing continuous conversation...")
    
    # Start continuous mode
    response = brain.process_command("start continuous conversation")
    print(f"Start: {response}")
    
    # Simulate some conversation
    test_commands = [
        "how are you",
        "what time is it", 
        "tell me a joke",
        "open calculator"
    ]
    
    for cmd in test_commands:
        print(f"\nUser: {cmd}")
        response = brain.process_command(cmd)
        print(f"JARVIS: {response}")
    
    # Stop continuous mode
    response = brain.process_command("stop continuous conversation")
    print(f"\nStop: {response}")

if __name__ == "__main__":
    test_continuous()