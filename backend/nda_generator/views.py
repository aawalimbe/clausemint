from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.conf import settings
from .utils import load_nda_prompt


@api_view(['POST'])
@csrf_exempt
def generate_nda(request):
    """Generate NDA document using AI"""
    try:
        data = json.loads(request.body)
        
        # Extract NDA parameters
        party_a = data.get('party_a', '')
        party_b = data.get('party_b', '')
        party_c = data.get('party_c', '')
        nda_type = data.get('nda_type', 'two-way')
        purpose = data.get('purpose', '')
        confidentiality_period = data.get('confidentiality_period', '2 years')
        jurisdiction = data.get('jurisdiction', 'United States')
        
        # Validate required fields
        if not party_a or not party_b or not purpose:
            return Response({
                'error': 'Party A, Party B, and Purpose are required fields'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Load the NDA prompt template
        prompt_template = load_nda_prompt()
        
        # Format the prompt with user inputs
        formatted_prompt = prompt_template.format(
            party_a=party_a,
            party_b=party_b,
            party_c=party_c if party_c else 'N/A',
            nda_type=nda_type,
            purpose=purpose,
            confidentiality_period=confidentiality_period,
            jurisdiction=jurisdiction
        )
        
        # Generate NDA using OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal document generator specializing in NDA agreements. Generate professional, legally sound documents."},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        nda_content = response.choices[0].message.content
        
        return Response({
            'nda_content': nda_content,
            'parameters': {
                'party_a': party_a,
                'party_b': party_b,
                'party_c': party_c,
                'nda_type': nda_type,
                'purpose': purpose,
                'confidentiality_period': confidentiality_period,
                'jurisdiction': jurisdiction
            }
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def export_nda(request):
    """Export NDA as DOCX file"""
    try:
        data = json.loads(request.body)
        nda_content = data.get('nda_content', '')
        
        if not nda_content:
            return Response({'error': 'NDA content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # This would typically generate a DOCX file
        # For now, return the content for frontend to handle
        return Response({
            'content': nda_content,
            'format': 'docx',
            'filename': 'generated_nda.docx'
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 