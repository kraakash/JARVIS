"""
JARVIS Smart Automation - Context-aware recommendations and workflow optimization
"""

import time
from datetime import datetime, timedelta
from collections import defaultdict

class SmartAutomation:
    def __init__(self):
        self.patterns = defaultdict(list)
        self.automation_rules = []
        self.user_preferences = {}
        self.workflow_suggestions = []
        
    def analyze_activity_patterns(self, activity_log):
        """Analyze user activity patterns for automation"""
        if len(activity_log) < 5:
            return
        
        # Pattern 1: Frequent app switching
        self._detect_app_switching_pattern(activity_log)
        
        # Pattern 2: Repetitive workflows
        self._detect_repetitive_workflows(activity_log)
        
        # Pattern 3: Time-based patterns
        self._detect_time_patterns(activity_log)
        
        # Pattern 4: Browser tab management
        self._detect_browser_patterns(activity_log)
    
    def _detect_app_switching_pattern(self, activity_log):
        """Detect frequent app switching"""
        recent_activities = activity_log[-10:]
        app_switches = len(set(a['app'] for a in recent_activities))
        
        if app_switches > 6:  # Too many different apps
            self._add_automation_suggestion(
                "workflow_optimization",
                "Bahut apps switch kar rahe hain Sir. Main organize kar dun?",
                "frequent_switching",
                {"apps": [a['app'] for a in recent_activities]}
            )
    
    def _detect_repetitive_workflows(self, activity_log):
        """Detect repetitive workflows that can be automated"""
        # Look for patterns like: Code -> Browser -> Code -> Browser
        recent_apps = [a['app'] for a in activity_log[-8:]]
        
        # Check for alternating pattern
        if len(recent_apps) >= 4:
            pattern_detected = False
            
            # Check Code -> Browser pattern
            code_browser_pattern = []
            for i in range(len(recent_apps) - 1):
                if ('code' in recent_apps[i].lower() and 
                    'chrome' in recent_apps[i+1].lower()) or \
                   ('chrome' in recent_apps[i].lower() and 
                    'code' in recent_apps[i+1].lower()):
                    code_browser_pattern.append((recent_apps[i], recent_apps[i+1]))
            
            if len(code_browser_pattern) >= 2:
                self._add_automation_suggestion(
                    "workflow_automation",
                    "Code aur Browser ke beech switch kar rahe hain. Split screen suggest karun?",
                    "code_browser_workflow",
                    {"pattern": code_browser_pattern}
                )
    
    def _detect_time_patterns(self, activity_log):
        """Detect time-based usage patterns"""
        current_hour = datetime.now().hour
        
        # Morning productivity pattern (9-12)
        if 9 <= current_hour <= 12:
            code_time = sum(a['duration'] for a in activity_log[-5:] 
                          if 'code' in a['app'].lower() or 'notepad' in a['app'].lower())
            
            if code_time > 1800:  # 30 minutes of coding
                self._add_automation_suggestion(
                    "productivity_boost",
                    "Morning productive session chal raha hai! Focus mode enable karein?",
                    "morning_focus",
                    {"coding_time": code_time}
                )
    
    def _detect_browser_patterns(self, activity_log):
        """Detect browser usage patterns"""
        browser_activities = [a for a in activity_log[-10:] 
                            if 'chrome' in a['app'].lower() or 'edge' in a['app'].lower()]
        
        if len(browser_activities) > 5:
            total_browser_time = sum(a['duration'] for a in browser_activities)
            
            if total_browser_time > 1200:  # 20 minutes
                self._add_automation_suggestion(
                    "browser_optimization",
                    "Browser mein bahut time spend kar rahe hain. Tab organizer chalayein?",
                    "browser_cleanup",
                    {"browser_time": total_browser_time, "sessions": len(browser_activities)}
                )
    
    def _add_automation_suggestion(self, category, message, rule_type, metadata):
        """Add automation suggestion"""
        suggestion = {
            'category': category,
            'message': message,
            'rule_type': rule_type,
            'metadata': metadata,
            'timestamp': datetime.now(),
            'priority': self._calculate_priority(category, metadata)
        }
        
        # Avoid duplicates
        if not any(s['rule_type'] == rule_type for s in self.workflow_suggestions[-3:]):
            self.workflow_suggestions.append(suggestion)
            print(f"[AUTOMATION] {message}")
    
    def _calculate_priority(self, category, metadata):
        """Calculate suggestion priority"""
        priority_map = {
            'workflow_optimization': 3,
            'workflow_automation': 4,
            'productivity_boost': 5,
            'browser_optimization': 2
        }
        return priority_map.get(category, 1)
    
    def get_automation_suggestions(self):
        """Get current automation suggestions"""
        # Sort by priority and recency
        sorted_suggestions = sorted(
            self.workflow_suggestions[-10:],
            key=lambda x: (x['priority'], x['timestamp']),
            reverse=True
        )
        return sorted_suggestions[:5]
    
    def execute_automation(self, rule_type, user_consent=True):
        """Execute automation based on rule type"""
        if not user_consent:
            return False, "User consent required"
        
        try:
            if rule_type == "browser_cleanup":
                return self._suggest_browser_cleanup()
            elif rule_type == "code_browser_workflow":
                return self._suggest_split_screen()
            elif rule_type == "morning_focus":
                return self._suggest_focus_mode()
            elif rule_type == "frequent_switching":
                return self._suggest_app_organization()
            else:
                return False, "Unknown automation rule"
        except Exception as e:
            return False, f"Automation failed: {e}"
    
    def _suggest_browser_cleanup(self):
        """Suggest browser tab cleanup"""
        suggestions = [
            "Chrome mein tabs organize kariye",
            "Bookmarks banayiye frequently used sites ke liye",
            "Tab groups use kariye similar content ke liye"
        ]
        return True, "Browser cleanup suggestions: " + "; ".join(suggestions)
    
    def _suggest_split_screen(self):
        """Suggest split screen setup"""
        suggestions = [
            "Windows key + Left/Right arrow use kariye split screen ke liye",
            "Code left side, Browser right side rakhiye",
            "Alt+Tab ki jagah mouse use kariye quick switching ke liye"
        ]
        return True, "Split screen suggestions: " + "; ".join(suggestions)
    
    def _suggest_focus_mode(self):
        """Suggest focus mode activation"""
        suggestions = [
            "Notifications band kar diye",
            "Distracting websites block kar diye", 
            "Focus timer 25 minutes set kar diya"
        ]
        return True, "Focus mode activated: " + "; ".join(suggestions)
    
    def _suggest_app_organization(self):
        """Suggest app organization"""
        suggestions = [
            "Taskbar mein frequently used apps pin kariye",
            "Desktop shortcuts organize kariye",
            "Virtual desktops use kariye different tasks ke liye"
        ]
        return True, "App organization suggestions: " + "; ".join(suggestions)
    
    def learn_user_preference(self, rule_type, accepted):
        """Learn from user feedback"""
        if rule_type not in self.user_preferences:
            self.user_preferences[rule_type] = {'accepted': 0, 'rejected': 0}
        
        if accepted:
            self.user_preferences[rule_type]['accepted'] += 1
        else:
            self.user_preferences[rule_type]['rejected'] += 1
    
    def get_automation_stats(self):
        """Get automation statistics"""
        total_suggestions = len(self.workflow_suggestions)
        categories = defaultdict(int)
        
        for suggestion in self.workflow_suggestions:
            categories[suggestion['category']] += 1
        
        return {
            'total_suggestions': total_suggestions,
            'categories': dict(categories),
            'user_preferences': self.user_preferences,
            'recent_suggestions': len([s for s in self.workflow_suggestions 
                                     if s['timestamp'] > datetime.now() - timedelta(hours=1)])
        }

# Singleton instance
smart_automation = SmartAutomation()