from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpRequest
from django.shortcuts import render_to_response
from rest_framework import viewsets, generics, request, response, status
from serializers import *
from models import *
import django_filters

# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorBooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        queryset = Book.objects.filter(authors=kwargs.get('id'))
        serializer = BookSerializer(queryset, context={'request': request}, many=True)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        new_book = BookSerializer(data=request.DATA)
        book = None
        if new_book.is_valid():
            book = new_book.save()
        member_data = {'book': book, 'author': Author.objects.get(pk=kwargs.get('id'))}
        new_member = MemberSerializer(data=member_data)
        if new_member.is_valid():
            new_member.save()
            return response.Response(status=status.HTTP_201_CREATED)
        book.delete()
        return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def list(self, request, *args, **kwargs):
        queryset = Author.objects.filter(books=kwargs['id'])
        serializer = AuthorSerializer(queryset, many=True, context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        new_author = AuthorSerializer(data=request.DATA)
        author = None
        if new_author.is_valid():
            author = new_author.save()
        member_data = {'author': author, 'book': Book.objects.get(pk=kwargs['id'])}
        new_member = MemberSerializer(data=member_data)
        if new_member.is_valid():
            new_member.save()
            return response.Response(status=status.HTTP_201_CREATED)
        author.delete()
        return response.Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer