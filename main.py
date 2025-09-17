from state import ProcessState
from interviewer import InterviewerAgent
from validator import ValidatorAgent
from data_extractor import DataExtractorAgent

def main():
    state = ProcessState()
    interviewer = InterviewerAgent()
    validator = ValidatorAgent()
    extractor = DataExtractorAgent()

    # Get the topic
    print("Interviewer: What is the process you would like to describe?")
    topic = input("You: ").strip()
    if not topic:
        print("Error: Process topic cannot be empty.")
        return
    state.set_topic(topic)
    state.add_interaction("What is the process you would like to describe?", topic)

    # Ask questions until enough info
    while not state.is_complete:
        question = interviewer.generate_question(state)
        print(f"Interviewer: {question}")
        answer = input("You: ").strip()
        state.add_interaction(question, answer)

        valid, enough, reason = validator.validate_answer(state, question, answer)
        if not valid:
            print(f"Validator: The answer was not valid. Reason: {reason}. Please try again.")
            state.conversation_history.pop()  # Remove the invalid interaction
            continue

        if enough:
            state.is_complete = True
        else:
            print("Validator: Need more information. Continuing...")

    # Extract the process
    print("\nWe have enough information. Now extracting the process...")
    document = extractor.extract_process(state)
    print("\nFinal Process Document:")
    print(document)

if __name__ == "__main__":
    main()