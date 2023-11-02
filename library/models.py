from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    isbn = models.CharField(unique=True, max_length=13)
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=100)
    year = models.PositiveBigIntegerField()
    distributor = models.CharField(max_length=150)
    genre = models.CharField(max_length=50)
    defaultBorrowDays = models.PositiveBigIntegerField()

class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issueDate = models.DateField(null=False)
    returnDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.issueDate = timezone.now()
            print('issue date', self.issueDate)
        elif self.id and not self.returnDate:
            self.returnDate = timezone.now()
            print('return Date', self.returnDate)
        return super(Issue, self).save(*args, **kwargs)