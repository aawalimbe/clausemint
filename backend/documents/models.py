from django.db import models
from django.utils import timezone


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('nda', 'NDA'),
        ('contract', 'Contract'),
        ('agreement', 'Agreement'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed = models.BooleanField(default=False)
    content = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-uploaded_at']


class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chat_messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['timestamp'] 