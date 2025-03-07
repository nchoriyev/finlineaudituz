from django.db import models
from django.contrib.auth.models import AbstractUser
from home.models import Category
from django.utils import timezone



class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    avatar_image = models.ImageField(upload_to="user_images/", blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="users")
    end_date = models.DateTimeField(verbose_name="Tugash sanasi", null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')


    def __str__(self):
        return self.username
