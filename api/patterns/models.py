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
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-rating',)


class Comment(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    VOTE_CHOICES = [('up', 'upvote'), ('down', 'downvote')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.vote_type

    class Meta:
        unique_together = ('pattern', 'user')
