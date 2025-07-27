from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
import os
from .models import Document, ChatMessage
from .utils import process_document, extract_text_from_file
from core.ai_service import ai_service


def index(request):
    """Main application view"""
    return render(request, 'index.html')


@api_view(['POST'])
@csrf_exempt
def upload_document(request):
    """Upload and process a document"""
    try:
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        title = request.POST.get('title', file.name)
        document_type = request.POST.get('document_type', 'other')
        
        # Create document record
        document = Document.objects.create(
            title=title,
            file=file,
            document_type=document_type
        )
        
        # Extract text from file
        content = extract_text_from_file(file)
        document.content = content
        document.processed = True
        document.save()
        
        return Response({
            'id': document.id,
            'title': document.title,
            'content': content,
            'message': 'Document uploaded and processed successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_documents(request):
    """Get list of uploaded documents"""
    documents = Document.objects.all()
    data = []
    for doc in documents:
        data.append({
            'id': doc.id,
            'title': doc.title,
            'document_type': doc.document_type,
            'uploaded_at': doc.uploaded_at.isoformat(),
            'processed': doc.processed
        })
    return Response(data)


@api_view(['POST'])
@csrf_exempt
def chat_message(request):
    """Handle chat messages with AI assistant"""
    try:
        data = json.loads(request.body)
        document_id = data.get('document_id')
        message = data.get('message')
        
        if not document_id or not message:
            return Response({'error': 'Document ID and message are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        document = Document.objects.get(id=document_id)
        
        # Save user message
        ChatMessage.objects.create(
            document=document,
            message_type='user',
            content=message
        )
        
        # Generate AI response
        system_prompt = """You are a legal AI assistant for Clausemint. You help users understand legal documents, 
        explain clauses, and provide legal insights. Always be helpful, accurate, and professional."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document content: {document.content}\n\nUser question: {message}"}
        ]
        
        ai_response = ai_service.generate_response(messages, max_tokens=500)
        
        # Save AI response
        ChatMessage.objects.create(
            document=document,
            message_type='assistant',
            content=ai_response
        )
        
        return Response({
            'response': ai_response,
            'document_id': document_id
        })
        
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def chat_message_streaming(request):
    """Handle chat messages with AI assistant using streaming"""
    try:
        data = json.loads(request.body)
        document_id = data.get('document_id')
        message = data.get('message')
        
        if not document_id or not message:
            return Response({'error': 'Document ID and message are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        document = Document.objects.get(id=document_id)
        
        # Save user message
        ChatMessage.objects.create(
            document=document,
            message_type='user',
            content=message
        )
        
        # Generate AI response
        system_prompt = """You are a legal AI assistant for Clausemint. You help users understand legal documents, 
        explain clauses, and provide legal insights. Always be helpful, accurate, and professional."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Document content: {document.content}\n\nUser question: {message}"}
        ]
        
        def generate_chat_stream():
            """Generate streaming chat response"""
            try:
                # Send initial status
                yield f"data: {json.dumps({'status': 'started', 'message': 'AI is thinking...'})}\n\n"
                
                # Generate content using streaming
                ai_response = ai_service.generate_response(messages, max_tokens=500)
                
                # Save AI response
                ChatMessage.objects.create(
                    document=document,
                    message_type='assistant',
                    content=ai_response
                )
                
                # Send the complete response
                yield f"data: {json.dumps({'status': 'completed', 'response': ai_response, 'document_id': document_id})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"
        
        # Return streaming response
        response = StreamingHttpResponse(
            generate_chat_stream(),
            content_type='text/event-stream'
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
        
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_chat_history(request, document_id):
    """Get chat history for a document"""
    try:
        document = Document.objects.get(id=document_id)
        messages = document.chat_messages.all()
        
        data = []
        for msg in messages:
            data.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            })
        
        return Response(data)
        
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND) 