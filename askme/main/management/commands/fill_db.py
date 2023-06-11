from django.core.management.base import BaseCommand
from main.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
import random
import string
import shutil

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

def generate_random_string_in_range(s, e):
    return generate_random_string(random.randint(s, e))

def delete_users():
    User.objects.all().delete()

def delete_questions():
    Question.objects.all().delete()

def delete_tags():
    Tag.objects.all().delete()

def delete_answers():
    Answer.objects.all().delete()

def delete_rates():
    Like.objects.all().delete()

def create_users(num):
    users = []
    for i in range(1, num+1):
        user = User(username=generate_random_string_in_range(5, 10),
                    email=generate_random_string_in_range(5, 15)+"@gmail.com",
                    password=generate_random_string(10))
        users.append(user)

    User.objects.bulk_create(users)

    profiles = []
    for user in User.objects.all():
        profile = Profile(user=user)
        profiles.append(profile)

    Profile.objects.bulk_create(profiles)

def create_questions(num):
    f = open('../w&p.txt', 'r')
    questions = []
    profiles = Profile.objects.all()
    for i in range(1, num):
        question = Question(
            title=f.read(random.randint(5, 20)),
            text=f.read(random.randint(100, 500)),
            profile=random.choice(profiles),
        )
        questions.append(question)
    f.close()
    Question.objects.bulk_create(questions)
    tags = Tag.objects.all()
    new_questions = Question.objects.order_by('-creation_date')[:100]
    for q in new_questions:
        chosen = random.choices(tags, k=random.randint(1, 5))
        for t in chosen:
            t.rating+=1
            t.save
        q.tag.add(*chosen)

def create_answers(num):
    f = open('../w&p.txt', 'r')
    answers = []
    profiles = Profile.objects.all()
    questions = Question.objects.all()
    for i in range(1, num):
        answer = Answer(
            text=f.read(random.randint(100, 400)),
            profile=random.choice(profiles),
            question=random.choice(questions),
        )
        answers.append(answer)
    f.close()
    Answer.objects.bulk_create(answers)

def create_tags(num):
    tags = []
    for i in range(1, num):
        tag = Tag(name=str(i), rating=0)
        tags.append(tag)

    Tag.objects.bulk_create(tags)

def create_rates(num):
    rates = []
    profiles = Profile.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()
    for i in range(1, num//2):
        like = Like(
            profile=random.choice(profiles),
            content_object=random.choice(questions),
            rate=random.choice([True, False]),
        )
        rates.append(like)

    for i in range(1, num//2):
        like = Like(
            profile=random.choice(profiles),
            content_object=random.choice(answers),
            rate=random.choice([True, False]),
        )
        rates.append(like)

    Like.objects.bulk_create(rates)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'ratio', type=int, help='number of users')

    def handle(self, *args, **options):
        ratio = options['ratio']
        delete_users()
        create_users(ratio)
        print('users created')
        delete_tags()
        create_tags(ratio)
        print('tags created')
        delete_questions()
        create_questions(ratio*10)
        print('questions created')
        delete_answers()
        create_answers(ratio*100)
        print('answers created')
        delete_rates()
        create_rates(ratio*200)
        print('rates created')
        return 'ok'
