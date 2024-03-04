import uuid

from django.contrib.auth.models import User
from django.db import models


class Pattern(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patterns')
    title = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        total = self.upvotes + self.downvotes + 0.1
        up_percentage = self.upvotes / total
        down_percentage = self.downvotes / total

        self.rating = up_percentage - down_percentage or 0
        super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
