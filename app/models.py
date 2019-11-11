from django.db import models
from django.utils import timezone

# Create your models here.
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    author = models.TextField()
    published = models.DateTimeField()
    genre = models.TextField()
    in_stock = models.BooleanField()
    description = models.TextField()


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now)
    action = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
