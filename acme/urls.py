from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("abt/", views.abt, name="about"),
    path("contact/", views.contact, name="contact"),
    path('catalog/', views.catalog, name='catalog'),
    path('services/', views.services, name='services'),
    path('faq/', views.faq, name='faq'),
    path('signup/', views.signup, name='signup'),
    # path('signin/', views.signin, name='signin'),
    path('ticketdash/', views.ticketdash, name='ticketdash'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('policy/', views.policy, name='policy'),
    path('get_machine_status/', views.get_all_machines, name='get_machine_status'),
    path('machine-status/', views.machine_status, name='machine_status'),
    path('api/account_management/', views.account_management, name='account_management'),
    path('signin/', views.signin, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('machines/<str:machine_id>/', views.machine_detail, name='machine_detail'),
    path('machine-live-data/<str:serial_number>/', views.machine_data_api, name='machine_data_api'),
    path('machine-status/add/', views.add_machine, name='add_machine'),
    path('delete_machine/<str:serial_number>/', views.delete_machine, name='delete_machine'),
    path('change-machine-status/<str:serial_number>/', views.change_machine_status, name='change_machine_status'),
    path('manage/users/', views.account_management, name='account_management'),
    path('manage/users/<int:user_id>/edit/', views.account_management_edit, name='edit_user'),
    path('manage/users/<int:user_id>/delete/', views.account_management_delete, name='delete_user'),
    path('profile/', views.profile_view, name='user_profile'),
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='acme/password_reset.html',
        email_template_name='acme/password_reset_email.html',
        subject_template_name='acme/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='acme/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='acme/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='acme/password_reset_complete.html'
    ), name='password_reset_complete'),
]

