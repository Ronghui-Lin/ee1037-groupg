from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Ticket, TicketAttachment, TicketComment,CommentAttachment
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import TicketForm, TicketCommentForm, TicketAttachmentForm, TicketStatusUpdateForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction

OPEN_STATUSES = ['Open', 'New', 'In Progress'] # VIGNESH, ADJUST HERE BASED ON DATABASE

def index(request):
    return render(request, "acme/index.html", {})

def abt(request):
    return render(request, "acme/abt.html", {})

def contact(request):
    return render(request, "acme/contact.html", {})

def catalog(request):
    return render(request, 'acme/catalog.html')

def services(request):
    return render(request, 'acme/services.html')

def faq(request):
    return render(request, 'acme/FAQ.html')

def policy(request):
    return render(request, 'acme/policy.html')

# def signup(request):
#     return render(request, 'acme/signup.html')

# def signin(request):
#     return render(request, 'acme/signin.html')

def machine_status(request):
    return render(request, 'acme/machine_status.html')

def account_management(request):
    return render(request, 'acme/account_management.html')

# def ticketdash(request):
#     # --- Summary Card Data ---
#     total_tickets = Ticket.objects.count()
#     # Count currently open tickets
#     open_tickets_count = Ticket.objects.filter(status__in=OPEN_STATUSES).count()
#     # example: Count tickets closed today, uncomment code below or we can adjust by changing thist o total tickets)
#     # closed_today_tickets = Ticket.objects.filter(status='Closed', closed_date__date=timezone.now().date()).count()
#     closed_today_tickets = 0 # Placeholder
#     # example: Count high priority open tickets
#     high_priority_open_tickets = Ticket.objects.filter(
#         priority='High',
#         status__in=OPEN_STATUSES
#     ).count()

#     # --- Ticket Table Data (Filter based on the view) ---
#     current_view = request.GET.get('view', 'open') # Default to 'open' if param not present

#     if current_view == 'all':
#         tickets_queryset = Ticket.objects.all()
#         table_heading = "All Tickets"
#     else:
#         # default to 'open' view if param is anything else or missing
#         current_view = 'open' # Ensure current_view is set correctly for the template
#         tickets_queryset = Ticket.objects.filter(status__in=OPEN_STATUSES)
#         table_heading = "Open Tickets"

#     # Order and limit the queryset for display
#     # maybe change view all to use pagination here, if we have too many tickets
#     tickets_to_display = tickets_queryset.order_by('-last_updated')[:50] # example: this shows latest 50

#     context = {
#         'total_tickets': total_tickets,
#         'open_tickets': open_tickets_count,
#         'closed_today_tickets': closed_today_tickets,
#         'high_priority_open_tickets': high_priority_open_tickets,
#         'tickets': tickets_to_display, # pass the filtered list
#         'current_view': current_view,   # pass the active view ('open' or 'all')
#         'table_heading': table_heading, # pass the dynamic heading
#         # other context variables if we need
#     }
#     return render(request, 'acme/ticketdash.html', context)

# # UNCOMMENT LATER WHEN AUTH IS IMPLEMENTED
# # @login_required # ensures only logged-in users can access this page
# def submit_ticket(request):
#     if request.method == 'POST':
#         # Pass request.POST for text data and request.FILES for file data
#         form = TicketForm(request.POST, request.FILES)
#         if form.is_valid():
#             # create Ticket object but don't save to database yet
#             ticket = form.save(commit=False)
#             # assign the logged-in user as the reporter
#             ticket.reporter = request.user
#             # set initial status
#             ticket.status = 'NEW'
#             # save the Ticket instance to the database
#             # saving the file to the path defined by upload_to
#             ticket.save()

#             messages.success(request, f'Ticket "{ticket.subject}" submitted successfully!')
#             # Redirect to the 'ticket detail' page after submission
#             return redirect('ticket_detail', ticket_id=ticket.id)
#         else:
#             # Form is invalid, render the page again with error messages
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         # GET request, display a blank form
#         form = TicketForm()

#     context = {
#         'form': form,
#         'page_title': 'Submit New Support Ticket' # title for the template
#     }
#     return render(request, 'acme/submit_ticket.html', context) # 

# Custom UserCreationForm with email field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    is_staff = forms.BooleanField(required=False, initial=False, label="Staff Access")
    is_superuser = forms.BooleanField(required=False, initial=False, label="Superuser Access")
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "is_staff", "is_superuser")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = self.cleaned_data.get("is_staff", False)
        user.is_superuser = self.cleaned_data.get("is_superuser", False)
        if commit:
            user.save()
        return user


@login_required
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'acme/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            
            # Get the next parameter if it exists
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')  # Default redirect to home page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'acme/signin.html')

def ticketdash(request):
    view = request.GET.get('view', 'all')
    
    # Get ticket data based on view parameter
    if view == 'open':
        tickets = Ticket.objects.exclude(status='Closed')
        current_view = 'open'
        table_heading = 'Open Tickets'
    else:  # 'all' is the default
        tickets = Ticket.objects.all()
        current_view = 'all'
        table_heading = 'All Tickets'
    
    # Calculate dashboard stats
    today = timezone.now().date()
    total_tickets = Ticket.objects.count()
    open_tickets = Ticket.objects.exclude(status='Closed').count()
    closed_today_tickets = Ticket.objects.filter(
        status='Closed', 
        last_updated__date=today
    ).count()
    high_priority_open_tickets = Ticket.objects.filter(
        priority='High'
    ).exclude(status='Closed').count()
    
    context = {
        'tickets': tickets,
        'current_view': current_view,
        'table_heading': table_heading,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'closed_today_tickets': closed_today_tickets,
        'high_priority_open_tickets': high_priority_open_tickets,
    }
    
    return render(request, 'acme/ticketdash.html', context)

def upload_files(request, ticket_id):
    if request.method == 'POST':
        form = TicketAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for f in files:
                instance = TicketAttachment(
                    file=f,
                    ticket_id=ticket_id,
                    # other fields as needed
                )
                instance.save()
            # Redirect or render response
    else:
        form = TicketAttachmentForm()
    # Render form

@login_required
@transaction.atomic
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        # Create a separate form for file uploads
        file_form = TicketAttachmentForm(request.POST, request.FILES)
        
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            
            # Handle file attachments
            files = request.FILES.getlist('file')
            for f in files:
                TicketAttachment.objects.create(
                    ticket=ticket,
                    file=f,
                    filename=f.name
                )
            
            messages.success(request, 'Your ticket has been submitted successfully.')
            return redirect('ticket_detail', ticket_id=ticket.ticket_id)
    else:
        form = TicketForm()
        file_form = TicketAttachmentForm()
        
    context = {
        'form': form,
        'file_form': file_form,
        'page_title': 'Submit New Support Ticket'
    }
    return render(request, 'acme/submit_ticket.html', context)


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)

    # Initialize forms
    comment_form = TicketCommentForm()
    status_form = TicketStatusUpdateForm(instance=ticket)

    if request.method == 'POST':
        # Handle comment submission
        if 'submit_comment' in request.POST:
            comment_form = TicketCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket
                comment.author = request.user
                comment.save()

                if request.FILES.get('attachment'):
                    CommentAttachment.objects.create(
                        comment=comment,
                        file=request.FILES['attachment']
                    )

                messages.success(request, 'Comment added successfully.')
                return redirect('ticket_detail', ticket_id=ticket.ticket_id)

        # Handle status update
        elif 'update_status' in request.POST:
            status_form = TicketStatusUpdateForm(request.POST, instance=ticket)
            if status_form.is_valid():
                new_status = status_form.cleaned_data['status']
                
                # Prevent reverting to 'New' once changed
                if ticket.status != 'New' and new_status == 'New':
                    messages.error(request, 'Cannot revert ticket back to "New" status.')
                else:
                    # Save the new status
                    status_form.save()

                    # Log the status change
                    TicketComment.objects.create(
                        ticket=ticket,
                        author=request.user,
                        content=f"Status changed to {ticket.status} by {request.user.username}"
                    )

                    messages.success(request, 'Ticket status updated successfully.')
                
                return redirect('ticket_detail', ticket_id=ticket.ticket_id)

    context = {
        'ticket': ticket,
        'comment_form': comment_form,
        'status_form': status_form,
    }

    return render(request, 'acme/ticket_detail.html', context)

@csrf_exempt
def machine_status_api(request):
    machines = [
        "CNC drilling Machine",
        "Lamination press",
        "Electroplating machine",
        "Soldering machine",
        "Electrical testing machine",
        "Pick and Place Machine",
        "AOI Machine",
        "Automated Test Equipment"
    ]
    
    status_data = []
    for machine in machines:
        # Generate unique random values for each machine
        entry = {
            "name": machine,
            "model": f"MOD-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C'])}",
            "status": "ok",
            "last_maintenance": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "uptime": random.uniform(75.0, 99.9)  # More realistic decimal values
        }

        # Make uptime precision consistent
        entry["uptime"] = round(entry["uptime"], 1)

        # Vary maintenance frequency based on machine type
        if "drilling" in machine.lower():
            entry["last_maintenance"] = (datetime.now() - timedelta(days=random.randint(7, 30))) # More frequent maintenance
        elif "Electroplating" in machine:
            entry["last_maintenance"] = (datetime.now() - timedelta(days=random.randint(1, 14)))

        # Status probability modifications
        if machine == "Electroplating machine":
            entry["status"] = random.choices(
                ["ok", "warning", "fault"],
                weights=[30, 50, 20],  # Higher chance of warnings
                k=1
            )[0]
        elif machine == "AOI Machine":
            entry["status"] = random.choices(
                ["ok", "warning", "fault"],
                weights=[70, 25, 5],
                k=1
            )[0]
        else:
            entry["status"] = random.choices(
                ["ok", "warning", "fault"],
                weights=[80, 15, 5],
                k=1
            )[0]

        # Add unique performance characteristics
        if entry["status"] == "ok":
            entry["uptime"] = round(min(entry["uptime"] + random.uniform(0, 5), 100))
        elif entry["status"] == "warning":
            entry["uptime"] = round(max(entry["uptime"] - random.uniform(5, 15), 50))
        else:
            entry["uptime"] = round(max(entry["uptime"] - random.uniform(20, 40), 0))

        status_data.append(entry)
    
    # Generate fake fault history 'maybe change this to actual add the random ones generated above'
    history = []
    for i in range(10):  # Last 10 events
        machine = random.choice(machines)
        status = random.choice(["warning", "fault"])
        
        history.append({
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, 1440))).isoformat(),
            "machine": machine,
            "status": status,
            "status_display": status.capitalize(),
            "description": random.choice([
                "Temperature threshold exceeded",
                "Component failure detected",
                "Preventive maintenance needed",
                "Calibration required",
                "Sensor timeout error",
                "Throughput reduced",
                "Emergency stop triggered"
            ])
        })
    
    return JsonResponse({
        "machines": status_data,
        "history": history
    })