from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
import json
from core.ai_service import ai_service
from .utils import analyze_clause, extract_clauses


@api_view(['POST'])
@csrf_exempt
def analyze_document(request):
    """Analyze document for clause redlining and RAG review"""
    try:
        data = json.loads(request.body)
        document_content = data.get('content', '')
        
        if not document_content:
            return Response({'error': 'Document content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract clauses from document
        clauses = extract_clauses(document_content)
        
        # Analyze each clause
        analysis_results = []
        for i, clause in enumerate(clauses):
            if clause.strip():  # Skip empty clauses
                analysis = analyze_clause(clause)
                analysis['clause_id'] = i
                analysis['clause_text'] = clause
                analysis_results.append(analysis)
        
        # Generate summary
        summary = generate_analysis_summary(analysis_results)
        
        return Response({
            'analysis': analysis_results,
            'summary': summary,
            'total_clauses': len(analysis_results)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def analyze_document_streaming(request):
    """Analyze document for clause redlining and RAG review with streaming"""
    try:
        data = json.loads(request.body)
        document_content = data.get('content', '')
        
        if not document_content:
            return Response({'error': 'Document content is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        def generate_analysis_stream():
            """Generate streaming analysis response"""
            try:
                # Send initial status
                yield f"data: {json.dumps({'status': 'started', 'message': 'Starting document analysis...'})}\n\n"
                
                # Extract clauses from document
                clauses = extract_clauses(document_content)
                yield f"data: {json.dumps({'status': 'progress', 'message': f'Found {len(clauses)} clauses to analyze...'})}\n\n"
                
                # Analyze each clause
                analysis_results = []
                for i, clause in enumerate(clauses):
                    if clause.strip():  # Skip empty clauses
                        yield f"data: {json.dumps({'status': 'progress', 'message': f'Analyzing clause {i+1}/{len(clauses)}...'})}\n\n"
                        analysis = analyze_clause(clause)
                        analysis['clause_id'] = i
                        analysis['clause_text'] = clause
                        analysis_results.append(analysis)
                
                # Generate summary
                yield f"data: {json.dumps({'status': 'progress', 'message': 'Generating analysis summary...'})}\n\n"
                summary = generate_analysis_summary(analysis_results)
                
                # Send the complete results
                yield f"data: {json.dumps({'status': 'completed', 'analysis': analysis_results, 'summary': summary, 'total_clauses': len(analysis_results)})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"
        
        # Return streaming response
        response = StreamingHttpResponse(
            generate_analysis_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def analyze_single_clause(request):
    """Analyze a single clause"""
    try:
        data = json.loads(request.body)
        clause_text = data.get('clause_text', '')
        clause_type = data.get('clause_type', 'general')
        
        if not clause_text:
            return Response({'error': 'Clause text is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        analysis = analyze_clause(clause_text, clause_type)
        
        return Response({
            'analysis': analysis,
            'clause_text': clause_text
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_analysis_summary(analysis_results):
    """Generate a summary of the analysis results"""
    red_count = sum(1 for result in analysis_results if result['risk_level'] == 'red')
    amber_count = sum(1 for result in analysis_results if result['risk_level'] == 'amber')
    green_count = sum(1 for result in analysis_results if result['risk_level'] == 'green')
    
    summary = {
        'total_clauses': len(analysis_results),
        'red_clauses': red_count,
        'amber_clauses': amber_count,
        'green_clauses': green_count,
        'risk_percentage': round((red_count + amber_count) / len(analysis_results) * 100, 1) if analysis_results else 0
    }
    
    return summary 