from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("abt/", views.abt, name="about"),
    path("contact/", views.contact, name="contact"),
]