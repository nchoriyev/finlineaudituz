from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import News, Category, Lesson
from django.core.files.storage import default_storage
from django.contrib.auth import update_session_auth_hash
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse
from .forms import ProfileImageForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
import requests









def success_view(request):
    return render(request, 'success.html')

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            # Eski parolni tekshiramiz
            user = authenticate(username=request.user.username, password=old_password)
            if not user:
                messages.error(request, "Eski parol noto‘g‘ri! Iltimos, qayta urinib ko‘ring.")
                return redirect('change-password')

            # Yangi parollar bir-biriga mosligini tekshiramiz
            if new_password1 != new_password2:
                messages.error(request, "Yangi parollar bir-biriga mos emas!")
                return redirect('change-password')

            # Parolni o'zgartiramiz
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Foydalanuvchini autentifikatsiya holatda qoldirish
            messages.success(request, "Parolingiz muvaffaqiyatli o‘zgartirildi!")
            return redirect('change-password')

    else:
        form = CustomPasswordChangeForm()

    return render(request, 'password_change.html', {'form': form})


@login_required
def upload_profile_image_view(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil rasmi muvaffaqiyatli yuklandi!")
            return redirect('upload-profile-image')
    else:
        form = ProfileImageForm(instance=request.user)

    return render(request, 'update_profile_image.html', {'form': form})
def login_view(request, ):
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "Muvaffaqqiyatli kirildi!")
            return redirect('home')
        else:
            messages.error(request, "Login yoki parol xato!")

    return render(request, "login_page.html")

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def show_user(request):
    user = request.user
    avatar_url = user.avatar_image.url if hasattr(user, 'avatar_image') and user.avatar_image else '/static/default-avatar.png'

    context = {
        'user': user,
        'full_name':f"{user.first_name} {user.last_name}",
        'avatar_image':avatar_url,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'password': user.password
    }

    return render(request, 'profile_user.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']

            # Eski parolni tekshiramiz
            user = authenticate(username=request.user.username, password=old_password)
            if not user:
                messages.error(request, "Eski parol noto‘g‘ri! Iltimos, qayta urinib ko‘ring.")
                return redirect('change-password')

            # Yangi parollar bir-biriga mosligini tekshiramiz
            if new_password1 != new_password2:
                messages.error(request, "Yangi parollar bir-biriga mos emas!")
                return redirect('change-password')

            # Parolni o'zgartiramiz
            request.user.set_password(new_password1)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Foydalanuvchini autentifikatsiya holatda qoldirish
            messages.success(request, "Parolingiz muvaffaqiyatli o‘zgartirildi!")
            return redirect('login')

    else:
        form = CustomPasswordChangeForm()

    return render(request, 'password_change.html', {'form': form})

@login_required
def upload_profile_image(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        user = request.user
        profile_image = request.FILES['profile_image']

        # ✅ Faqat rasm fayllarini qabul qilish
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
        file_extension = profile_image.name.split('.')[-1].lower()
        file_type = imghdr.what(profile_image)  # Fayl MIME turini aniqlash

        if file_extension not in allowed_extensions or file_type not in allowed_extensions:
            return JsonResponse({
                'success': False,
                'message': "❌ Faqat rasm fayllarini yuklash mumkin! (JPG, PNG, GIF, WEBP)"
            }, status=400)

        # ✅ Eski rasmni o‘chirish (agar mavjud bo‘lsa)
        if user.profile.image:
            default_storage.delete(user.profile.image.path)

        # ✅ Yangi rasmni saqlash
        user.profile.image.save(profile_image.name, profile_image)
        user.profile.save()

        # ✅ JSON Response - status 200
        return JsonResponse({
            'success': True,
            'message': "✅ Rasm muvaffaqiyatli yuklandi!",
            'new_image_url': user.profile.image.url
        }, status=200)

    # ❌ Xatolik bo‘lsa - status 400
    return JsonResponse({
        'success': False,
        'message': "❌ Rasm yuklashda xatolik yuz berdi."
    }, status=400)


@login_required
def add_comment(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.category = category
            comment.comment_User = request.user
            comment.save()
            messages.success(request, "Kommentariya muvaffaqiyatli qo‘shildi!")
            return redirect('category_detail', slug=slug)

    else:
        form = CommentForm()

    return render(request, 'category_detail.html', {'form': form, 'category': category})


from django.shortcuts import redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .models import Category, CustomUser


@login_required
def remove_user_expired_categories(request):
    """Agar foydalanuvchining muddati tugagan bo‘lsa, unga biriktirilgan kategoriyalarni o‘chiradi."""

    user = request.user

    # Foydalanuvchining end_date'ni tekshirish
    if user.end_date and user.end_date < now():
        expired_categories = Category.objects.filter(users=user)

        if expired_categories.exists():
            for category in expired_categories:
                messages.warning(request, f"⏳ '{category.category_name}' muddati tugadi va o‘chirildi.")
                user.categories.remove(category)

    return render(request, "category.html")

def get_video_otp(video_id):
    url = "https://dev.vdocipher.com/api/videos/{}/otp".format(video_id)
    headers = {
        "Authorization": f"Apikey {settings.VDO_CIPHER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"ttl": 300}  # OTP 5 daqiqa (300 soniya) amal qiladi
    response = requests.post(url, headers=headers, json=data)
    return response.json()
