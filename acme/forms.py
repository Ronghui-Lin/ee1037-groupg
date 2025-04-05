from django import forms
from .models import Ticket, Machine # import Machine model

class TicketForm(forms.ModelForm):
    machine = forms.ModelChoiceField(
        queryset=Machine.objects.all().order_by('name'), # Get all machines
        required=False, # optional in the form
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="-- Select Machine (Optional) --", # placeholder
        help_text="Choose the machine related to this issue, if any."
    )

    class Meta:
        model = Ticket
        # Add 'category' and 'machine' to the fields list
        fields = ['subject', 'description', 'category', 'priority', 'machine', 'attachment']

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Machine XYZ not starting'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the issue in detail, including steps to reproduce if possible.'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

        labels = {
            'subject': 'Subject / Issue Title',
            'description': 'Detailed Description',
            'priority': 'Priority Level',
            'category': 'Issue Category',
            'machine': 'Related Machine',
            'attachment': 'Attach File (Optional)'
        }

        help_texts = {
            'priority': 'Select the urgency of this issue.',
            'category': 'Choose the most relevant category for your issue.',
            'attachment': 'You can attach a screenshot, log file, or other relevant document.'
        }