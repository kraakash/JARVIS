"""
JARVIS Desktop Monitor - Real-time Activity Tracking
"""

import time
import threading
from datetime import datetime
try:
    import win32gui
    import win32process
    import psutil
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    print("[MONITOR] Windows monitoring libraries not available")

class DesktopMonitor:
    def __init__(self):
        self.monitoring = False
        self.current_window = None
        self.window_start_time = None
        self.activity_log = []
        self.suggestions = []
        self.context_questions = []
        
    def start_monitoring(self):
        """Start desktop monitoring"""
        if not MONITORING_AVAILABLE:
            return False
            
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        print("[MONITOR] Desktop monitoring started")
        return True
    
    def stop_monitoring(self):
        """Stop desktop monitoring"""
        self.monitoring = False
        print("[MONITOR] Desktop monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Get current active window
                hwnd = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(hwnd)
                
                # Get process info
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                try:
                    process = psutil.Process(pid)
                    app_name = process.name()
                except:
                    app_name = "Unknown"
                
                # Check if window changed
                current_info = {
                    'title': window_title,
                    'app': app_name,
                    'pid': pid
                }
                
                if self.current_window != current_info:
                    self._log_window_change(current_info)
                    self.current_window = current_info
                    self.window_start_time = datetime.now()
                
                # Check for suggestions every 30 seconds
                if len(self.activity_log) > 0:
                    self._check_suggestions()
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                print(f"[MONITOR] Error: {e}")
                time.sleep(5)
    
    def _log_window_change(self, window_info):
        """Log window change activity"""
        timestamp = datetime.now()
        
        # Calculate time spent on previous window
        if self.window_start_time:
            duration = (timestamp - self.window_start_time).total_seconds()
        else:
            duration = 0
        
        activity = {
            'timestamp': timestamp,
            'app': window_info['app'],
            'title': window_info['title'],
            'duration': duration
        }
        
        self.activity_log.append(activity)
        
        # Keep only last 50 activities
        if len(self.activity_log) > 50:
            self.activity_log.pop(0)
        
        print(f"[MONITOR] {window_info['app']}: {window_info['title'][:50]}")
    
    def _check_suggestions(self):
        """Check for smart suggestions"""
        if not self.activity_log:
            return
        
        recent_activity = self.activity_log[-10:]  # Last 10 activities
        
        # Basic suggestions
        chrome_activities = [a for a in recent_activity if 'chrome' in a['app'].lower()]
        if len(chrome_activities) > 5:
            self._add_suggestion("productivity", "Chrome mein bahut tabs hain, organize kariye Sir!")
        
        code_apps = ['code.exe', 'notepad++.exe', 'pycharm64.exe', 'devenv.exe']
        coding_time = sum(a['duration'] for a in recent_activity if a['app'].lower() in [app.lower() for app in code_apps])
        if coding_time > 3600:  # 1 hour
            self._add_suggestion("health", "1 ghante se coding kar rahe hain Sir, break lein!")
        
        file_activities = [a for a in recent_activity if 'explorer.exe' in a['app'].lower()]
        if len(file_activities) > 3:
            self._add_suggestion("efficiency", "Same files bar bar khol rahe hain, bookmark kariye Sir!")
        
        # Use advanced AI for context analysis
        self._analyze_with_ai()
        
        # Smart automation analysis
        try:
            from modules.monitoring.smart_automation import smart_automation
            smart_automation.analyze_activity_patterns(self.activity_log)
        except Exception as e:
            print(f"[AUTOMATION] Error: {e}")
    
    def _add_suggestion(self, category, message):
        """Add suggestion to queue"""
        suggestion = {
            'category': category,
            'message': message,
            'timestamp': datetime.now()
        }
        
        # Avoid duplicate suggestions
        if not any(s['message'] == message for s in self.suggestions[-3:]):
            self.suggestions.append(suggestion)
            print(f"[SUGGESTION] {message}")
    
    def get_current_activity(self):
        """Get current activity info"""
        if not self.current_window:
            return None
        
        duration = 0
        if self.window_start_time:
            duration = (datetime.now() - self.window_start_time).total_seconds()
        
        return {
            'app': self.current_window['app'],
            'title': self.current_window['title'],
            'duration': int(duration)
        }
    
    def get_recent_suggestions(self):
        """Get recent suggestions"""
        return self.suggestions[-5:]  # Last 5 suggestions
    
    def get_activity_summary(self):
        """Get activity summary"""
        if not self.activity_log:
            return "No activity logged yet"
        
        # App usage summary
        app_usage = {}
        for activity in self.activity_log[-20:]:  # Last 20 activities
            app = activity['app']
            if app in app_usage:
                app_usage[app] += activity['duration']
            else:
                app_usage[app] = activity['duration']
        
        # Top 3 apps
        top_apps = sorted(app_usage.items(), key=lambda x: x[1], reverse=True)[:3]
        
        summary = "Recent Activity Summary:\n"
        for app, duration in top_apps:
            minutes = int(duration / 60)
            summary += f"  {app}: {minutes} minutes\n"
        
        return summary
    
    def _analyze_with_ai(self):
        """Use AI to analyze current activity and generate insights"""
        if not self.current_window:
            return
        
        try:
            from modules.ai.contextual_ai import contextual_ai
            
            duration = 0
            if self.window_start_time:
                duration = (datetime.now() - self.window_start_time).total_seconds()
            
            # Get AI analysis
            analysis = contextual_ai.analyze_activity_context(
                self.current_window['app'],
                self.current_window['title'],
                duration
            )
            
            # Store AI insights for later use
            if analysis['confidence'] > 0.7:
                for question in analysis['questions']:
                    self.context_questions.append({
                        'question': question,
                        'context': analysis['context']['activity_type'],
                        'confidence': analysis['confidence'],
                        'timestamp': datetime.now()
                    })
            
        except Exception as e:
            print(f"[AI] Context analysis error: {e}")
    
    def _generate_context_questions(self):
        """Generate intelligent questions based on current activity"""
        if not self.current_window:
            return
        
        app = self.current_window['app'].lower()
        title = self.current_window['title'].lower()
        
        questions = []
        
        # Code-related questions
        if 'code.exe' in app or 'pycharm' in app or 'notepad++' in app:
            if 'python' in title or '.py' in title:
                questions.extend([
                    "Kya Python code mein koi error aa raha hai?",
                    "Kya function test karna chahte hain?",
                    "Code optimize karne mein help chahiye?"
                ])
            elif 'javascript' in title or '.js' in title:
                questions.extend([
                    "JavaScript mein kya problem solve kar rahe hain?",
                    "Frontend ya backend code hai?"
                ])
            else:
                questions.extend([
                    "Kya code mein help chahiye?",
                    "Debugging kar rahe hain?",
                    "New feature add kar rahe hain?"
                ])
        
        # Browser-related questions
        elif 'chrome' in app or 'edge' in app or 'firefox' in app:
            if 'github' in title:
                questions.extend([
                    "GitHub pe kya search kar rahe hain?",
                    "Repository clone karna hai?"
                ])
            elif 'stackoverflow' in title:
                questions.extend([
                    "Kya programming problem solve kar rahe hain?",
                    "Error fix karne ki koshish kar rahe hain?"
                ])
            elif 'youtube' in title:
                questions.extend([
                    "Tutorial dekh rahe hain?",
                    "Kya seekhne ki koshish kar rahe hain?"
                ])
            else:
                questions.extend([
                    "Research kar rahe hain?",
                    "Kya information dhund rahe hain?"
                ])
        
        # File management
        elif 'explorer' in app:
            questions.extend([
                "Files organize kar rahe hain?",
                "Koi specific file dhund rahe hain?"
            ])
        
        # Add questions to queue
        for question in questions[:2]:  # Limit to 2 questions
            self.context_questions.append({
                'question': question,
                'context': app,
                'timestamp': datetime.now()
            })
    
    def get_context_question(self):
        """Get AI-powered relevant question based on current activity"""
        if not self.context_questions:
            return None
        
        # Sort by confidence and recency
        current_time = datetime.now()
        valid_questions = [
            q for q in self.context_questions 
            if (current_time - q['timestamp']).total_seconds() < 300
        ]
        
        if not valid_questions:
            return None
        
        # Get highest confidence question
        best_question = max(valid_questions, key=lambda x: x.get('confidence', 0.5))
        
        # Clean old questions
        self.context_questions = valid_questions
        
        return best_question['question']
    
    def ask_contextual_question(self):
        """Ask intelligent AI-powered question based on current activity"""
        if not self.current_window:
            return "Kya kar rahe hain Sir?"
        
        # Use advanced contextual AI
        try:
            from modules.ai.contextual_ai import contextual_ai
            
            duration = 0
            if self.window_start_time:
                duration = (datetime.now() - self.window_start_time).total_seconds()
            
            # Get AI-powered contextual question
            ai_question = contextual_ai.get_contextual_question(
                self.current_window['app'],
                self.current_window['title'],
                duration
            )
            
            return ai_question
            
        except Exception as e:
            print(f"[AI] Contextual AI error: {e}")
            # Fallback to basic questions
            app = self.current_window['app']
            if 'code' in app.lower():
                return "Coding kar rahe hain Sir? Kya help chahiye?"
            elif 'chrome' in app.lower() or 'edge' in app.lower():
                return "Browser mein kya kar rahe hain Sir?"
            else:
                return f"{app} use kar rahe hain Sir. Kya kar rahe hain?"

# Singleton instance
desktop_monitor = DesktopMonitor()