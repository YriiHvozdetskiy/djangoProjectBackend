from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2)  # DecimalField - вказуємо кількість цифр і десяткових знаків до коми
    # blank=True впливає на те, чи буде поле обов'язковим в адмін-інтерфейсі Django.
    author_name = models.CharField(max_length=255, null=True)
    # ForeignKey -  Many to one, багато до одного (в одного user може бути багато замовленнь)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='my_books'
    )
    # through - використовується для відношення між моделями
    readers = models.ManyToManyField(
        User,
        through='UserBookRelation',
        related_name='books'
    )

    def __str__(self):
        return self.name


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible!'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.user.username}, {self.book.name}, rate: {self.rate}'
