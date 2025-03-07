from django.contrib import admin
from .models import Video, Comments, Category, Lesson, News, Contact

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'slug')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment_User', 'text', 'rating', 'created_at', 'slug')
    prepopulated_fields = {"slug": ("comment_User",)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at', 'slug')
    prepopulated_fields = {"slug": ("category_name",)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('lesson_name', 'category', 'created_at', 'slug')
    prepopulated_fields = {"slug": ("lesson_name",)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'telephone_number1', 'address_name', 'slug')
    prepopulated_fields = {"slug": ("company_name",)}
