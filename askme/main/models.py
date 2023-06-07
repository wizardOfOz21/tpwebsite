import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ProfileManager(models.Manager):
    def get_popular(self):
        return self.filter(rating__gt=100)

class Profile(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='products/img/')
    rating = models.DecimalField(max_digits=6, decimal_places=2)

    objects = ProfileManager()

    def __str__(self):
        return self.profile.username


class QuestionManager(models.Manager):
    def get_popular(self):
        return self.order_by('-rating')

    def get_new(self):
        return self.order_by('-creation_date')
    
    def get_by_tag(self, tag_name):
        tag_id = Tag.objects.get(name=tag_name).id
        questions = self.filter(tag__exact=tag_id).order_by('creation_date')
        questions.prefetch_related('tag')
        for q in questions:
            q.tags = q.tag.all()
        return questions
    
    def get_by_id(self, question_id):
        question = self.get(id=question_id)
        question.tags = question.tag.all()

        return question
    
    def get_tags(self, question_id):
        question = self.get_by_id(question_id)
        return question.tag.all()

class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField(null=True)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)

    tag = models.ManyToManyField('Tag')

    objects = QuestionManager()

    def get_new_questions():
        questions = Question.objects.get_new()
        for q in questions:
            q.tags = q.tag.all()
        return questions
    
    def get_popular_questions():
        questions = Question.objects.get_popular()
        for q in questions:
            q.tags = q.tag.all()
        return questions


class AnswerManager(models.Manager):
    def get_by_qid(self, question_id):
        return self.filter(question_id__exact=question_id).order_by('-rating','-creation_date')

class Answer(models.Model):
    text = models.TextField(null=True)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default = False)

    objects = AnswerManager()


class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by('rating')

class Tag(models.Model):
    name = models.CharField(max_length=10)
    rating = models.PositiveIntegerField()

    objects = TagManager()

    def __str__(self):
        return self.name


class LikeManager(models.Manager):
    pass

class Like(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    rate = models.BooleanField()

    objects = LikeManager()
