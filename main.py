# main.py
from state import ProcessState
from interviewer import InterviewerAgent
from validator import ValidatorAgent
from data_extractor import DataExtractorAgent
import os

def main():
    state = ProcessState()
    interviewer = InterviewerAgent()
    validator = ValidatorAgent()
    extractor = DataExtractorAgent()
    
    if os.path.exists("interview_state.json"):
        load = input("Found a previous interview state. Load it? (y/n): ").lower()
        if load == 'y':
            state.load_state("interview_state.json")
            print(f"Loaded previous state for: {state.topic}")
    
    if state.topic is None:
        print("Interviewer: What is the process you would like to describe?")
        topic = input("You: ").strip()
        if not topic:
            print("Error: Process topic cannot be empty.")
            return
        state.set_topic(topic)
        state.add_interaction("What is the process you would like to describe?", topic)
    
    max_questions = 20
    question_count = len(state.conversation_history) - 1
    
    print(f"\nStarting interview about: {state.topic}")
    print("Type 'exit' at any time to end the interview early.\n")
    
    while not state.is_complete and question_count < max_questions:
        question = interviewer.generate_question(state)
        
        if "thank you" in question.lower() or "enough information" in question.lower():
            state.is_complete = True
            print(f"Interviewer: {question}")
            break
            
        print(f"Interviewer: {question}")
        answer = input("You: ").strip()
        
        if answer.lower() in ['exit', 'quit', 'stop', 'end']:
            print("Interview ended by user.")
            break
        
        valid, complete, reason = validator.validate_answer(state, question, answer)
        
        if not valid:
            print(f"Validation: {reason}")
            continue
            
        state.add_interaction(question, answer)
        question_count += 1
        
        if question_count % 3 == 0:
            state.save_state("interview_state.json")
        
        if complete:
            state.is_complete = True
            print("Interviewer: Thank you, I have enough information to document this process.")
    
    if state.conversation_history:
        print("\nWe have enough information. Now extracting the process...")
        
        print("\nConversation Summary:")
        for i, (q, a) in enumerate(state.conversation_history):
            if i > 0:
                print(f"{i}. Q: {q}")
                print(f"   A: {a}\n")
        
        document = extractor.extract_process(state)
        
        print("\n" + "="*60)
        print("FINAL PROCESS DOCUMENT")
        print("="*60)
        print(document)
        print("="*60)
        
        save = input("\nWould you like to save this document? (y/n): ").lower()
        if save == 'y':
            filename = f"{state.topic.replace(' ', '_')}_process.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(document)
            print(f"Document saved as {filename}")
            
        save_state = input("Would you like to save the interview state for later? (y/n): ").lower()
        if save_state == 'y':
            state.save_state("interview_state.json")
            print("Interview state saved.")
    else:
        print("No conversation history to process.")
    
    print("\nInterview completed. Thank you!")

if __name__ == "__main__":
    main()