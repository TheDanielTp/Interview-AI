from ollama_helper import call_ollama

class ValidatorAgent:
    def validate_answer(self, state, question, answer):
        if answer.strip() == "":
            return False, False, "Answer is empty."

        conversation_text = state.get_conversation_text()
        prompt = f"""
        You are validating the information gathered for documenting the process: {state.topic}

        Conversation history:
        {conversation_text}

        Latest question: {question}
        Latest answer: {answer}

        Evaluate the following:
        1. Is the answer valid and relevant to the question? (yes/no)
        2. Based on the entire conversation, do we have enough information to create a complete process document? Consider if we have:
           - List of all ingredients/materials
           - List of all tools/equipment
           - Detailed step-by-step instructions
           - Timing information where relevant
           - Any other necessary details

        Respond exactly in the format:
        VALID: yes|no
        ENOUGH: yes|no
        """
        response = call_ollama(prompt)
        if response is None:
            return True, False, "Error in validation."

        valid_str = None
        enough_str = None
        lines = response.split('\n')
        for line in lines:
            if line.startswith("VALID:"):
                valid_str = line.split(":")[1].strip().lower()
            elif line.startswith("ENOUGH:"):
                enough_str = line.split(":")[1].strip().lower()
        
        valid = valid_str == 'yes' if valid_str else False
        enough = enough_str == 'yes' if enough_str else False
        return valid, enough, response