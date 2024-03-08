from django.contrib import admin

from .models import Comment, Pattern, Vote

admin.site.register(Pattern)
admin.site.register(Comment)
admin.site.register(Vote)
