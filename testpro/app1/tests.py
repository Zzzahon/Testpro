from django.test import TestCase
from .models import *

# Create your tests here.


class AuthorTestCase(TestCase):
    def setUp(self):
        Author.objects.create(name='Dima', age=22)
        Author.objects.create(name='Miha', age=44)

    def test_author(self):
        dima = Author.objects.get(name='Dima')
        miha = Author.objects.get(name='Miha')
        self.assertEqual(dima.age, 22)
        self.assertEqual(miha.age, 44)


class ManyToManyTest(TestCase):
    def setUp(self):
        Author.objects.create(name='Dima', age=22)
        Book.objects.create(title='Stol')
        Book.objects.create(title='Lampa')
        Member.objects.create(book=Book.objects.get(title='Lampa'), author=Author.objects.get(name='Dima'))
        Member.objects.create(book=Book.objects.get(title='Stol'), author=Author.objects.get(name='Dima'))

    def testM2M(self):
        member = Member.objects.get(pk=1)
        self.assertEqual(member.author.age, 22)
        member = Member.objects.get(pk=2)
        self.assertEqual(member.book.title, 'Stol')