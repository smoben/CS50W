from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def bence(request):
    return HttpResponse("Hello, Bence!!")

def david(request):
    return HttpResponse("Hello, David")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })