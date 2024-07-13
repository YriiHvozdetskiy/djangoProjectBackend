import unittest

from django.db.models import Count, Case, When
from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create(username='test_user_1')
        user_2 = User.objects.create(username='test_user_2')
        user_3 = User.objects.create(username='test_user_3')

        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='Author 1')
        book_2 = Book.objects.create(name='Test book 2', price=55,
                                     author_name='Author 5')

        UserBookRelation.objects.create(user=user_1, book=book_1, like=True)
        UserBookRelation.objects.create(user=user_2, book=book_1, like=True)
        UserBookRelation.objects.create(user=user_3, book=book_1, like=True)

        UserBookRelation.objects.create(user=user_1, book=book_2, like=True)
        UserBookRelation.objects.create(user=user_3, book=book_2, like=True)
        UserBookRelation.objects.create(user=user_2, book=book_2, like=False)

        # Book.objects.all().annotate(...):
        # Це додає обчислюване поле annotation_likes до кожного об'єкта Book у запиті.
        books = Book.objects.all().annotate(
            annotation_likes=Count(Case(When(userbookrelation__like=True, then=1))))
        data = BookSerializer(books, many=True).data

        # data = BookSerializer([book_2, book_1], many=True).data
        expected_data = [
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author_name': 'Author 5',
                'likes_count': 2,
                'annotation_likes': 2,
            },
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Author 1',
                'likes_count': 3,
                'annotation_likes': 3,
            }
        ]
        self.assertEqual(expected_data, data)


if __name__ == '__main__':
    unittest.main()
