import json
import os
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.session_file = "jarvis_session.json"
        self.session_data = self.load_session()
    
    def load_session(self):
        """Load previous session data"""
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "monitoring_active": False,
            "last_mode": "normal",
            "session_count": 0,
            "last_shutdown": None
        }
    
    def save_session(self):
        """Save current session data"""
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def set_monitoring_mode(self, active):
        """Set monitoring mode state"""
        self.session_data["monitoring_active"] = active
        self.session_data["last_mode"] = "monitoring" if active else "normal"
        self.save_session()
    
    def is_monitoring_active(self):
        """Check if monitoring was active in last session"""
        return self.session_data.get("monitoring_active", False)
    
    def get_last_mode(self):
        """Get the last active mode"""
        return self.session_data.get("last_mode", "normal")
    
    def increment_session(self):
        """Increment session counter"""
        self.session_data["session_count"] = self.session_data.get("session_count", 0) + 1
        self.save_session()
    
    def set_shutdown_time(self):
        """Record shutdown time"""
        self.session_data["last_shutdown"] = datetime.now().isoformat()
        self.save_session()

# Singleton instance
session_manager = SessionManager()