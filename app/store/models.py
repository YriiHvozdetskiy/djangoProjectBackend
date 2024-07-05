from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7,
                                decimal_places=2)  # DecimalField - вказуємо кількість цифр і десяткових знаків до коми

    def __str__(self):
        return self.name
