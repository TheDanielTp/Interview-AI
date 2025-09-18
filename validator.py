from ollama_helper import call_ollama

class ValidatorAgent:
    def __init__(self):
        self.validation_attempts = {}
    
    def validate_answer(self, state):
        enough = self.check_completeness(state)
        return enough
    
    def check_completeness(self, state):
        # Check if we have enough information to document the process
        conversation_text = state.get_conversation_text()
        
        # Require a minimum number of interactions
        if len(state.conversation_history) < 5:
            return False
        
        prompt = f"""
        Attention: You're being used for an API call.
        You are validating whether the following conversation about the process "{state.topic}" has enough information to create a complete and consistent process document that others could follow.

        The process document should include:
        - The purpose of the process.
        - Inputs and outputs.
        - Tools or resources required.
        - Step-by-step instructions.
        - Actors (who performs the process).
        - Exceptions and how to handle them.
        - Preconditions (what must be true before starting).
        - Postconditions (what will be true after).
        - Success criteria.
        - Examples if available.

        Conversation history:
        {conversation_text}

        Based on the above, does the conversation contain sufficient details for each of the above aspects?
        Note: The conversation should contain details about each aspect ONLY if it is applicable to the process.
        Note: Some aspects might not be applicable to every process, but we have to cover the applicable ones.

        Answer with only 'yes' or 'no'.
        """
        
        response = call_ollama(prompt)
        return response and response.strip().lower().startswith('yes')