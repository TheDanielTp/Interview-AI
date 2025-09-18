# interviewer.py
from ai_helper import call_deepseek
from typing import List

class InterviewerAgent:
    def __init__(self):
        self.aspect_priority = [
            "purpose", "inputs", "tools", "steps", 
            "exceptions", "success_criteria", "actors"
        ]
        
    def generate_question(self, state) -> str:
        if state.topic is None:
            return "What is the process you would like to describe?"
            
        conversation_text = state.get_conversation_text()
        recent_context = state.get_recent_context()
        
        # Determine which aspects still need coverage
        remaining_aspects = [a for a in self.aspect_priority if a not in state.covered_aspects]
        
        if not remaining_aspects:
            return "Thank you, I believe I have enough information to document this process thoroughly."
        
        next_aspect = remaining_aspects[0]
        
        system_message = """
        ATTENTION: You're being used for an API call.
        You are a professional process analyst conducting a structured interview.
        Your goal is to extract complete information about a process to create comprehensive documentation.
        
        GUIDELINES:
        1. Ask exactly ONE clear, specific question per interaction
        2. Focus on extracting information about one specific aspect of the process
        3. Never repeat questions that have already been asked
        4. If an aspect has been covered, move to the next one
        5. Be polite, professional, and concise
        6. If the user provides incomplete answers, ask follow-up questions for clarification
        7. Avoid yes/no questions - ask open-ended questions instead
        8. If all aspects are covered, thank the user and conclude the interview
        
        ASPECTS TO COVER:
        - Purpose: Why this process exists, its objectives and goals
        - Inputs: All materials, information, or resources needed
        - Tools: Equipment, software, or resources required
        - Steps: Detailed step-by-step instructions in chronological order
        - Exceptions: What could go wrong and how to handle it
        - Success Criteria: How to determine if the process was successful
        - Actors: Who performs the process and their responsibilities
        Note: Ask questions in order. Purpose -> Inputs -> Tools -> Steps -> Exceptions -> Success Criteria -> Actors
        
        IMPORTANT NOTES:
        - Make the questions in a natural tone which is related to the subject. Don't ask formal style questions.
        - This is an interview. You must ask the questions about what the user is going to do, not about the general process.
        - The questions are going to gather information about the subject. You shouldn't ask questions about the previous answers.
        """
        
        prompt = f"""
        PROCESS TOPIC: {state.topic}
        
        CONVERSATION HISTORY:
        {conversation_text}
        
        RECENT CONTEXT (last 3 interactions):
        {recent_context}
        
        CURRENT FOCUS: You need to ask about the {next_aspect} aspect of the process.
        
        ASPECTS ALREADY COVERED: {', '.join(state.covered_aspects) if state.covered_aspects else 'None'}
        
        Generate exactly ONE question that will extract detailed information about the {next_aspect} of the process.
        Make sure your question is specific, clear, and directly related to the {next_aspect}.
        Do not ask about aspects that have already been covered.
        
        Your question should:
        - Be open-ended to elicit detailed responses
        - Be specific to the process topic
        - Be concise (under 25 words if possible)
        - Build upon previous information when relevant
        
        QUESTION:
        """
        
        question = call_deepseek(prompt, system_message)
        
        if not question:
            # Fallback questions based on aspect
            fallbacks = {
                "purpose": "What is the main purpose or objective of this process?",
                "inputs": "What materials, information, or resources are needed to perform this process?",
                "tools": "What tools, equipment, or software are required for this process?",
                "steps": "What are the specific step-by-step instructions for performing this process?",
                "exceptions": "What could go wrong during this process, and how should those situations be handled?",
                "success_criteria": "How do you determine if this process has been completed successfully?",
                "actors": "Who is responsible for performing this process, and what are their specific roles?"
            }
            question = fallbacks.get(next_aspect, "Could you provide more details about this process?")
        
        # Clean up the question
        question = question.strip()
        if question.startswith('"') and question.endswith('"'):
            question = question[1:-1]
        
        return question