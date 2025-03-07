from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import News, Contact, Category, Lesson, Comments
from users.forms import CommentForm

@login_required
def home(request):
    """
    View for the home page.
    If the user is logged in, their name, avatar image, and a list of news articles
    are passed to the page. If the user does not have an avatar image,
    a default avatar is displayed.
    """
    user = request.user
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'
    news = News.objects.all()
    subscriptions = user.categories.all()

    context = {
        'user': user,
        'avatar_image': avatar_url,
        'full_name': f"{user.first_name} {user.last_name}",
        'news' : news,
        'subscriptions':subscriptions,
        'end_date':user.end_date,
    }
    return render(request, 'index.html', context)

@login_required
def contact(request):
    """
    View for the contact page.
    Displays all contact information available on the site.
    """
    contacts = Contact.objects.all()
    user = request.user
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'


    context = {
        'user': user,
        'avatar_image': avatar_url,
        'full_name': f"{user.first_name} {user.last_name}",
        'contacts' : contacts,
    }

    return render(request, 'contact.html', context)

@login_required
def categories(request):
    """
    View to display categories.
    Shows all available categories on the site and the categories
    associated with the logged-in user.
    """
    user = request.user
    categories = Category.objects.all()
    user_categories = user.categories.all()  # Foydalanuvchiga tegishli kategoriyalar
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'

    context = {
        'avatar_image': avatar_url,
        'full_name': f"{user.first_name} {user.last_name}",
        'categories': categories,
        'user_categories': user_categories,
    }
    return render(request, ['category.html'], context)


@login_required
def category_detail(request, slug):
    """
    View to display category details.
    Checks if the user has purchased access to the category.
    If the user has not purchased the category, an error message
    is displayed, and they are redirected to the categories page.
    """
    user = request.user
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'
    category = get_object_or_404(Category, slug=slug)  # Slug orqali kategoriya olish

    if category not in request.user.categories.all():
        messages.error(request, "You have not purchased this course.")
        return redirect('categories')  # Redirect to the categories page

    lessons = Lesson.objects.filter(category=category)

    context = {
        'avatar_image': avatar_url,
        'full_name': f"{user.first_name} {user.last_name}",
        'category': category,
        'lessons': lessons,
    }

    return render(request, 'lessons.html', context)


@login_required
def lesson_detail(request, lesson_slug):
    """
    View to display lesson details.
    """
    user = request.user
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'

    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    comments = lesson.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.lesson = lesson
            comment.comment_User = request.user  # Foydalanuvchini qo'shish
            comment.save()
            return redirect('lesson_detail', lesson_slug=lesson.slug)
    else:
        form = CommentForm()

    # Foydalanuvchi ushbu darsga ruxsati borligini tekshiramiz
    if lesson.category not in request.user.categories.all():
        messages.error(request, "You have not purchased access to this lesson.")
        return redirect('categories')

    context = {
        'avatar_image':avatar_url,
        'full_name':f"{user.first_name}{user.last_name}",
        'lesson':lesson,
        'comments': comments,
        'form' : form,
    }



    return render(request, 'lesson_page.html', context)


