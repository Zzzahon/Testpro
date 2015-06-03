from django.shortcuts import render
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpRequest
from django.shortcuts import render_to_response
from rest_framework import viewsets, generics, request, response, status, urls, permissions
from serializers import *
from models import *
from permissions import *
import django_filters

# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)



class AuthorBooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ReadOnly)#IsAuthorBooksOrReadOnly)
    kwa = None

    def list(self, request, *args, **kwargs):
        #self.id = kwargs.get('id')
        self.kwa = kwargs
        self.permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorBooksOrReadOnly)
        self.queryset = Book.objects.filter(authors=kwargs.get('id'))
        serializer = BookSerializer(self.queryset, context={'request': request}, many=True)
        return response.Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #?self.id = kwargs.get('id')
        #?self.permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorBooksOrReadOnly)
        self.kwa = kwargs
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

    def retrieve(self, request, *args, **kwargs):
        self.kwa = kwargs
        self.permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorBooksOrReadOnly)
        self.queryset = Book.objects.filter(authors=kwargs.get('id')).filter(pk=kwargs.get('pk'))
        serializer = BookSerializer(self.queryset, many=True, context={'request': request})
        if len(self.queryset) > 0:
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def _get_kwa(self):
        return self.kwa


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class BookAuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ReadOnly)
    kwa = None

    def list(self, request, *args, **kwargs):
        self.id = kwargs.get('id')
        self.permission_classes = (permissions.IsAuthenticatedOrReadOnly, ReadOnly)
        self.queryset = Author.objects.filter(books=kwargs['id'])
        serializer = AuthorSerializer(self.queryset, many=True, context={'request': request})
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

    def retrieve(self, request, *args, **kwargs):
        self.kwa = kwargs
        self.permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsBookAuthorsOrReadOnly)
        self.queryset = Author.objects.filter(books=kwargs.get('id')).filter(pk=kwargs.get('pk'))
        serializer = AuthorSerializer(self.queryset, many=True, context={'request': request})
        if len(self.queryset) > 0:
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)

    def _get_kwa(self):
        return self.kwa


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


class AnyList(generics.ListAPIView):
    queryset = Any.objects.all()
    serializer_class = AnySerializer
    permission_classes = (permissions.IsAdminUser,)


class AnyDetail(generics.RetrieveAPIView):
    def get_queryset(self):
        print self.get_queryset()