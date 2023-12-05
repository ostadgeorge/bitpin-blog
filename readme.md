curl -X POST -H "phone: 09115814641" -d "blog_id=1&rating=3.4" http://localhost:8000/api/rate_blog_entry/

curl -X GET -H "phone: 09115814641" http://localhost:8000/api/blog_entries/