from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    patro = models.CharField(max_length=20, null=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_chat_id = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=20)

    def __str__(self):
        return self.user.username
