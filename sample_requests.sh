# Rate a blog entry
curl -X POST -H "phone: 09115814641" -d "blog_id=1&rating=3.4" http://localhost:8000/api/rate_blog_entry/

# Get blog entries
curl -X GET -H "phone: 09115814641" http://localhost:8000/api/blog_entries/

# You can use python shell to create a userprofile
# python manage.py shell
# >>> from blog.models import UserProfile
# >>> UserProfile.objects.create(phone="09115814641")
# >>> exit()
