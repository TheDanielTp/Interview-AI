# data_extractor.py
from ai_helper import call_deepseek
import re

class DataExtractorAgent:
    def extract_process(self, state):
        conversation_text = state.get_conversation_text()
        
        system_message = """
        You are an expert technical writer specializing in process documentation.
        Your goal is to create a comprehensive, structured process document from an interview conversation.
        
        GUIDELINES:
        1. Use ONLY information explicitly provided in the conversation
        2. Do not add any external knowledge or assumptions
        3. Organize information logically with clear section headings
        4. Use consistent terminology from the conversation
        5. Write in clear, imperative language
        6. Make instructions actionable and specific
        7. Include all relevant details from the conversation
        8. Omit sections that lack information in the conversation
        
        DOCUMENT STRUCTURE:
        - Process Name and Overview
        - Purpose and Objectives
        - Scope and Limitations
        - Input Requirements
        - Output Specifications
        - Tools/Equipment Needed
        - Step-by-Step Instructions
        - Quality Criteria
        - Roles and Responsibilities
        - Common Issues and Solutions
        - Preconditions and Postconditions
        
        Format the document using Markdown with appropriate headings.
        """
        
        prompt = f"""
        Create a comprehensive process document from the following interview conversation.
        
        PROCESS TOPIC: {state.topic}
        
        CONVERSATION HISTORY:
        {conversation_text}
        
        Generate a well-structured process document that includes all relevant information from the conversation.
        Use Markdown formatting with appropriate headings and sections.
        
        DOCUMENT:
        """
        
        document = call_deepseek(prompt, system_message)
        
        if not document:
            return self.create_fallback_document(conversation_text, state.topic)
        
        # Enhance the document with strict formatting
        return self.enhance_document(document, conversation_text, state.topic)
    
    def enhance_document(self, document, conversation_text, topic):
        """
        Apply strict formatting rules to ensure document quality
        """
        # Ensure proper header
        if not document.startswith('# '):
            document = f"# Process: {topic}\n\n{document}"
        
        # Ensure all sections have proper Markdown headers
        sections = [
            "## Purpose", "## Scope", "## Input", "## Output", 
            "## Tools", "## Steps", "## Quality", "## Roles",
            "## Issues", "## Preconditions", "## Postconditions"
        ]
        
        for section in sections:
            if section.lower() in document.lower() and f"#{section}" not in document:
                # Add proper header formatting
                document = document.replace(section, f"#{section}")
        
        # Remove any hallucinated content not in the conversation
        lines = document.split('\n')
        filtered_lines = []
        conversation_lower = conversation_text.lower()
        
        for line in lines:
            # Keep all headers
            if line.startswith('#'):
                filtered_lines.append(line)
                continue
                
            # Keep lines that reference conversation content
            line_lower = line.lower()
            if (len(line.strip()) > 0 and 
                (any(word in conversation_lower for word in line_lower.split() if len(word) > 5) or
                 len(line.strip().split()) < 5)):  # Keep short lines (likely headers)
                filtered_lines.append(line)
        
        enhanced_doc = '\n'.join(filtered_lines)
        
        # If we filtered out too much, use the original
        if len(enhanced_doc.split('\n')) < 10:
            return document
            
        return enhanced_doc
    
    def create_fallback_document(self, conversation_text, topic):
        """
        Create a basic document when the API call fails
        """
        document = f"# Process: {topic}\n\n"
        
        # Extract information by simple text analysis
        lines = conversation_text.split('\n')
        current_section = ""
        
        for line in lines:
            if "purpose" in line.lower() or "why" in line.lower():
                current_section = "## Purpose"
                document += f"{current_section}\n"
            elif "input" in line.lower() or "material" in line.lower():
                current_section = "## Input Requirements"
                document += f"\n{current_section}\n"
            elif "tool" in line.lower() or "equipment" in line.lower():
                current_section = "## Tools/Equipment Needed"
                document += f"\n{current_section}\n"
            elif "step" in line.lower() or "instruction" in line.lower():
                current_section = "## Step-by-Step Instructions"
                document += f"\n{current_section}\n"
            elif line.startswith("Answer:"):
                content = line.replace("Answer:", "").strip()
                if current_section and content:
                    document += f"- {content}\n"
        
        return document
    
    def validate_document_quality(self, document, conversation_text):
        """
        Validate that the document only contains information from the conversation
        """
        doc_lines = document.split('\n')
        conversation_words = set(conversation_text.lower().split())
        
        valid_lines = []
        for line in doc_lines:
            if line.startswith('#') or len(line.strip()) == 0:
                valid_lines.append(line)
                continue
                
            # Check if line contains words from conversation
            line_words = set(line.lower().split())
            if line_words.intersection(conversation_words):
                valid_lines.append(line)
        
        return '\n'.join(valid_lines)