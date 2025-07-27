from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import json
from .ai_service import ai_service
from .jurisdictions import get_jurisdictions_list, get_default_jurisdiction, get_jurisdiction_details


@api_view(['GET'])
def ai_status(request):
    """Get current AI provider status and test connection"""
    try:
        current_provider = ai_service.get_current_provider()
        connection_test = ai_service.test_connection()
        
        return Response({
            'current_provider': current_provider,
            'connection_status': connection_test
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def switch_ai_provider(request):
    """Switch between AI providers"""
    try:
        data = json.loads(request.body)
        provider = data.get('provider', 'mistral')
        
        if provider not in ['mistral', 'openai']:
            return Response({
                'error': 'Provider must be "mistral" or "openai"'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        result = ai_service.switch_provider(provider)
        connection_test = ai_service.test_connection()
        
        return Response({
            'message': result,
            'current_provider': provider,
            'connection_status': connection_test
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def test_ai_connection(request):
    """Test connection to current AI provider"""
    try:
        connection_test = ai_service.test_connection()
        return Response(connection_test)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def jurisdictions(request):
    """Get list of available jurisdictions"""
    try:
        jurisdictions_list = get_jurisdictions_list()
        default_jurisdiction = get_default_jurisdiction()
        
        return Response({
            'jurisdictions': jurisdictions_list,
            'default': default_jurisdiction
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def jurisdiction_details(request, jurisdiction_name):
    """Get detailed information about a specific jurisdiction"""
    try:
        details = get_jurisdiction_details(jurisdiction_name)
        if details:
            return Response(details)
        else:
            return Response({'error': 'Jurisdiction not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 