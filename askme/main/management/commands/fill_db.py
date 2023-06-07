from django.core.management.base import BaseCommand
from main.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def generate_random_string_in_range(s, e):
    return generate_random_string(random.randint(s, e))


def delete_users():
    User.objects.exclude(username='johndoe').delete()
    Profile.objects.all().delete()

def delete_questions():
    Question.objects.all().delete()

def delete_tags():
    Tag.objects.all().delete()

def delete_answers():
    Answer.objects.all().delete()

def delete_rates():
    Like.objects.all().delete()

def create_users(num):
    profiles = []
    users = []

    for i in range(1, num+1):
        user = User(username=generate_random_string_in_range(5, 10),
                    email=generate_random_string_in_range(5, 15)+"@gmail.com",
                    password=generate_random_string(10))
        users.append(user)

    User.objects.bulk_create(users)

    for user in User.objects.all():
        profile = Profile(profile=user, rating=random.randint(0, 500))
        profiles.append(profile)

    Profile.objects.bulk_create(profiles)

def create_questions(num):
    questions = []
    for i in range(1, num):
        question = Question(
            title='Question about ' + generate_random_string_in_range(5, 20),
            text=generate_random_string(random.randint(100, 2000)),
            user_id=random.choice(Profile.objects.all()),
            rating=random.randint(0, 200),
        )

        question.save()

        question.tag.add(
            *random.choices(Tag.objects.all(), k=random.randint(1, 5)))

        questions.append(question)

    # Question.objects.bulk_create(questions)

def create_answers(num):
    answers = []
    for i in range(1, num):
        answer = Answer(
            text=generate_random_string(random.randint(100, 2000)),
            user_id=random.choice(Profile.objects.all()),
            question_id=random.choice(Question.objects.all()),
            rating=random.randint(0, 400),
        )
        answers.append(answer)

    Answer.objects.bulk_create(answers)

def create_tags(num):
    tags = []
    for i in range(1, num):
        tag = Tag(name=generate_random_string_in_range(1, 7), rating=0)
        tags.append(tag)

    Tag.objects.bulk_create(tags)

def create_rates(num):
    rates = []
    for i in range(1, num//2):
        like = Like(
            user_id=random.choice(Profile.objects.all()),
            content_object=random.choice(Question.objects.all()),
            rate=random.choice([True, False]),
        )
        rates.append(like)

    for i in range(1, num//2):
        like = Like(
            user_id=random.choice(Profile.objects.all()),
            content_object=random.choice(Answer.objects.all()),
            rate=random.choice([True, False]),
        )
        rates.append(like)

    Like.objects.bulk_create(rates)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'ratio', type=int, help='Указывает сколько пользователей необходимо создать')

    def handle(self, *args, **options):
        ratio = options['ratio']
        delete_users()
        create_users(ratio)
        delete_tags()
        create_tags(ratio)
        delete_questions()
        create_questions(ratio*10)
        delete_answers()
        create_answers(ratio*100)
        delete_rates()
        create_rates(ratio*200)
        return 'ok'
