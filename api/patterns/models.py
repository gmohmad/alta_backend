import uuid

from django.contrib.auth.models import User
from django.db import models


class Pattern(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    image_url = models.URLField()
