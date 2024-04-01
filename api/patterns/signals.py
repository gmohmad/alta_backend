from django.db.models.signals import post_delete, post_save

from .models import Vote


def update_pattern_rating(sender, instance, **kwargs):
    pattern = instance.pattern
    upvotes = Vote.objects.filter(pattern=pattern, vote_type='up').count()
    downvotes = Vote.objects.filter(pattern=pattern, vote_type='down').count()

    total = upvotes + downvotes + 0.1
    up_percentage = upvotes / total
    down_percentage = downvotes / total

    pattern.rating = up_percentage - down_percentage
    pattern.save()


post_save.connect(update_pattern_rating, sender=Vote)
post_delete.connect(update_pattern_rating, sender=Vote)
