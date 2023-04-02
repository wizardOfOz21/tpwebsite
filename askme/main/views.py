from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    data = {
        'title': 'Main Page',
        'values': ['Some', '123', "324"],
        'obj': {
            'f1' : "f1",
            'f2' : "f2",
            'f3' : "f4"
        },
    }
    return render(request, 'main/index.html',  data)

def about(request):
    return render(request, 'main/about.html')

def listing(request):
    return render(request, 'main/taglisting.html')

def ask(request):
    return render(request, 'main/ask.html')

def settings(request):
    return render(request, 'main/settings.html')

def signup(request):
    return render(request, 'main/auth/signup.html')

def login(request):
    return render(request, 'main/auth/login.html')

def question(request):
    return render(request, 'main/question.html')
