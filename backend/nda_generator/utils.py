import os
from pathlib import Path


def load_nda_prompt():
    """Load the comprehensive NDA prompt template"""
    # Try to load the comprehensive template generator prompt
    template_path = Path(__file__).parent.parent / 'prompts' / 'nda' / 'template_generator.txt'
    system_path = Path(__file__).parent.parent / 'prompts' / 'nda' / 'system_prompt.txt'
    
    try:
        # Load the main template generator prompt
        with open(template_path, 'r', encoding='utf-8') as f:
            template_prompt = f.read()
        
        # Load the system prompt for additional context
        if system_path.exists():
            with open(system_path, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            return f"{system_prompt}\n\n{template_prompt}"
        else:
            return template_prompt
            
    except Exception as e:
        # Return enhanced default prompt if files don't exist
        return """You are an expert legal document generator specializing in Non-Disclosure Agreements (NDAs). You have extensive experience in corporate law, intellectual property protection, and contract drafting.

## Your Role and Expertise:
- Generate legally sound, comprehensive NDA agreements
- Ensure compliance with relevant jurisdiction laws
- Use precise legal terminology and structure
- Adapt language based on the type of NDA and parties involved
- Include all necessary clauses for comprehensive protection

## Document Structure Requirements:
1. **Header Section**: Document title, date, and party identification
2. **Recitals**: Purpose and context of the agreement
3. **Definitions**: Clear definition of confidential information and key terms
4. **Confidentiality Obligations**: Detailed non-disclosure requirements
5. **Permitted Disclosures**: Exceptions and authorized disclosures
6. **Term and Termination**: Duration and termination conditions
7. **Return of Materials**: Obligations upon termination
8. **Remedies and Enforcement**: Legal remedies for breaches
9. **General Provisions**: Standard contract terms
10. **Signature Blocks**: Proper execution format

## Input Parameters:
- **Parties**: {party_a}, {party_b}, {party_c}
- **NDA Type**: {nda_type}
- **Purpose**: {purpose}
- **Duration**: {confidentiality_period}
- **Jurisdiction**: {jurisdiction}

Generate a comprehensive, legally sound NDA agreement based on these parameters. Include all standard NDA sections with professional legal language and structure.""" 