# state.py
import json
from datetime import datetime
from typing import List, Tuple

class ProcessState:
    def __init__(self):
        self.topic = None
        self.conversation_history: List[Tuple[str, str]] = []
        self.is_complete = False
        self.covered_aspects = set()
        self.start_time = datetime.now()
        self.validation_errors = 0
        
    def set_topic(self, topic: str):
        self.topic = topic
        
    def add_interaction(self, question: str, answer: str):
        self.conversation_history.append((question, answer))
        
        # Update covered aspects
        question_lower = question.lower()
        if "purpose" in question_lower or "why" in question_lower:
            self.covered_aspects.add("purpose")
        elif "input" in question_lower or "material" in question_lower:
            self.covered_aspects.add("inputs")
        elif "tool" in question_lower or "equipment" in question_lower:
            self.covered_aspects.add("tools")
        elif "step" in question_lower or "instruction" in question_lower:
            self.covered_aspects.add("steps")
        elif "exception" in question_lower or "problem" in question_lower:
            self.covered_aspects.add("exceptions")
        elif "success" in question_lower or "criteria" in question_lower:
            self.covered_aspects.add("success_criteria")
        elif "actor" in question_lower or "role" in question_lower:
            self.covered_aspects.add("actors")
            
    def get_conversation_text(self) -> str:
        text = f"Process Topic: {self.topic}\n\n"
        for i, (question, answer) in enumerate(self.conversation_history):
            text += f"Interaction {i+1}:\n"
            text += f"Question: {question}\n"
            text += f"Answer: {answer}\n\n"
        return text
    
    def get_recent_context(self, last_n: int = 3) -> str:
        """Get the most recent interactions for context"""
        if not self.conversation_history:
            return ""
        
        recent = self.conversation_history[-last_n:]
        text = ""
        for i, (question, answer) in enumerate(recent):
            text += f"Recent {i+1}:\n"
            text += f"Q: {question}\n"
            text += f"A: {answer}\n\n"
        return text
    
    def save_state(self, filename: str):
        """Save the current state to a file"""
        data = {
            "topic": self.topic,
            "conversation_history": self.conversation_history,
            "is_complete": self.is_complete,
            "covered_aspects": list(self.covered_aspects),
            "start_time": self.start_time.isoformat(),
            "validation_errors": self.validation_errors
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_state(self, filename: str):
        """Load state from a file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            self.topic = data["topic"]
            self.conversation_history = [tuple(item) for item in data["conversation_history"]]
            self.is_complete = data["is_complete"]
            self.covered_aspects = set(data["covered_aspects"])
            self.start_time = datetime.fromisoformat(data["start_time"])
            self.validation_errors = data["validation_errors"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading state: {e}")
    
    def get_stats(self):
        """Get statistics about the current state"""
        return {
            "topic": self.topic,
            "total_interactions": len(self.conversation_history),
            "covered_aspects": list(self.covered_aspects),
            "is_complete": self.is_complete,
            "validation_errors": self.validation_errors,
            "duration_minutes": (datetime.now() - self.start_time).total_seconds() / 60
        }