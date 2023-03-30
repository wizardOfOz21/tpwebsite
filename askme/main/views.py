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
    return render(request, 'main/basic.html',  data)


def about(request):
    return render(request, 'main/about.html')
