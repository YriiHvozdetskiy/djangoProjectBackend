from django.db.models import Avg

from store.models import UserBookRelation


def set_rating(book):
    # aggregate - повертає об'єкт з тих полів які всередині нього н-д:rating
    rating = (UserBookRelation.objects
              .filter(book=book)
              .aggregate(rating=Avg('rate'))
              .get('rating'))
    book.rating = rating
    book.save()
