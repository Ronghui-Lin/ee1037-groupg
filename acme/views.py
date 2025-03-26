from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    return HttpResponse("Hello, World, this is ACME index")

def abt(request):
    return render(request, "acme/abt.html", {})

def contact(request):
    return render(request, "acme/contact.html", {})