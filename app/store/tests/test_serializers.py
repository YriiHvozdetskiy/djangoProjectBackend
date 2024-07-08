import unittest

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(unittest.TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test book 1', price=25)
        book_2 = Book.objects.create(name='Test book 2', price=55)
        data = BookSerializer([book_2, book_1], many=True).data
        expected_data = [
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00'
            },
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00'
            }
        ]
        self.assertEqual(expected_data, data)


if __name__ == '__main__':
    unittest.main()
