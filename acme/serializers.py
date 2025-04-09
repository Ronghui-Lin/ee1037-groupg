from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ticket, TicketComment, TicketAttachment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ['id', 'filename', 'file', 'uploaded_at']

class TicketCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = TicketComment
        fields = ['id', 'author', 'content', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    attachments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'subject', 'description', 'status', 
            'priority', 'created_by', 'assigned_to', 
            'created_at', 'last_updated', 'comments_count',
            'attachments_count'
        ]
    
    def get_comments_count(self, obj):
        return obj.comments.count()
        
    def get_attachments_count(self, obj):
        return obj.attachments.count()

class TicketDetailSerializer(TicketSerializer):
    comments = TicketCommentSerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    
    class Meta(TicketSerializer.Meta):
        fields = TicketSerializer.Meta.fields + ['comments', 'attachments']