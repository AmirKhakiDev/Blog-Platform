from django.contrib import admin

from .models import Category, Comment
from .models import Author

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Author)