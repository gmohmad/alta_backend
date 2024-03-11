from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Vote


@receiver([post_save, post_delete], sender=Vote)
def update_pattern_rating(sender, instance, **kwargs):
    pattern = instance.pattern
    upvotes = Vote.objects.filter(pattern=pattern, vote_type='up').count()
    downvotes = Vote.objects.filter(pattern=pattern, vote_type='down').count()

    total = upvotes + downvotes + 0.1
    up_percentage = upvotes / total
    down_percentage = downvotes / total

    pattern.rating = up_percentage - down_percentage
    pattern.save()
