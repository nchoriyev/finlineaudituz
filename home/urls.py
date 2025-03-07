from django.urls import path
from .views import home, contact, categories, category_detail, lesson_detail

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('category/', categories, name='category'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('lesson/<slug:lesson_slug>/', lesson_detail, name='lesson_detail'),  # Faqat dars slug'ini ishlatamiz
]
