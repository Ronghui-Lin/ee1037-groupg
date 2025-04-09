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
    path('machine_status/', views.machine_status, name='machine_status'),
    path('api/machine-status/', views.machine_status_api, name='machine-status-api'),
    path('api/account_management/', views.account_management, name='account_management'),
    path('signin/', views.signin, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
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

