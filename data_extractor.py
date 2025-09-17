from ollama_helper import call_ollama

class DataExtractorAgent:
    def extract_process(self, state):
        conversation_text = state.get_conversation_text()
        prompt = f"""
        You are a technical writer. Your task is to create a structured process document based on the following conversation about the process: {state.topic}
        Conversation:
        {conversation_text}
        Create a clear, step-by-step guide that others could follow consistently. Include ingredients, tools, and steps. Format the output in a markdown-like structure.
        """
        document = call_ollama(prompt)
        if document is None:
            return "Error: Unable to generate document."
        return document