from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Maps to the 'index' view function in views.py
    path("", views.index, name="index"),
    # Maps to the 'abt' view function
    path("abt/", views.abt, name="about"),
    # Maps to the 'contact' view function
    path("contact/", views.contact, name="contact"),
    # Maps to the 'catalog' view function
    path('catalog/', views.catalog, name='catalog'),
    # Maps to the 'services' view function
    path('services/', views.services, name='services'),
    # Maps to the 'faq' view function
    path('faq/', views.faq, name='faq'),
    # Maps to the 'signup' view function
    path('signup/', views.signup, name='signup'),
    # Maps to the 'ticketdash' view function for staff/admins
    path('ticketdash/', views.ticketdash, name='ticketdash'),
    # Captures the ticket ID as a string ('ticket_id') and passes it to the view
    # Maps to the 'ticket_detail' view function
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    # Maps to the 'submit_ticket' view function
    path('submit/', views.submit_ticket, name='submit_ticket'),
    # Maps to the 'policy' view function
    path('policy/', views.policy, name='policy'),
    # Maps to the 'get_all_machines' view function
    path('get_machine_status/', views.get_all_machines, name='get_machine_status'),
    # Maps to the 'machine_status' view function
    path('machine-status/', views.machine_status, name='machine_status'),
    # URL for an API endpoint for account management 
    path('api/account_management/', views.account_management, name='account_management'),
    # Maps to the custom 'signin' view function in views.py
    path('signin/', views.signin, name='signin'),
    # Uses Django's built-in LogoutView Class-Based View
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # URL for a logged-in user to view their own tickets
    # Maps to the 'my_tickets' view function
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    # URL for viewing details of a specific machine
    # Captures the machine ID as a string ('machine_id') and passes it to the view
    # Maps to the 'machine_detail' view function
    path('machines/<str:machine_id>/', views.machine_detail, name='machine_detail'),
    # URL for an API endpoint to get live data for a specific machine
    # Captures the serial number as a string ('serial_number')
    # Maps to the 'machine_data_api' view function
    path('machine-live-data/<str:serial_number>/', views.machine_data_api, name='machine_data_api'),
    # Password reset URLs
    # These use Django's built-in authentication views for handling the password reset flow.

    # URL to initiate password reset (shows email form)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='acme/password_reset.html',
        email_template_name='acme/password_reset_email.html',
        subject_template_name='acme/password_reset_subject.txt'
    ), name='password_reset'),
    # URL shown after the password reset email has been sent
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='acme/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='acme/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    # URL shown after the password has been successfully reset 
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='acme/password_reset_complete.html'
    ), name='password_reset_complete'),
]

