from django.utils.timezone import now
from django.contrib import messages
from .models import Category

class ExpiredCategoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.end_date and user.end_date < now():
                expired_categories = Category.objects.filter(users=user)
                if expired_categories.exists():
                    for category in expired_categories:
                        messages.warning(request, f"⏳ '{category.category_name}' muddati tugadi va o‘chirildi.")
                        user.categories.remove(category)

        response = self.get_response(request)
        return response
