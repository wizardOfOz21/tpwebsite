from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Profile, Question, Answer, Tag, Like

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects


def index(request):
    questions = Question.get_new_questions()

    page_objects = paginate(questions, request, 6)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }
    return render(request, 'main/index.html', context)


def hot(request):
    questions = Question.get_popular_questions()

    page_objects = paginate(questions, request, 6)

    context = {
        'questions': page_objects,
        'hot_tags': Tag.objects.get_popular()[:10],
        'best_members': Profile.objects.get_popular()[:10],
    }

    return render(request, 'main/hot.html', context)


def tag(request, tname):
    questions = Question.objects.get_by_tag(tag_name=tname)

    page_objects = paginate(questions, request, 6)

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


def ask(request):
    return render(request, 'main/ask.html')


def settings(request):
    return render(request, 'main/settings.html')


def signup(request):
    return render(request, 'main/auth/signup.html')


def login(request):
    return render(request, 'main/auth/login.html')
