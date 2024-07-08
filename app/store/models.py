from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2)  # DecimalField - вказуємо кількість цифр і десяткових знаків до коми
    # blank=True впливає на те, чи буде поле обов'язковим в адмін-інтерфейсі Django.
    author_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
