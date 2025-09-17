class ProcessState:
    def __init__(self):
        self.topic = None
        self.conversation_history = []  # list of dicts: {'question': '', 'answer': ''}
        self.is_complete = False

    def set_topic(self, topic):
        self.topic = topic

    def add_interaction(self, question, answer):
        self.conversation_history.append({'question': question, 'answer': answer})

    def get_conversation_text(self):
        text = ""
        for interaction in self.conversation_history:
            text += f"Question: {interaction['question']}\nAnswer: {interaction['answer']}\n"
        return text