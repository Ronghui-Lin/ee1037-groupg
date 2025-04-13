from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


import os

def ticket_attachment_path(instance, filename):
    ticket_id_str = str(instance.id) if instance.id else f"unsaved_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    return os.path.join('ticket_attachments', f'ticket_{ticket_id_str}', filename)

# --- Machine Model, remove parts we dont need---
class Machine(models.Model):
    """ a piece of machinery in the facility. """
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('warning', 'Warning'),
        ('fault', 'Fault'),
    ]
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name or identifier for the machine"
    )
    location = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Physical location of the machine (e.g., 'Shop Floor A', 'Building 2')."
    )
    model = models.CharField(
        max_length=100,
        unique=True,
        help_text="Model Name for the machine"
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name or identifier for the machine"
    )
    last_maintenance = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    installation_date = models.DateField()
    last_maintenance = models.DateField()
    next_maintenance = models.DateField()
    department = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return f"{self.name} ({self.model})"
    
    @property
    def days_until_maintenance(self):
        """Calculate days until next maintenance is due"""
        today = timezone.now().date()
        return (self.next_maintenance - today).days
    
    @property
    def maintenance_overdue(self):
        """Check if maintenance is overdue"""
        return self.days_until_maintenance < 0

class MachineMaintenanceRecord(models.Model):
    MAINTENANCE_TYPES = [
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Maintenance'),
        ('predictive', 'Predictive Maintenance'),
        ('emergency', 'Emergency Repair'),
    ]
    
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField()
    type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    technician = models.CharField(max_length=100)
    notes = models.TextField()
    
    def __str__(self):
        return f"{self.machine.name} - {self.get_type_display()} - {self.date}"

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Pending Customer', 'Pending Customer'),
        ('Closed', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    
    subject = models.CharField(max_length=255)
    ticket_id = models.CharField(max_length=20, unique=True, blank=True)

    description = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='New'
    )
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='Medium'
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='submitted_tickets'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            last_id = Ticket.objects.count() + 1
            self.ticket_id = f"TVK-{last_id:04d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Ticket #{self.id}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


class TicketAttachment(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    file = models.FileField(upload_to='ticket_attachments/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename


class TicketComment(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on Ticket #{self.ticket.ticket_id}"
    
    class Meta:
        ordering = ['created_at']

class CommentAttachment(models.Model):
    comment = models.ForeignKey(TicketComment, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

#user model
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, # If User is deleted, delete profile too
        related_name='profile',   # Allows access via user.profile
        primary_key=True         # Makes the User the primary key for efficiency
    )
    role = models.CharField(
        max_length=100,
        blank=True,           # Allows the field to be empty in forms/admin
        null=True,            # Allows the database column to be NULL
        help_text="User's job title or designation (e.g., Technician, Manager)"
    )
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # If a new User was created, also create a corresponding UserProfile
        UserProfile.objects.create(user=instance)