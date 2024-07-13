import unittest
from django.test import TestCase

from django.contrib.auth.models import User

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user_1 = User.objects.create(username='test_user_1',
                                     first_name='Ivan', last_name='Ivanov')
        user_2 = User.objects.create(username='test_user_2',
                                     first_name='Petr', last_name='Petrov')
        user_3 = User.objects.create(username='test_user_3',
                                     first_name='Sidor', last_name='Sidorov')

        self.book_1 = Book.objects.create(name='Test book 1', price=25,
                                          author_name='Author 1', owner=user_1)

        UserBookRelation.objects.create(user=user_1, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user_2, book=self.book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user_3, book=self.book_1, like=True,
                                        rate=4)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        # приводими до одного виду
        self.assertEqual('4.67', str(self.book_1.rating))


if __name__ == '__main__':
    unittest.main()
