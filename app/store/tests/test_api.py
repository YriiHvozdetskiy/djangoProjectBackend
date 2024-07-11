import json
import unittest

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):
    # setUp - допоміжна функція яка буде виконуватися перед кожним тестовим запитом
    def setUp(self):
        self.user = User.objects.create_user(username='test_user')

        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1',
                                          owner=self.user)
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

    def test_get_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Programming Python 3",
            "price": 150,
            "author_name": "Kotee"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_get_update(self):
        # args=[self.book_1.id] - передаймо айді в url
        url = reverse('book-detail', args=[self.book_1.id])
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # refresh_from_db - додаємо для того щою оновити в потоці дані
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_get_update_not_owner(self):
        self.user_2 = User.objects.create_user(username='test_user_2')
        # args=[self.book_1.id] - передаймо айді в url
        url = reverse('book-detail', args=[self.book_1.id])
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        # refresh_from_db - додаємо для того щою оновити в потоці дані
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_get_update_not_owner_but_staff(self):
        self.user_2 = User.objects.create_user(username='test_user_2',
                                               is_staff=True)
        # args=[self.book_1.id] - передаймо айді в url
        url = reverse('book-detail', args=[self.book_1.id])
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # refresh_from_db - додаємо для того щою оновити в потоці дані
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_delete_book(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=[self.book_1.id])
        self.client.force_login(self.user)
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())

        # Перевіряємо, що книга дійсно видалена
        with self.assertRaises(ObjectDoesNotExist):
            Book.objects.get(id=self.book_1.id)

        # Додаткова перевірка через API
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)


if __name__ == '__main__':
    unittest.main()
