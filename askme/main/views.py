from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Profile, Question, Answer, Tag, Like
from .forms import LoginForm
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

PAGE_NUM = 6

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects

def index(request):
    questions = Question.get_new_questions()

    page_objects = paginate(questions, request, PAGE_NUM)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }
    return render(request, 'main/index.html', context)

def hot(request):
    questions = Question.get_popular_questions()

    page_objects = paginate(questions, request, PAGE_NUM)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/hot.html', context)


def tag(request, tname):
    questions = Question.objects.get_by_tag(tag_name=tname)

    page_objects = paginate(questions, request, PAGE_NUM)

    context = {
        'questions': page_objects,
        'tname': tname,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/tag.html', context)


def question(request, qid):
    q = Question.objects.get_by_id(question_id=qid)

    answers = paginate(Answer.objects.get_by_qid(question_id=qid), request, 3)

    context = {
        'question': q,
        'answers': answers,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/question.html', context)

@login_required()
def ask(request):
    return render(request, 'main/ask.html')

@login_required()
def settings(request):
    return render(request, 'main/settings.html')

def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    elif request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                url = request.GET.get('next')
                return redirect(url)
            login_form.add_error(None, "Invalid username or password")

    next_url = request.GET.get('next')
    if not next_url:
        next_url = reverse('home')
    print(next_url)
    return render(request, 'main/auth/login.html', context={'form': login_form, 'next': next_url})

def signup(request):
    # if request.method == "GET": 
    #     reg_form = RegistrationForm()
    # elif request.method == "POST":
    #     reg_form = RegistrationForm(request.POST)

    #     if reg_form.is_valid():
    #         user = Profile.objects.
    #         if user:
    #             login(request, user)
    #             return redirect(reverse('home'))
    #         login_form.add_error(None, "Invalid username or password")
    return render(request, 'main/auth/signup.html', context={'form': register_form})
