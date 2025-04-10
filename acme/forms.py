from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Ticket, TicketComment, TicketAttachment
from django.contrib.auth.models import User
from django import forms
from .models import Ticket, Machine, TicketAttachment, TicketComment

class TicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        help_text="Assign this ticket to a superuser"
    )
    machine = forms.ModelChoiceField(
        queryset=Machine.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        help_text="Select the machine associated with this issue"
    )
    
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 3, 
            'placeholder': 'Add comments or additional information'
        }),
        required=False,
        help_text='Optional: Add details about this ticket'
    )
    
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control', 
            'multiple': False
        }),
        required=False,
        help_text='Upload relevant files or screenshots'
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        
        self.fields['machine'].queryset = Machine.objects.all().order_by('name')
        
        if self.instance.pk:
            self.fields['status'].initial = self.instance.status
        # else:
        #     # For new tickets, hide the assigned_to field (admins will handle assignment)
        #     if 'assigned_to' in self.fields:
        #         self.fields['assigned_to'].widget = forms.HiddenInput()
    
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'priority', 'status', 'machine', 'assigned_to']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Brief summary of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 5, 
                'placeholder': 'Please provide all details about your issue'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'priority': 'Set the urgency of this support request',
            'status': 'Current status of the ticket',
        }
    
    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        
        if not ticket.pk and self.user:
            ticket.created_by = self.user
        
        if commit:
            ticket.save()
            
            # Save comment if provided
            comment_text = self.cleaned_data.get('comment')
            if comment_text:
                TicketComment.objects.create(
                    ticket=ticket,
                    author=self.user,
                    content=comment_text
                )
            
            # Save attachments if provided
            files = self.files.getlist('attachments')
            for file in files:
                TicketAttachment.objects.create(
                    ticket=ticket,
                    file=file,
                    filename=file.name
                )
        
        return ticket

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class TicketAttachmentForm(forms.ModelForm):
    file = MultipleFileField(label='Files', required=False)

    class Meta:
        model = TicketAttachment
        fields = ['file'] 

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment or update'}),
        }
        labels = {
            'content': 'Comment'
        }

class TicketStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    attachment = forms.FileField(required=False)

    class Meta:
        model = TicketComment
        fields = ['content']
