import datetime
import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ProfileManager(models.Manager):
    def get_popular(self):
        return self.order_by('-rating')

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=False, blank=True, upload_to='avatars/%Y/%m/%d/', default='avatars/default_avatar.png')
    rating = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=False)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

class QuestionManager(models.Manager):
    def get_popular(self):
        return self.order_by('-rating')

    def get_new(self):
        return self.order_by('-creation_date')
    
    def get_by_tag(self, tag_name):
        tag = Tag.objects.get(name=tag_name)
        questions = self.filter(tag__exact=tag).order_by('-creation_date')
        questions.prefetch_related('tag')
        return questions
    
    def get_by_id(self, q_id):
        return self.get(id=q_id)
    
    def get_tags(self, question_id):
        question = self.get_by_id(question_id)
        return question.tag.all()

class Question(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField(max_length=20000, null=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField('Tag')
    objects = QuestionManager()

class AnswerManager(models.Manager):
    def get_by_qid(self, question_id):
        return self.filter(question_id__exact=question_id).order_by('creation_date')

class Answer(models.Model):
    text = models.TextField(max_length="20000", null=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default = False)

    objects = AnswerManager()

class TagManager(models.Manager):
    def get_popular(self):
        return self.order_by('-rating')

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)
    rating = models.PositiveIntegerField(default=0, null=False)
    objects = TagManager()
    def __str__(self):
        return self.name

class LikeManager(models.Manager):
    pass

class Like(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    rate = models.BooleanField()

    objects = LikeManager()
