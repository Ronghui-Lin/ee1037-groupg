from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import Ticket, TicketAttachment, TicketComment,CommentAttachment, Machine, MachineMaintenanceRecord
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import TicketForm, TicketCommentForm, TicketAttachmentForm, TicketStatusUpdateForm
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone
import random
import json
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

def account_management(request):
    return render(request, 'acme/account_management.html')

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
            
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')  
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'acme/signin.html')

def ticketdash(request):
    view = request.GET.get('view', 'all')
    
    if view == 'open':
        tickets = Ticket.objects.exclude(status='Closed')
        current_view = 'open'
        table_heading = 'Open Tickets'
    else: 
        tickets = Ticket.objects.all()
        current_view = 'all'
        table_heading = 'All Tickets'
    
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
                )
                instance.save()
            
    else:
        form = TicketAttachmentForm()
    

@login_required
@transaction.atomic
def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
    
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

    
    comment_form = TicketCommentForm()
    status_form = TicketStatusUpdateForm(instance=ticket)

    if request.method == 'POST':
        
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

        
        elif 'update_status' in request.POST:
            status_form = TicketStatusUpdateForm(request.POST, instance=ticket)
            if status_form.is_valid():
                new_status = status_form.cleaned_data['status']
                
                
                if ticket.status != 'New' and new_status == 'New':
                    messages.error(request, 'Cannot revert ticket back to "New" status.')
                else:
                    
                    status_form.save()

                    
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
        entry = {
            "name": machine,
            "model": f"MOD-{random.randint(1000, 9999)}-{random.choice(['A', 'B', 'C'])}",
            "status": "ok",
            "last_maintenance": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
            "uptime": random.uniform(75.0, 99.9)  # More realistic decimal values
        }

        entry["uptime"] = round(entry["uptime"], 1)

        if "drilling" in machine.lower():
            entry["last_maintenance"] = (datetime.now() - timedelta(days=random.randint(7, 30))) # More frequent maintenance
        elif "Electroplating" in machine:
            entry["last_maintenance"] = (datetime.now() - timedelta(days=random.randint(1, 14)))

        
        if machine == "Electroplating machine":
            entry["status"] = random.choices(
                ["ok", "warning", "fault"],
                weights=[30, 50, 20], 
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


        if entry["status"] == "ok":
            entry["uptime"] = round(min(entry["uptime"] + random.uniform(0, 5), 100))
        elif entry["status"] == "warning":
            entry["uptime"] = round(max(entry["uptime"] - random.uniform(5, 15), 50))
        else:
            entry["uptime"] = round(max(entry["uptime"] - random.uniform(20, 40), 0))

        status_data.append(entry)
    
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


@login_required
def my_tickets(request):
    view = request.GET.get('view', 'all')
    current_user = request.user
    
    # Get tickets where the user is the creator
    user_tickets = Ticket.objects.filter(created_by=current_user)
    
    # Apply filters based on the selected view
    if view == 'open':
        filtered_tickets = user_tickets.exclude(status='Closed')
    elif view == 'closed':
        filtered_tickets = user_tickets.filter(status='Closed')
    else: 
        filtered_tickets = user_tickets
    
    # Order tickets by last updated, with newest first
    filtered_tickets = filtered_tickets.order_by('-last_updated')
    
    # Get counts for the summary cards
    total_tickets = user_tickets.count()
    open_tickets = user_tickets.exclude(status='Closed').count()
    closed_tickets = user_tickets.filter(status='Closed').count()
    
    context = {
        'tickets': filtered_tickets,
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'current_view': view,
        'page_title': 'My Tickets'
    }
    
    return render(request, 'acme/my_tickets.html', context)


@login_required
def machine_detail(request, machine_id):
    # Get the machine or return 404
    machine = get_object_or_404(Machine, serial_number=machine_id)
    
    # Get health metrics (in a real app, this would come from sensors or IoT data)
    health_percentage = random.randint(70, 100)
    temperature = random.randint(60, 85)  # degrees Celsius
    temperature_percentage = min(100, int((temperature / 100) * 100))
    vibration = round(random.uniform(0.5, 5.0), 1)  # mm/s
    vibration_percentage = min(100, int((vibration / 10) * 100))
    oil_percentage = random.randint(70, 100)
    
    # Set color indicators based on values
    machine.health_percentage = health_percentage
    machine.health_color = get_color_for_value(health_percentage)
    
    machine.temperature = f"{temperature}°C"
    machine.temperature_percentage = temperature_percentage
    machine.temperature_color = get_color_for_temperature(temperature)
    
    machine.vibration = f"{vibration} mm/s"
    machine.vibration_percentage = vibration_percentage
    machine.vibration_color = get_color_for_vibration(vibration)
    
    machine.oil_percentage = oil_percentage
    machine.oil_color = get_color_for_value(oil_percentage)
    
    # Get associated tickets
    open_tickets = Ticket.objects.filter(
        machine=machine,
        status__in=['Open', 'In Progress', 'New', 'Pending Customer']
    ).order_by('-created_at')
    
    closed_tickets = Ticket.objects.filter(
        machine=machine,
        status='Closed'
    ).order_by('-last_updated')
    
    # Get maintenance history
    maintenance_history = MachineMaintenanceRecord.objects.filter(
        machine=machine
    ).order_by('-date')
    
    # Generate historical performance data for the last 24 hours
    end_time = timezone.now()
    start_time = end_time - timedelta(hours=24)
    
    # Generate hourly timestamps
    timestamps = []
    current_time = start_time
    while current_time <= end_time:
        timestamps.append(current_time.strftime('%H:%M'))
        current_time += timedelta(hours=1)
    
    base_performance = random.randint(80, 95)
    base_temp = random.randint(65, 75)
    base_vibration = random.uniform(1.0, 3.0)
    
    performance_data = []
    temperature_data = []
    vibration_data = []
    
    for i in range(len(timestamps)):
        perf_variation = random.randint(-5, 5)
        temp_variation = random.randint(-3, 3)
        vib_variation = random.uniform(-0.5, 0.5)
        
        if machine.status == 'fault' and i > len(timestamps) - 3:
            perf_variation -= 15
            temp_variation += 10
            vib_variation += 2
            
        # Ensure values stay within reasonable ranges
        performance = max(50, min(100, base_performance + perf_variation))
        temperature_val = max(50, min(95, base_temp + temp_variation))
        vibration_val = max(0.5, min(7.0, base_vibration + vib_variation))
        
        performance_data.append(performance)
        temperature_data.append(temperature_val)
        vibration_data.append(round(vibration_val, 1))
    
    context = {
        'machine': machine,
        'open_tickets': open_tickets,
        'closed_tickets': closed_tickets,
        'maintenance_history': maintenance_history,
        'timestamps': json.dumps(timestamps),
        'performance_data': json.dumps(performance_data),
        'temperature_data': json.dumps(temperature_data),
        'vibration_data': json.dumps(vibration_data),
        'page_title': f'Machine Details: {machine.name}'
    }
    
    return render(request, 'acme/machine_detail.html', context)

@login_required
def machine_data_api(request, serial_number):
    machine = get_object_or_404(Machine, serial_number=serial_number)

    end_time = timezone.now()
    start_time = end_time - timedelta(hours=24)
    
    # Generate hourly timestamps
    timestamps = []
    current_time = start_time
    while current_time <= end_time:
        timestamps.append(current_time.strftime('%H:%M'))
        current_time += timedelta(hours=1)

    base_performance = random.randint(80, 95)
    base_temp = random.randint(65, 75)
    base_vibration = random.uniform(1.0, 3.0)

    performance_data = []
    temperature_data = []
    vibration_data = []

    for i in range(len(timestamps)):
        perf_variation = random.randint(-5, 5)
        temp_variation = random.randint(-3, 3)
        vib_variation = random.uniform(-0.5, 0.5)

        if machine.status == 'fault' and i > len(timestamps) - 3:
            perf_variation -= 15
            temp_variation += 10
            vib_variation += 2

        performance = max(50, min(100, base_performance + perf_variation))
        temperature_val = max(50, min(95, base_temp + temp_variation))
        vibration_val = max(0.5, min(7.0, base_vibration + vib_variation))

        performance_data.append(performance)
        temperature_data.append(temperature_val)
        vibration_data.append(round(vibration_val, 1))

    return JsonResponse({
        'timestamps': timestamps,
        'performance': performance_data,
        'temperature': temperature_data,
        'vibration': vibration_data
    })

@login_required
def get_all_machines(request):
    machines = list(Machine.objects.values()) 
    return JsonResponse({"machines": machines})
@login_required
def machine_status(request):
    machines = Machine.objects.all()
    context = {
        'machines': machines
    }
    
    return render(request, 'acme/machine_status.html', context)

def get_color_for_value(value):
    """Return color based on percentage value"""
    if value >= 85:
        return 'success'
    elif value >= 70:
        return 'warning'
    else:
        return 'danger'

def get_color_for_temperature(temp):
    """Return color based on temperature"""
    if temp < 70:
        return 'success'
    elif temp < 80:
        return 'warning'
    else:
        return 'danger'

def get_color_for_vibration(vibration):
    """Return color based on vibration value"""
    if vibration < 2.0:
        return 'success'
    elif vibration < 4.0:
        return 'warning'
    else:
        return 'danger'