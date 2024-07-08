import unittest

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    # setUp - допоміжна функція яка буде виконуватися перед кожним тестовим запитом
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55,
                                          author_name='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55,
                                          author_name='Author 2')

    def test_get(self):
        # book-list - отримати список книжок
        # book-detail - отримати детальну інформацію про книжку
        url = reverse('book-list')
        # self.client - клієнт який використовується для виконання запитів
        responce = self.client.get(url)
        # many=True - вказуєм що ми передали список в BookSerializer
        self.assertEqual(BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data, responce.data)
        # or
        # self.assertEqual(BookSerializer(book_1).data, responce.data[0])
        self.assertEqual(status.HTTP_200_OK, responce.status_code)

    def test_get_filter(self):
        url = reverse('book-list')
        responce = self.client.get(url, data={'price': 55})
        self.assertEqual(BookSerializer([self.book_2, self.book_3], many=True).data, responce.data)
        self.assertEqual(status.HTTP_200_OK, responce.status_code)

    def test_get_search(self):
        url = reverse('book-list')
        responce = self.client.get(url, data={'search': 'Author 1'})
        self.assertEqual(BookSerializer([self.book_1, self.book_3], many=True).data, responce.data)
        self.assertEqual(status.HTTP_200_OK, responce.status_code)

    # Перевіряє сортування за ціною за зростанням.
    def test_get_ordering_price_asc(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [self.book_1, self.book_2, self.book_3]  # Очікуваний порядок
        self.assertEqual(
            BookSerializer(books, many=True).data,
            response.data
        )

    # Перевіряє сортування за ціною за спаданням.
    def test_get_ordering_price_desc(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [self.book_2, self.book_3, self.book_1]  # Очікуваний порядок
        self.assertEqual(
            BookSerializer(books, many=True).data,
            response.data
        )

    # Перевіряє сортування за ім'ям автора за алфавітом.
    def test_get_ordering_author_name_asc(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'author_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [self.book_1, self.book_3, self.book_2]  # Очікуваний порядок
        self.assertEqual(
            BookSerializer(books, many=True).data,
            response.data
        )

    # Перевіряє сортування за ім'ям автора у зворотному алфавітному порядку.
    def test_get_ordering_author_name_desc(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': '-author_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [self.book_2, self.book_3, self.book_1]  # Очікуваний порядок
        self.assertEqual(
            BookSerializer(books, many=True).data,
            response.data
        )

    # Перевіряє сортування за кількома полями (спочатку за ціною за зростанням, потім за ім'ям автора за спаданням).
    def test_get_ordering_multiple_fields(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price,-author_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = [self.book_1, self.book_2, self.book_3]  # Очікуваний порядок
        self.assertEqual(
            BookSerializer(books, many=True).data,
            response.data
        )


if __name__ == '__main__':
    unittest.main()
