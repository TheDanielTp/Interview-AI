from ollama_helper import call_ollama

class InterviewerAgent:
    def generate_question(self, state):
        if state.topic is None:
            return "What is the process you would like to describe?"

        conversation_text = state.get_conversation_text()
        prompt = f"""
        You are an expert interviewer conducting a step-by-step interview to document a process. The process is: {state.topic}

        Here is the conversation so far:
        {conversation_text}

        Your task is to ask only one specific question that will help extract the next piece of information needed to document the process. Do not ask broad questions that cover multiple aspects. Instead, focus on one aspect at a time, such as:
        - Ingredients or materials needed
        - Tools or equipment required
        - Step-by-step instructions
        - Timing or durations
        - Conditions or prerequisites
        - Safety precautions
        - Common mistakes or troubleshooting

        Based on what has already been covered, determine what information is still missing and ask a question to get that information. Make sure your question is clear and concise.

        Generate only the question without any additional text.
        """
        question = call_ollama(prompt)
        if question is None:
            return "Can you tell me more about the process?"
        return question.strip()