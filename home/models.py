from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


import core.settings


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, max_length=300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Avtomatik slug yaratish
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class Category(models.Model):
    """
    This model for storing the category of the video lessons
    """
    category_name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, max_length=300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)  # Avtomatik slug yaratish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Lesson(models.Model):
    """
    This model for every theme:
    - videos
    - lesson descriptions
    - and captions
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=50)
    video = models.FileField(upload_to='lesson_videos/', null=True, blank=True)
    description = models.TextField()
    material = models.FileField(upload_to='materials/', blank=True, null=True)
    theme_link = models.URLField(blank=True, null=True)
    created_at = models.TimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, max_length=300)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.lesson_name)  # Avtomatik slug yaratish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.lesson_name


class Comments(models.Model):
    """
    This model for comments:
    """

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name='comments'
    )

    comment_User = models.ForeignKey(
        core.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    rating = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, max_length=300)


class News(models.Model):
    """
    This model news for Dashboard for only users
    """
    image = models.ImageField(upload_to='news_photos/', null=True, blank=True)
    name = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.TimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, max_length=300)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Avtomatik slug yaratish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contact(models.Model):
    company_name = models.CharField(max_length=150)
    telephone_number1 = models.TextField()
    telephone_number2 = models.TextField()
    instagram = models.TextField()
    telegram = models.TextField()
    youtube = models.TextField()
    facebook = models.TextField()
    location = models.TextField()
    address_name = models.TextField()
    slug = models.SlugField(unique=True, null=True, max_length=300)






