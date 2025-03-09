from django.urls import path

from .views import login_view, logout_view, show_user, change_password_view, upload_profile_image_view, add_comment, remove_user_expired_categories

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user_profile/', show_user, name='profile'),
    path('change-password/', change_password_view, name='change-password'),
    path('upload-profile-image/', upload_profile_image_view, name='upload-profile-image'),
    path('category/remove_expired/', remove_user_expired_categories, name='remove_user_expired_categories'),

]
