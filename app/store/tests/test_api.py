import unittest

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    def test_get(self):
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=55)
        # book-list - отримати список книжок
        # book-detail - отримати детальну інформацію про книжку
        url = reverse('book-list')
        # self.client - клієнт який використовується для виконання запитів
        responce = self.client.get(url)
        # many=True - вказуєм що ми передали список в BookSerializer
        self.assertEqual(BookSerializer([book_1, book_2], many=True).data, responce.data)
        # or
        # self.assertEqual(BookSerializer(book_1).data, responce.data[0])

        self.assertEqual(status.HTTP_200_OK, responce.status_code)


if __name__ == '__main__':
    unittest.main()
