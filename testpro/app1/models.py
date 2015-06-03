from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission

# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, blank=True, null=True)
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    books = models.ManyToManyField('Book', through='Member', related_name='Member_list')

    def __unicode__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, through='Member', related_name='Member_list')

    def __unicode__(self):
        return self.title


class Member(models.Model):
    book = models.ForeignKey(Book)
    author = models.ForeignKey(Author)


class Comment(models.Model):
    text = models.CharField(max_length=500)
    book = models.ForeignKey(Book)


class Any(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User')

    def __unicode__(self):
        return self.title