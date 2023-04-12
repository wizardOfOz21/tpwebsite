from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


class Question:
    def __init__(self, title, text, anum, id, tags):
        self.title = title
        self.text = text
        self.anum = anum
        self.id = id
        self.tags = tags

def get_some_questions(num):
    questions = []
    for i in range(1, num):
        questions.append(Question(
            'Question#' + str(i),
            generate_random_string(random.randint(100,2000)),
            i,
            i,
            [generate_random_string(3), generate_random_string(2), generate_random_string(1)],
        ))
    return questions

class FakeDataBase:
    def __init__(self, num):
        self.data = get_some_questions(num)

    def get_question(self,id):
        return self.data[id]
    
    def get_all(self):
        return self.data
    
    def get_by_tag(self, tag):
        tlist = []
        for el in self.data:
            for t in el.tags:
                if t == tag:
                    tlist.append(el)
                    break
        return tlist
    
    def get_by_rating(self, num):
        rtop = []
        while len(rtop) < num:
            rtop.append(self.data[random.randint(0, len(self.data))])
        return rtop

db = FakeDataBase(70)

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)
    return objects


def index(request):
    questions = db.get_all()
    
    page_objects = paginate(questions, request, 6)
    return render(request, 'main/index.html', {'questions': page_objects})

def hot(request):
    questions = db.get_by_rating(10)
    
    page_objects = paginate(questions, request, 6)
    return render(request, 'main/hot.html', {'questions': page_objects})


def tag(request, tname):
    questions = db.get_by_tag(tname)

    page_objects = paginate(questions, request, 6)
    return render(request, 'main/tag.html', {'questions': page_objects, 'tname': tname})

def question(request, qid):
    q = db.get_question(int(qid)-1)

    answers = paginate(get_some_questions(10), request, 3)

    return render(request, 'main/question.html', {'question': q, 'answers': answers})


def ask(request):
    return render(request, 'main/ask.html')

def settings(request):
    return render(request, 'main/settings.html')

def signup(request):
    return render(request, 'main/auth/signup.html')

def login(request):
    return render(request, 'main/auth/login.html')
