from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Book(models.Model):
    book_name = models.CharField(max_length=20)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.book_name}  price= {self.price}'


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=10)
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.first_name


class BooksIssued(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issued')
    person_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    issue_date = models.DateField()
    submission_date = models.DateField()

    def __str__(self):
        return str(self.issue_date)
