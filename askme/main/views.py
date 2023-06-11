from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Profile, Question, Answer, Tag, Like
from .forms import LoginForm
from .forms import RegistrationForm
from .forms import EditForm
from .forms import AskForm
from .forms import AnswerForm
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.http import require_http_methods

QUESTION_PAGE_NUM = 6
ANSWERS_PAGE_NUM = 3

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects

def index(request):
    questions = Question.objects.get_new()

    page_objects = paginate(questions, request, QUESTION_PAGE_NUM)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }
    return render(request, 'main/index.html', context)

def hot(request):
    questions = Question.objects.get_popular()

    page_objects = paginate(questions, request, QUESTION_PAGE_NUM)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/hot.html', context)

def tag(request, tag_name):
    questions = Question.objects.get_by_tag(tag_name=tag_name)

    page_objects = paginate(questions, request, QUESTION_PAGE_NUM)

    context = {
        'questions': page_objects,
        'tag_name': tag_name,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/tag.html', context)

@require_http_methods(['GET', 'POST'])
def question(request, q_id):
    question = Question.objects.get_by_id(q_id=q_id)
    if request.method == "GET":
        answer_form = AnswerForm()
    else:
        answer_form = AnswerForm(request.POST)

        if request.user.is_authenticated:
            if answer_form.is_valid():
                answer = answer_form.save(user=request.user, question=question)
                if answer:
                    return redirect("%s?page=-1" % reverse('question', kwargs={'q_id': q_id}))
                answer_form.add_error(None, "Saving answer error")
        else:
            answer_form.add_error(None, "Please log in to answer")

    answers = Answer.objects.get_by_qid(question_id=q_id)
    page_objects = paginate(answers, request, ANSWERS_PAGE_NUM)

    context = {
        'question': question,
        'answers': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
        'form': answer_form,
    }
    return render(request, 'main/question.html', context)

@login_required()
@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == "GET":
        ask_form = AskForm()
    else:
        ask_form = AskForm(request.POST)

        if ask_form.is_valid():
            question = ask_form.save(user=request.user)
            if question:
                return redirect(reverse('question', kwargs={'q_id': question.id}))
            ask_form.add_error(None, "Saving question error")
    return render(request, 'main/ask.html', context={'form': ask_form})

@login_required()
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == "GET":
        data = model_to_dict(request.user)
        edit_form = EditForm(initial=data)
    else:
        edit_form = EditForm(request.POST, files=request.FILES, instance=request.user)

        if edit_form.is_valid():
            user = edit_form.save()
            if user:
                return redirect(reverse('settings'))
            edit_form.add_error(None, "Error")

    return render(request, 'main/settings.html', context={'form': edit_form})

@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    else:
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
    return render(request, 'main/auth/login.html', context={'form': login_form, 'next': next_url})

def signup(request):
    if request.method == "GET": 
        reg_form = RegistrationForm()
    elif request.method == "POST":
        reg_form = RegistrationForm(request.POST, request.FILES)
        if reg_form.is_valid():
            user = reg_form.save()
            if user:
                login(request, user)
                return redirect(reverse('home'))
            reg_form.add_error(None, "Saving error")
    return render(request, 'main/auth/signup.html', context={'form': reg_form})
