from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from blog.models import BlogEntry, UserProfile
from blog.serializers import BlogEntrySerializer
from blog.rating_provider import RatingProvider


def collect_user(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request.userprofile = None
        
        phone = request.headers.get("phone")
        if phone:
            try:
                user = UserProfile.objects.get(phone=phone)
                request.userprofile = user

            except UserProfile.DoesNotExist:
                pass

        return view_func(request, *args, **kwargs)

    return wrapper

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.userprofile:
            return HttpResponse(status=403)

        return view_func(request, *args, **kwargs)

    return wrapper


@collect_user
def get_blog_entries(request):
    blog_entries = BlogEntry.objects.all()
    serializer = BlogEntrySerializer(blog_entries, many=True)
    data = serializer.data

    if request.user:
        for entry in data:
            user_rate = RatingProvider.get_instance().get_rating(entry["id"], request.userprofile.phone)
            if user_rate:
                entry["rating"] = user_rate

    return JsonResponse(data, safe=False)


@csrf_exempt
@collect_user
@login_required
def rate_blog_entry(request):
    blog_id = request.POST.get("blog_id")
    rating = request.POST.get("rating")

    if not blog_id or not rating:
        return HttpResponse(status=400)

    try:
        blog_id = int(blog_id)
        rating = float(rating)
    except ValueError:
        return HttpResponse(status=400)

    if rating < 0 or rating > 5:
        return HttpResponse(status=400)

    try:
        blog_entry = BlogEntry.objects.get(id=blog_id)
    except BlogEntry.DoesNotExist:
        return HttpResponse(status=404)

    if request.userprofile:
        blog_entry.rate_blog(request.userprofile, rating)

    return HttpResponse(status=200)
