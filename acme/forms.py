from django import forms
from django.forms.widgets import ClearableFileInput
from .models import Ticket, TicketComment, TicketAttachment
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
from .models import Ticket, Machine, TicketAttachment, TicketComment
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from .models import Machine 

class TicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True), # assign ticketes 
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        help_text="Assign this ticket to a a staff member"
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


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'serial_number', 'model', 'last_maintenance', 'installation_date', 'next_maintenance', 'status', 'location', 'description']

    def clean_next_maintenance(self):
        next_maintenance = self.cleaned_data.get('next_maintenance')
        if next_maintenance and next_maintenance < timezone.now().date():
            raise forms.ValidationError("Next maintenance date cannot be in the past.")
        return next_maintenance

    def clean_last_maintenance(self):
        last_maintenance = self.cleaned_data.get('last_maintenance')
        if last_maintenance and last_maintenance > timezone.now().date():
            raise forms.ValidationError("Last maintenance date cannot be in the future.")
        return last_maintenance

    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('installation_date')
        if purchase_date and purchase_date > timezone.now().date():
            raise forms.ValidationError("Purchase date cannot be in the future.")
        return purchase_date
    
class CustomUserCreationForm(UserCreationForm):
    # Add widgets for styling
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(required=False, initial=False, label="Staff Access", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_superuser = forms.BooleanField(required=False, initial=False, label="Superuser Access", widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    # new Role Field
    role = forms.CharField(
        max_length=100,
        required=False,
        label="Role/Designation",
        help_text="Enter the user's job title.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name", "is_staff", "is_superuser")

    def save(self, commit=True):
        user = super().save(commit=False) # Don't commit user yet
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data.get("is_staff", False)
        user.is_superuser = self.cleaned_data.get("is_superuser", False)

        # Get role data
        role_data = self.cleaned_data.get("role", None)

        if commit:
            user.save() # Save user FIRST

            # Save role data AFTER user save
            if role_data is not None:
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'role': role_data}
                )
        return user

class UserEditForm(forms.Form):
    """
    Form for Superusers to edit limited fields (Active Status, Role)
    of existing users on the account management page.
    """
    is_active = forms.BooleanField(
        required=False, # Needs to be False so unchecking it works
        label="User is Active", # Label for the form field
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}) # Basic Bootstrap styling
        )
    role = forms.CharField(
        max_length=100,
        required=False, # Role can be optional/cleared
        label="Role/Designation",
        help_text="Update the user's job title or designation.", # Help text
        widget=forms.TextInput(attrs={'class': 'form-control'}) # Basic Bootstrap styling
        )