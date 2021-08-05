from django.http import HttpResponse
from django.shortcuts import render

from datetime import datetime

def home(request):
    return render(request, "studyquiz/home.html")

def about(request):
    return render(request, "studyquiz/about.html")

def contact(request):
    return render(request, "studyquiz/contact.html")

def hello_there(request, name):
    return render(
        request,
        'studyquiz/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )