# validator.py
from ai_helper import call_deepseek
from datetime import datetime
import json
import re

class ValidatorAgent:
    def __init__(self):
        self.validation_history = []
        
    def validate_answer(self, state, question, answer):
        if not answer.strip():
            return False, False, "Answer is empty. Please provide a response."
            
        # Check if answer is relevant to the question
        is_relevant, relevance_reason = self.check_relevance(question, answer)
        if not is_relevant:
            state.validation_errors += 1
            return False, False, f"Answer is not relevant to the question. {relevance_reason}"
        
        # Check if we have enough information
        is_complete, completion_reason = self.check_completeness(state)
        
        self.validation_history.append({
            "question": question,
            "answer": answer,
            "relevant": is_relevant,
            "complete": is_complete,
            "timestamp": datetime.now().isoformat()
        })
        
        return True, is_complete, "Answer is valid and relevant."
    
    def check_relevance(self, question, answer):
        system_message = """
        You are a validation agent that determines if an answer is relevant to a question.
        Your goal is to ensure that the answer addresses the specific question asked.
        
        GUIDELINES:
        1. An answer is relevant if it addresses the topic of the question
        2. It can be relevant even if incomplete or partially correct
        3. Answers that indicate "I don't know" or similar are still relevant
        4. Answers that change the subject or avoid the question are not relevant
        5. Consider the context of a process documentation interview
        
        Respond with a JSON object containing:
        - relevant: boolean (true/false)
        - reason: string explaining your reasoning
        """
        
        prompt = f"""
        QUESTION: {question}
        ANSWER: {answer}
        
        Determine if the answer is relevant to the question.
        Provide your response as a JSON object with "relevant" and "reason" fields.
        """
        
        response = call_deepseek(prompt, system_message)
        
        if response:
            try:
                # Try to parse JSON response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result.get("relevant", False), result.get("reason", "No reason provided")
            except json.JSONDecodeError:
                print("Failed to parse JSON response from relevance check")
            except Exception as e:
                print(f"Error in relevance check: {e}")
        
        # Fallback: Simple keyword-based relevance check
        question_keywords = set(question.lower().split())
        answer_keywords = set(answer.lower().split())
        
        # Remove common words
        common_words = {"what", "how", "why", "when", "where", "who", "which", 
                       "the", "a", "an", "is", "are", "do", "does", "can", "could"}
        question_keywords -= common_words
        
        # Check if answer contains any question keywords
        has_overlap = any(keyword in answer_keywords for keyword in question_keywords)
        
        if has_overlap:
            return True, "Answer contains relevant keywords from the question."
        else:
            return False, "Answer does not address the specific question asked."
    
    def check_completeness(self, state):
        system_message = """
        You are a completeness validator for a process documentation interview.
        Your goal is to determine if the conversation contains enough information
        to create a comprehensive process document.
        
        GUIDELINES:
        1. A complete process document should cover: purpose, inputs, tools, steps, exceptions, success criteria
        2. The steps should be detailed enough for someone else to follow
        3. There should be enough information about each relevant aspect
        4. Consider the complexity of the process - simple processes need less detail
        5. The conversation should have sufficient depth and breadth
        
        Respond with a JSON object containing:
        - complete: boolean (true/false)
        - reason: string explaining your reasoning
        """
        
        prompt = f"""
        PROCESS TOPIC: {state.topic}
        
        CONVERSATION HISTORY:
        {state.get_conversation_text()}
        
        Determine if this conversation contains enough information to create a comprehensive process document.
        Consider if all important aspects have been covered with sufficient detail.
        
        Provide your response as a JSON object with "complete" and "reason" fields.
        """
        
        response = call_deepseek(prompt, system_message)
        
        if response:
            try:
                # Try to parse JSON response
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result.get("complete", False), result.get("reason", "No reason provided")
            except json.JSONDecodeError:
                print("Failed to parse JSON response from completeness check")
            except Exception as e:
                print(f"Error in completeness check: {e}")
        
        # Fallback: Rule-based completeness check
        aspects_covered = len(state.covered_aspects)
        interactions = len(state.conversation_history)
        
        # Require at least 5 interactions and coverage of 3+ aspects
        if interactions >= 5 and aspects_covered >= 3:
            return True, f"Covered {aspects_covered} aspects in {interactions} interactions."
        else:
            return False, f"Need more information. Currently {aspects_covered} aspects covered in {interactions} interactions."
    
    def get_validation_stats(self):
        """Get statistics about validation results"""
        total = len(self.validation_history)
        relevant = sum(1 for item in self.validation_history if item["relevant"])
        complete = sum(1 for item in self.validation_history if item["complete"])
        
        return {
            "total_validations": total,
            "relevant_answers": relevant,
            "complete_conversations": complete,
            "relevance_rate": relevant / total if total > 0 else 0,
            "completion_rate": complete / total if total > 0 else 0
        }