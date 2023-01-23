from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from accounts.models import Author, User


class Posts(models.Model):
    text = models.CharField(max_length=225)
    create_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.text}-{self.create_at}'

    def average_rating(self):
        return self.rating_set.aggregate(Avg('rating'))['rating__avg']

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Rating(models.Model):
    post = models.ForeignKey(Posts,  related_name='rating_set', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

