import re
from core.ai_service import ai_service


def extract_clauses(document_content):
    """Extract clauses from document content"""
    # Simple clause extraction - split by common legal section markers
    clause_patterns = [
        r'\d+\.\s*[A-Z][^.]*\.',  # Numbered clauses
        r'[A-Z][^.]*\.',  # Sentences starting with capital letters
        r'WHEREAS[^.]*\.',  # Whereas clauses
        r'PROVIDED[^.]*\.',  # Provided clauses
        r'FURTHER[^.]*\.',  # Further clauses
    ]
    
    clauses = []
    for pattern in clause_patterns:
        matches = re.findall(pattern, document_content, re.MULTILINE | re.DOTALL)
        clauses.extend(matches)
    
    # If no clauses found with patterns, split by sentences
    if not clauses:
        sentences = re.split(r'[.!?]+', document_content)
        clauses = [s.strip() for s in sentences if len(s.strip()) > 20]  # Filter short sentences
    
    return clauses


def analyze_clause(clause_text, clause_type='general'):
    """Analyze a single clause using AI"""
    try:
        system_prompt = """You are a legal reviewer specializing in clause analysis. Analyze the following clause and classify it:
- Red: Unfair, risky, or problematic clauses
- Amber: Ambiguous, unusual, or clauses that need review
- Green: Standard, fair, and acceptable clauses

Then provide:
1. Risk level (red/amber/green)
2. Brief explanation of the classification
3. Suggested improvements if red or amber
4. Confidence score (0-100)

Format your response as JSON:
{
    "risk_level": "red|amber|green",
    "explanation": "brief explanation",
    "suggestions": "improvement suggestions",
    "confidence": 85
}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this clause: {clause_text}"}
        ]
        
        ai_response = ai_service.generate_response(messages, max_tokens=500, temperature=0.3)
        
        # Try to extract JSON from response
        try:
            import json
            analysis = json.loads(ai_response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis = {
                'risk_level': 'amber',
                'explanation': 'Unable to parse AI response',
                'suggestions': 'Manual review recommended',
                'confidence': 50
            }
        
        return analysis
        
    except Exception as e:
        # Fallback analysis
        return {
            'risk_level': 'amber',
            'explanation': f'Analysis failed: {str(e)}',
            'suggestions': 'Manual review recommended',
            'confidence': 0
        }


def get_clause_type(clause_text):
    """Determine the type of clause based on content"""
    clause_text_lower = clause_text.lower()
    
    if any(word in clause_text_lower for word in ['confidential', 'secret', 'proprietary']):
        return 'confidentiality'
    elif any(word in clause_text_lower for word in ['indemnify', 'indemnification', 'liability']):
        return 'indemnity'
    elif any(word in clause_text_lower for word in ['intellectual property', 'ip', 'patent', 'copyright']):
        return 'ip'
    elif any(word in clause_text_lower for word in ['terminate', 'termination', 'end']):
        return 'termination'
    elif any(word in clause_text_lower for word in ['governing law', 'jurisdiction', 'venue']):
        return 'governing_law'
    else:
        return 'general' 