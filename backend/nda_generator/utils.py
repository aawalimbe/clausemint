import os
from pathlib import Path


def load_nda_prompt():
    """Load the NDA prompt template"""
    prompt_path = Path(__file__).parent.parent / 'prompts' / 'nda' / 'base_prompt.txt'
    
    if not prompt_path.exists():
        # Return default prompt if file doesn't exist
        return """You are a legal assistant generating an NDA agreement. Format the output in legal English. Use the following inputs to construct the NDA:
- Parties: {party_a}, {party_b}, {party_c}
- Type: {nda_type}
- Purpose: {purpose}
- Duration: {confidentiality_period}
- Jurisdiction: {jurisdiction}

Generate a comprehensive, legally sound NDA agreement based on these parameters."""
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        # Return default prompt if there's an error reading the file
        return """You are a legal assistant generating an NDA agreement. Format the output in legal English. Use the following inputs to construct the NDA:
- Parties: {party_a}, {party_b}, {party_c}
- Type: {nda_type}
- Purpose: {purpose}
- Duration: {confidentiality_period}
- Jurisdiction: {jurisdiction}

Generate a comprehensive, legally sound NDA agreement based on these parameters.""" 