import docx2txt
import os
from django.core.files.uploadedfile import UploadedFile


def extract_text_from_file(file: UploadedFile) -> str:
    """Extract text from uploaded file (DOCX only for now)"""
    try:
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension == '.docx':
            return extract_text_from_docx(file)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}. Please upload a DOCX file.")
            
    except Exception as e:
        raise Exception(f"Error extracting text from file: {str(e)}")


def extract_text_from_docx(file: UploadedFile) -> str:
    """Extract text from DOCX file using docx2txt"""
    try:
        text = docx2txt.process(file)
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX: {str(e)}")


def process_document(document_content: str) -> dict:
    """Process document content for analysis"""
    # This function can be extended for more advanced document processing
    # For now, it returns basic document statistics
    lines = document_content.split('\n')
    words = document_content.split()
    
    return {
        'line_count': len(lines),
        'word_count': len(words),
        'character_count': len(document_content),
        'content': document_content
    } 