from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


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
    return render(request, 'acme/faq.html')

def signup(request):
    return render(request, 'acme/signup.html')

def signin(request):
    return render(request, 'acme/signin.html')