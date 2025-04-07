from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("abt/", views.abt, name="about"),
    path("contact/", views.contact, name="contact"),
    path('catalog/', views.catalog, name='catalog'),
    path('services/', views.services, name='services'),
    path('faq/', views.faq, name='faq'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('ticketdash/', views.ticketdash, name='ticketdash'),
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('policy/', views.policy, name='policy'),
    path('machine_status/', views.machine_status, name='machine_status'),
    path('api/machine-status/', views.machine_status_api, name='machine-status-api'),
    path('api/account_management/', views.account_management, name='account_management'),
]

