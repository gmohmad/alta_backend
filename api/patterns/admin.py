from django.contrib import admin

from .models import Comment, Pattern

admin.site.register(Pattern)
admin.site.register(Comment)
