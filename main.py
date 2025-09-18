from state import ProcessState
from interviewer import InterviewerAgent
from validator import ValidatorAgent
from data_extractor import DataExtractorAgent

def main():
    state = ProcessState()
    interviewer = InterviewerAgent()
    validator = ValidatorAgent()
    extractor = DataExtractorAgent()

    print("Interviewer: What is the process you would like to describe?")
    topic = input("You: ").strip()
    if not topic:
        print("Error: Process topic cannot be empty.")
        return
    state.set_topic(topic)
    state.add_interaction("What is the process you would like to describe?", topic)

    while not state.is_complete:
        question = interviewer.generate_question(state)
        print(f"Interviewer: {question}")
        answer = input("You: ").strip()
        state.add_interaction(question, answer)

        enough = validator.validate_answer(state)

        if enough:
            state.is_complete = True

    print("\nWe have enough information. Now extracting the process...")
    
    print("\nSummary of collected information:")
    for i, (question, answer) in enumerate(state.conversation_history):
        if i > 0:
            print(f"Q: {question}")
            print(f"A: {answer}\n")
    
    document = extractor.extract_process(state)
    print("\nFinal Process Document:")
    print(document)
    
    save = input("\nWould you like to save this document? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"{state.topic.replace(' ', '_')}_process.md"
        with open(filename, 'w') as f:
            f.write(document)
        print(f"Document saved as {filename}")

if __name__ == "__main__":
    main()