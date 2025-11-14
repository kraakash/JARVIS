"""
Advanced Contextual AI - Real-time Activity Understanding
"""

import json
import os
from datetime import datetime
import re

try:
    import tensorflow as tf
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

class ContextualAI:
    def __init__(self):
        self.activity_patterns = {}
        self.question_history = []
        self.context_memory = []
        self.vectorizer = None
        self.activity_embeddings = {}
        self.user_responses = {}
        self.learning_data = []
        self.improvement_suggestions = []
        
        if ML_AVAILABLE:
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        self.load_context_knowledge()
        self.load_user_training_data()
    
    def load_context_knowledge(self):
        """Load pre-trained context knowledge"""
        self.context_knowledge = {
            'coding_patterns': {
                'python': ['error', 'debug', 'function', 'class', 'import', 'def'],
                'javascript': ['function', 'var', 'const', 'async', 'promise'],
                'web': ['html', 'css', 'react', 'vue', 'angular'],
                'data': ['pandas', 'numpy', 'matplotlib', 'sklearn']
            },
            'browsing_patterns': {
                'research': ['documentation', 'tutorial', 'guide', 'how to'],
                'social': ['facebook', 'twitter', 'instagram', 'linkedin'],
                'work': ['email', 'calendar', 'meeting', 'project'],
                'learning': ['course', 'video', 'lesson', 'training']
            },
            'file_patterns': {
                'organizing': ['folder', 'directory', 'file', 'organize'],
                'searching': ['find', 'search', 'locate', 'where'],
                'editing': ['edit', 'modify', 'change', 'update']
            }
        }
    
    def analyze_activity_context(self, app_name, window_title, duration):
        """Advanced context analysis using ML"""
        if not ML_AVAILABLE:
            return self._basic_context_analysis(app_name, window_title)
        
        # Create activity signature
        activity_text = f"{app_name} {window_title}".lower()
        
        # Extract meaningful features
        context = {
            'app': app_name.lower(),
            'title_words': self._extract_keywords(window_title),
            'duration': duration,
            'time_of_day': datetime.now().hour,
            'activity_type': self._classify_activity_type(app_name, window_title)
        }
        
        # Generate intelligent questions
        questions = self._generate_smart_questions(context)
        
        # Learn from this activity
        self._learn_activity_pattern(context, questions)
        
        return {
            'context': context,
            'questions': questions,
            'confidence': self._calculate_confidence(context)
        }
    
    def _extract_keywords(self, text):
        """Extract meaningful keywords from text"""
        # Remove common noise words
        noise_words = ['microsoft', 'google', 'chrome', 'edge', 'visual', 'studio', 'code']
        words = re.findall(r'\b\w+\b', text.lower())
        
        keywords = []
        for word in words:
            if len(word) > 2 and word not in noise_words:
                keywords.append(word)
        
        return keywords[:10]  # Top 10 keywords
    
    def load_user_training_data(self):
        """Load previously learned user responses"""
        try:
            if os.path.exists('contextual_training.json'):
                with open('contextual_training.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_responses = data.get('user_responses', {})
                    self.learning_data = data.get('learning_data', [])
                    self.improvement_suggestions = data.get('improvements', [])
        except Exception as e:
            print(f"[AI] Error loading training data: {e}")
    
    def save_user_training_data(self):
        """Save learned user responses"""
        try:
            data = {
                'user_responses': self.user_responses,
                'learning_data': self.learning_data,
                'improvements': self.improvement_suggestions,
                'last_updated': datetime.now().isoformat()
            }
            with open('contextual_training.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[AI] Error saving training data: {e}")
    
    def _classify_activity_type(self, app_name, window_title):
        """Classify the type of activity using pattern matching"""
        app = app_name.lower()
        title = window_title.lower()
        
        # Code development
        if any(code_app in app for code_app in ['code', 'pycharm', 'notepad++', 'sublime']):
            if any(ext in title for ext in ['.py', '.js', '.html', '.css', '.java', '.cpp']):
                return 'coding'
            else:
                return 'text_editing'
        
        # Web browsing
        elif any(browser in app for browser in ['chrome', 'firefox', 'edge', 'safari']):
            if any(site in title for site in ['github', 'stackoverflow', 'documentation']):
                return 'technical_research'
            elif any(site in title for site in ['youtube', 'coursera', 'udemy']):
                return 'learning'
            elif any(site in title for site in ['gmail', 'outlook', 'calendar']):
                return 'communication'
            else:
                return 'web_browsing'
        
        # File management
        elif 'explorer' in app or 'finder' in app:
            return 'file_management'
        
        # Communication
        elif any(comm_app in app for comm_app in ['teams', 'slack', 'discord', 'zoom']):
            return 'communication'
        
        return 'general'
    
    def _generate_smart_questions(self, context):
        """Generate contextually intelligent questions"""
        activity_type = context['activity_type']
        keywords = context['title_words']
        duration = context['duration']
        
        questions = []
        
        if activity_type == 'coding':
            # Analyze code context
            if any(word in keywords for word in ['error', 'exception', 'bug']):
                questions.extend([
                    "Kya error debug kar rahe hain? Main help kar sakta hun.",
                    "Error message kya aa raha hai? Batayiye."
                ])
            elif any(word in keywords for word in ['test', 'testing']):
                questions.extend([
                    "Code testing kar rahe hain? Results kaisa aa raha hai?",
                    "Kya test cases likhne mein help chahiye?"
                ])
            elif duration > 1800:  # 30 minutes
                questions.extend([
                    "Kaafi time se same code pe kaam kar rahe hain. Kya stuck hain?",
                    "Break lena chahiye ya koi specific help chahiye?"
                ])
            else:
                questions.extend([
                    "Kya feature develop kar rahe hain?",
                    "Code review chahiye?"
                ])
        
        elif activity_type == 'technical_research':
            if 'stackoverflow' in ' '.join(keywords):
                questions.extend([
                    "StackOverflow pe solution mil gaya?",
                    "Kya problem solve karne ki koshish kar rahe hain?"
                ])
            elif 'github' in ' '.join(keywords):
                questions.extend([
                    "GitHub pe kya explore kar rahe hain?",
                    "Koi interesting repository mila?"
                ])
            else:
                questions.extend([
                    "Research mein kya specific dhund rahe hain?",
                    "Technical documentation samajh aa raha hai?"
                ])
        
        elif activity_type == 'learning':
            questions.extend([
                "Kya naya seekh rahe hain?",
                "Tutorial follow kar rahe hain ya notes bana rahe hain?",
                "Koi doubt hai jo clear karna chahte hain?"
            ])
        
        elif activity_type == 'communication':
            questions.extend([
                "Important meeting chal raha hai?",
                "Kya emails check kar rahe hain?"
            ])
        
        elif activity_type == 'file_management':
            if duration > 300:  # 5 minutes
                questions.extend([
                    "Files organize karne mein time lag raha hai?",
                    "Koi specific file dhund rahe hain? Main help kar sakta hun."
                ])
            else:
                questions.extend([
                    "Files manage kar rahe hain?",
                    "Backup ya cleanup kar rahe hain?"
                ])
        
        # Add time-based questions
        hour = context['time_of_day']
        if hour < 10 and activity_type == 'coding':
            questions.append("Morning mein fresh mind se coding! Kya plan hai aaj ka?")
        elif hour > 22:
            questions.append("Late night kaam kar rahe hain? Health ka khayal rakhiye Sir.")
        
        return questions[:3]  # Return top 3 most relevant questions
    
    def _learn_activity_pattern(self, context, questions):
        """Learn from user activity patterns"""
        pattern_key = f"{context['activity_type']}_{context['app']}"
        
        if pattern_key not in self.activity_patterns:
            self.activity_patterns[pattern_key] = {
                'frequency': 0,
                'avg_duration': 0,
                'common_keywords': [],
                'successful_questions': []
            }
        
        pattern = self.activity_patterns[pattern_key]
        pattern['frequency'] += 1
        pattern['avg_duration'] = (pattern['avg_duration'] + context['duration']) / 2
        
        # Update common keywords
        for keyword in context['title_words']:
            if keyword not in pattern['common_keywords']:
                pattern['common_keywords'].append(keyword)
        
        # Keep only top 20 keywords
        pattern['common_keywords'] = pattern['common_keywords'][:20]
    
    def learn_from_user_response(self, question, user_answer, context):
        """Learn from user's answer to improve future questions"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'user_answer': user_answer.lower(),
            'context': context,
            'activity_type': context.get('activity_type', 'unknown'),
            'keywords': context.get('title_words', [])
        }
        
        self.learning_data.append(learning_entry)
        
        # Analyze user response for patterns
        self._analyze_user_response(question, user_answer, context)
        
        # Generate improvement suggestions
        self._generate_improvement_suggestions(learning_entry)
        
        # Save learning data
        self.save_user_training_data()
        
        print(f"[AI] Learned from response: '{user_answer}' for context: {context['activity_type']}")
    
    def _analyze_user_response(self, question, answer, context):
        """Analyze user response to understand their work patterns"""
        answer_lower = answer.lower()
        activity_type = context.get('activity_type', 'unknown')
        
        # Create response pattern key
        pattern_key = f"{activity_type}_responses"
        
        if pattern_key not in self.user_responses:
            self.user_responses[pattern_key] = {
                'common_answers': {},
                'work_patterns': {},
                'preferences': {},
                'improvement_areas': []
            }
        
        pattern = self.user_responses[pattern_key]
        
        # Track common answer patterns
        if answer_lower in pattern['common_answers']:
            pattern['common_answers'][answer_lower] += 1
        else:
            pattern['common_answers'][answer_lower] = 1
        
        # Analyze work patterns from responses
        if activity_type == 'coding':
            if any(word in answer_lower for word in ['error', 'bug', 'problem', 'issue']):
                pattern['work_patterns']['debugging'] = pattern['work_patterns'].get('debugging', 0) + 1
            elif any(word in answer_lower for word in ['feature', 'new', 'building', 'creating']):
                pattern['work_patterns']['development'] = pattern['work_patterns'].get('development', 0) + 1
            elif any(word in answer_lower for word in ['learning', 'tutorial', 'studying']):
                pattern['work_patterns']['learning'] = pattern['work_patterns'].get('learning', 0) + 1
        
        # Identify improvement areas
        if any(word in answer_lower for word in ['stuck', 'confused', 'difficult', 'hard']):
            if 'needs_help' not in pattern['improvement_areas']:
                pattern['improvement_areas'].append('needs_help')
        
        if any(word in answer_lower for word in ['slow', 'taking time', 'long']):
            if 'efficiency' not in pattern['improvement_areas']:
                pattern['improvement_areas'].append('efficiency')
    
    def _generate_improvement_suggestions(self, learning_entry):
        """Generate suggestions for productivity improvement"""
        answer = learning_entry['user_answer']
        activity_type = learning_entry['activity_type']
        
        suggestions = []
        
        if activity_type == 'coding':
            if any(word in answer for word in ['error', 'bug', 'stuck']):
                suggestions.extend([
                    "Code debugging mein help chahiye? Main error analysis kar sakta hun.",
                    "Debugging tools use karne ka suggestion du?",
                    "Similar errors ke solutions batau?"
                ])
            
            elif any(word in answer for word in ['slow', 'time', 'taking long']):
                suggestions.extend([
                    "Code efficiency improve karne ke tips du?",
                    "Faster development ke liye shortcuts batau?",
                    "Automation tools suggest karu?"
                ])
        
        elif activity_type == 'learning':
            if any(word in answer for word in ['difficult', 'hard', 'confusing']):
                suggestions.extend([
                    "Learning material simplify karne mein help karu?",
                    "Step-by-step breakdown chahiye?",
                    "Practice exercises suggest karu?"
                ])
        
        # Add unique suggestions
        for suggestion in suggestions:
            if suggestion not in self.improvement_suggestions:
                self.improvement_suggestions.append({
                    'suggestion': suggestion,
                    'context': activity_type,
                    'timestamp': datetime.now().isoformat()
                })
    
    def get_personalized_question(self, app_name, window_title, duration):
        """Get personalized question based on learned user patterns"""
        context = {
            'app': app_name.lower(),
            'title_words': self._extract_keywords(window_title),
            'activity_type': self._classify_activity_type(app_name, window_title),
            'duration': duration
        }
        
        activity_type = context['activity_type']
        
        # Check if we have learned patterns for this activity
        pattern_key = f"{activity_type}_responses"
        
        if pattern_key in self.user_responses:
            user_pattern = self.user_responses[pattern_key]
            
            # Generate personalized questions based on learned patterns
            if activity_type == 'coding':
                work_patterns = user_pattern.get('work_patterns', {})
                
                if work_patterns.get('debugging', 0) > work_patterns.get('development', 0):
                    return "Debugging kar rahe hain? Kya specific error aa raha hai?"
                elif work_patterns.get('learning', 0) > 2:
                    return "Naya concept seekh rahe hain? Samajh aa raha hai?"
                else:
                    return "Kya feature develop kar rahe hain? Progress kaisa hai?"
            
            elif activity_type == 'technical_research':
                if 'needs_help' in user_pattern.get('improvement_areas', []):
                    return "Research mein kya specific problem solve kar rahe hain? Main help kar sakta hun."
                else:
                    return "Technical research kar rahe hain? Kya interesting mila?"
        
        # Fallback to standard questions if no patterns learned yet
        return self._generate_smart_questions(context)[0] if self._generate_smart_questions(context) else "Kya kar rahe hain Sir?"
    
    def get_improvement_suggestions(self):
        """Get personalized improvement suggestions"""
        if not self.improvement_suggestions:
            return "Abhi tak koi specific improvement areas identify nahi hue hain."
        
        recent_suggestions = self.improvement_suggestions[-3:]
        response = "Productivity Improvement Suggestions:\n"
        
        for i, suggestion in enumerate(recent_suggestions, 1):
            response += f"{i}. {suggestion['suggestion']}\n"
        
        return response
    
    def analyze_work_patterns(self):
        """Analyze user's work patterns and provide insights"""
        if not self.learning_data:
            return "Abhi tak sufficient data nahi hai analysis ke liye."
        
        # Analyze activity distribution
        activity_counts = {}
        for entry in self.learning_data:
            activity = entry['activity_type']
            activity_counts[activity] = activity_counts.get(activity, 0) + 1
        
        # Find most common activity
        most_common = max(activity_counts.items(), key=lambda x: x[1])
        
        analysis = f"Work Pattern Analysis:\n"
        analysis += f"Most Common Activity: {most_common[0]} ({most_common[1]} times)\n"
        
        # Analyze improvement areas
        all_improvements = []
        for pattern in self.user_responses.values():
            all_improvements.extend(pattern.get('improvement_areas', []))
        
        if all_improvements:
            common_improvements = max(set(all_improvements), key=all_improvements.count)
            analysis += f"Main Improvement Area: {common_improvements}\n"
        
        analysis += f"Total Learning Entries: {len(self.learning_data)}"
        
        return analysis
    
    def _calculate_confidence(self, context):
        """Calculate confidence in context understanding"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on keyword matches
        if len(context['title_words']) > 3:
            confidence += 0.2
        
        # Increase confidence for known activity types
        if context['activity_type'] != 'general':
            confidence += 0.2
        
        # Increase confidence based on duration (more time = more context)
        if context['duration'] > 300:  # 5 minutes
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _basic_context_analysis(self, app_name, window_title):
        """Fallback analysis when ML is not available"""
        context = {
            'app': app_name.lower(),
            'title_words': self._extract_keywords(window_title),
            'activity_type': self._classify_activity_type(app_name, window_title)
        }
        
        questions = self._generate_smart_questions(context)
        
        return {
            'context': context,
            'questions': questions,
            'confidence': 0.7
        }
    
    def get_contextual_question(self, app_name, window_title, duration=0):
        """Main method to get intelligent contextual question"""
        # First try personalized question based on learned patterns
        if len(self.learning_data) > 5:  # If we have enough learning data
            personalized_question = self.get_personalized_question(app_name, window_title, duration)
            if personalized_question:
                return personalized_question
        
        # Fallback to standard analysis
        analysis = self.analyze_activity_context(app_name, window_title, duration)
        
        if analysis['questions'] and analysis['confidence'] > 0.6:
            return analysis['questions'][0]
        
        # Final fallback
        activity_type = analysis['context']['activity_type']
        if activity_type == 'coding':
            return "Code mein kya interesting kaam kar rahe hain Sir?"
        elif activity_type == 'web_browsing':
            return "Online research kar rahe hain ya casual browsing?"
        else:
            return f"{app_name} mein kya kaam kar rahe hain Sir?"

# Singleton instance
contextual_ai = ContextualAI()