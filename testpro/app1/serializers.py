from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *
import django_filters


class UserSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name')
    class Meta:
        model = User
        fields = ('url', 'username', 'author', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = Author
        fields = ('url', 'name', 'age', 'user', 'books')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'title', 'authors')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'text', 'book')


class MemberSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.SlugRelatedField(slug_field='title', queryset=Book.objects.all())
    author = serializers.SlugRelatedField(slug_field='name', queryset=Author.objects.all())

    class Meta:
        model = Member
        fields = ('url', 'book', 'author')


class AnySerializer(serializers.ModelSerializer):
    class Meta:
        model = Any
        fields = ('title', 'user')