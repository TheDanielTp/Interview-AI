from ai_helper import call_ai

class DataExtractorAgent:
    def extract_process(self, state):
        conversation_text = state.get_conversation_text()
        
        document_prompt = f"""
        Attention: You're being used for an API call.
        Create a comprehensive process document based on this conversation going on between an AI interviewer and a human user:
        {conversation_text}
        
        Process: {state.topic}
        
        Structure the document with these sections (use markdown):
        # Process: {state.topic}
        
        ## Purpose
        [Clear statement of why this process exists]
        
        ## Inputs/Materials
        [Bulleted list of all required items]
        
        ## Tools/Equipment
        [Bulleted list of all tools needed]
        
        ## Step-by-Step Instructions
        [Numbered list of specific actions]
        
        ## Timing/Temperature
        [Any specific measurements mentioned]
        
        ## Success Criteria
        [How to determine if the process was successful]
        
        ## Notes/Exceptions
        [Any special considerations or potential issues]
        
        Guidelines:
        - Use only the information provided by the user in the conversation. Do NOT add any additional information by yourself.
        - Write only the sections that are contained in the conversation. If there's no info about a section, remove it.
        - Write in clear, imperative language
        - Be specific and actionable
        - Organize steps chronologically
        - Use consistent terminology
        """
        
        document = call_ai(document_prompt)
        if document is None:
            return "Error: Unable to generate document."
        
        return document