from django.db import models
from django.conf import settings
from django.utils import timezone
import os

def ticket_attachment_path(instance, filename):
    # Generate a unique path based on ticket ID (or 'temp' if not saved yet)
    ticket_id_str = str(instance.id) if instance.id else f"unsaved_{timezone.now().strftime('%Y%m%d%H%M%S')}"
    return os.path.join('ticket_attachments', f'ticket_{ticket_id_str}', filename)

# --- Machine Model, remove parts we dont need---
class Machine(models.Model):
    """ a piece of machinery in the facility. """
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
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True, # ensure serial numbers are unique if they exist
        help_text="Manufacturer's serial number (optional)."
    )


    class Meta:
        ordering = ['name'] # Order machines alphabetically by default
        verbose_name = "Machine"
        verbose_name_plural = "Machines"

    def __str__(self):
        return self.name

# --- Ticket Model ---
class Ticket(models.Model):
    """ Represents a support ticket in the system. """

    # --- Choices ---
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('ON_HOLD', 'On Hold'),
        ('CLOSED', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]
    CATEGORY_CHOICES = [
        ('BUG', 'Bug Report'),
        ('GENERAL', 'General Enquiry'),
        ('ACCOUNT', 'Account Issue'),
        ('HARDWARE', 'Hardware Problem'),
        ('SOFTWARE', 'Software Issue'),
    ]

    # --- Core Fields ---
    subject = models.CharField(
        max_length=255,
        help_text="Brief summary of the ticket's purpose."
    )
    description = models.TextField(
        help_text="Detailed description of the issue or request."
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        db_index=True,
        help_text="The current status of the ticket."
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        db_index=True,
        help_text="The urgency level of the ticket."
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='GENERAL',
        db_index=True,
        help_text="The category of the issue."
    )

    # --- Timestamps ---
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp when the ticket was created."
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the ticket was last modified."
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )

    # --- Relationships ---
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Prevent deleting user if they have tickets
        related_name='reported_tickets',
        help_text="The user who submitted the ticket."
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Allow ticket to become unassigned if assignee deleted
        related_name='assigned_tickets',
        null=True,
        blank=True,
        help_text="The user currently assigned to resolve the ticket (optional).",
        db_index=True
    )

    # ForeignKey to link to a specific machine (optional)
    machine = models.ForeignKey(
        Machine,
        on_delete=models.SET_NULL, # If machine is deleted, set this field to Null
        null=True,                 # Allow Null in the database
        blank=True,                # Allow the field to be blank in forms/admin
        related_name='tickets',    # How to refer to tickets from a machine instance (machine.tickets.all())
        help_text="Select the specific machine related to this ticket, if applicable.",
        db_index=True
    )

    # --- Attachment ---
    attachment = models.FileField(
        upload_to=ticket_attachment_path,
        null=True,
        blank=True,
        help_text="Optional file attachment related to the ticket (e.g., screenshot, log file)."
    )

    # --- Meta Options ---
    class Meta:
        ordering = ['-last_updated']
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"

    # --- Methods ---
    def __str__(self):
        """String representation of the Ticket model."""
        return f"Ticket #{self.id}: {self.subject}"

    def get_attachment_filename(self):
        """Returns the basename of the attached file, or None."""
        if self.attachment:
            return os.path.basename(self.attachment.name)
        return None

    def save(self, *args, **kwargs):
        # If the ticket status is changed to 'CLOSED' and resolved_at is not set, set it.
        if self.status == 'CLOSED' and self.resolved_at is None:
            self.resolved_at = timezone.now()
        # If the status is changed away from 'CLOSED', clear resolved_at (optional logic)
        elif self.status != 'CLOSED' and self.resolved_at is not None:
            self.resolved_at = None
        super().save(*args, **kwargs) # Call the "real" save() method.